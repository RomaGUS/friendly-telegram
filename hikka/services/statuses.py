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

    @classmethod
    def get_by_account(cls, account: User, content: int, page=0, limit=20) -> Status:
        offset = page * limit
        statuses = Status.objects().filter(account=account, content=content).limit(limit).skip(offset)
        return list(statuses)
