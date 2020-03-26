from hikka.services.models.comment import Comment
from hikka.services.models.user import User
from typing import List

class CommentService:
    @classmethod
    def create(cls, subject, account: User, text: str) -> Comment:
        comment = Comment(subject=subject, account=account, text=text)
        comment.save()

        return comment

    @classmethod
    def get_by_counter(cls, counter: int, account: User):
        comment = Comment.objects().filter(counter=counter, account=account).first()
        return comment

    @classmethod
    def list(cls, subject, page=0, limit=10) -> List[Comment]:
        offset = page * limit
        comments = Comment.objects().filter(subject=subject).limit(limit).skip(offset)
        return list(comments)
