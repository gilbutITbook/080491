from schema.response import ArticleResponse, CommentResponse
from schema.request import ArticleRequest, ArticleUpdateRequest, CommentRequest
from fastapi import FastAPI, status, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from database.db_connection import get_session
from sqlalchemy import select
from database.db_connection import engine, SessionFactory
from database.orm import Base
from models import Article, Comment
from starlette.middleware.sessions import SessionMiddleware
from schema.request import LoginRequest

Base.metadata.create_all(bind=engine)
app = FastAPI()

# 세션 미들웨어 등록
app.add_middleware(
    SessionMiddleware,
    secret_key="your-secret-key"
)

# # 게시글 저장
# articles = [
#     {"id": 1, "title": "FastAPI 시작하기", "content": "FastAPI 기본 개념 정리"},
#     {"id": 2, "title": "REST API 이해하기", "content": "REST 설계 원칙 정리"},
#     {"id": 3, "title": "Pydantic 활용하기", "content": "요청과 응답 모델 작성 방법"},
# ]

# 로그인
@app.post("/login")
def login_handler(request: Request, body: LoginRequest):
    request.session["name"] = body.name
    return {"message": "login success"}

# 전체 게시글 조회
@app.get(
    "/articles",
    response_model=list[ArticleResponse],
    status_code=status.HTTP_200_OK
)
def get_articles_handler(
    session = Depends(get_session)
):
    # session = SessionFactory()
    # try:
    stmt = select(Article)
    articles = session.execute(stmt).scalars().all()
    return articles
    # finally:
    #     session.close()

# 단일 게시글 조회
@app.get(
    "/articles/{article_id}",
    response_model=ArticleResponse,
    status_code=status.HTTP_200_OK
)
def get_article_handler(
    article_id: int,
    session = Depends(get_session)
):
    # session = SessionFactory()
    # try:
    stmt = select(Article).where(Article.id == article_id)
    article = session.execute(stmt).scalars().first()
    if article:
        return article
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo not found"
    )
    # finally:
    #     session.close()

# 게시글 생성
@app.post(
    "/articles",
    response_model=ArticleResponse,
    status_code=status.HTTP_201_CREATED
)
def create_article_handler(
    body: ArticleRequest,
    session = Depends(get_session)
):
    # session = SessionFactory()
    # try:
    article = Article(
        title=body.title,
        content=body.content,
    )
    session.add(article)
    session.commit()
    return article
    # finally:
    #     session.close()

# 게시글 수정
@app.patch(
    "/articles/{article_id}",
    response_model=ArticleResponse,
    status_code=status.HTTP_200_OK
)
def update_article_handler(
    article_id: int,
    body: ArticleUpdateRequest,
    session = Depends(get_session)
):
    # session = SessionFactory()
    # try:
    stmt = select(Article).where(Article.id == article_id)
    article = session.execute(stmt).scalars().first()
    if article:
        if body.title is not None:
            article.title = body.title
        if body.content is not None:
            article.content = body.content
        session.commit()
        return article
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo not found"
    )
    # finally:
    #     session.close()

# 게시글 삭제
@app.delete(
    "/articles/{article_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_article_handler(
    article_id: int,
    session = Depends(get_session)
):
    # session = SessionFactory()
    # try:
    stmt = select(Article).where(Article.id == article_id)
    article = session.execute(stmt).scalars().first()
    if article:
        session.delete(article)
        session.commit()
        return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo not found"
    )
    # finally:
    #     session.close()

# 댓글 작성
@app.post(
    "/articles/{article_id}/comments",
    response_model=CommentResponse
)
def create_comment_handler(
    article_id: int,
    request: Request,
    body: CommentRequest,
    session = Depends(get_session)
):
    # with SessionFactory() as session:
    name = request.session.get("name")
    if name is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Unauthorized"
        )
    stmt = select(Article).where(Article.id == article_id)
    article = session.execute(stmt).scalars().first()
    if article is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    comment = Comment(
        author=name,
        content=body.content,
        article_id=article_id,
    )
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment
