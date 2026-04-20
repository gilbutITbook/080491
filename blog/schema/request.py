from pydantic import BaseModel

# 게시글 생성 요청 모델
class ArticleRequest(BaseModel):
    title: str
    content: str

# 게시글 수정 요청 모델
class ArticleUpdateRequest(BaseModel):
    title: str | None = None
    content: str | None = None

# 댓글 생성 요청 모델
class CommentRequest(BaseModel):
    # author: str
    content: str

# 로그인 요청 모델
class LoginRequest(BaseModel):
    name: str
