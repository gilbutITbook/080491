from datetime import datetime
from pydantic import BaseModel

# 게시글 응답 모델
class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str

# 댓글 응답 모델
class CommentResponse(BaseModel):
    id: int
    author: str
    content: str
    created_at: datetime