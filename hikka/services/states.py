from hikka.services.models.state import State
from typing import List

class StatesService:
    @classmethod
    def create(cls, name: str, slug: str, description=None) -> State:
        status = State(
            name=name,
            slug=slug,
            description=description
        )

        status.save()
        return status

    @classmethod
    def get_by_slug(cls, slug: str):
        status = State.objects().filter(slug=slug).first()
        return status

    @classmethod
    def list(cls, page=0, limit=10) -> List[State]:
        offset = page * limit
        statuses = State.objects().filter().limit(limit).skip(offset)
        return list(statuses)
