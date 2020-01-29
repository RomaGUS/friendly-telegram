from hikka.services.models.type import ReleaseType
from typing import List

class ReleaseTypesService:
    @classmethod
    def create(cls, name: str, slug: str, description=None) -> ReleaseType:
        rtype = ReleaseType(name=name, slug=slug, description=description)
        rtype.save()
        return rtype

    @classmethod
    def get_by_slug(cls, slug: str):
        rtype = ReleaseType.objects().filter(slug=slug).first()
        return rtype

    @classmethod
    def list(cls, page=0, limit=10) -> List[ReleaseType]:
        offset = page * limit
        rtype = ReleaseType.objects().filter().limit(limit).skip(offset)
        return list(rtype)
