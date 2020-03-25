from hikka.services.models.comment import Comment
from hikka.services.models.user import User

class CommentService:
    @classmethod
    def create(cls, subject, account: User, text: str) -> Comment:
        comment = Comment(subject=subject, account=account, text=text)
        comment.save()

        return comment
