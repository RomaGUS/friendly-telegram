from hikka.services.models.status import Status
from hikka.services.models.user import User

class StatusService:
    @classmethod
    def get(cls, subject, account: User, content: int) -> Status:
        status = Status.objects().filter(
            subject=subject, account=account,
            content=content
        ).first()

        if status is None:
            status = Status(subject=subject, account=account, content=content)
            status.save()

        return status
