from hikka.services.models.descriptor import Descriptor
from typing import List

class DescriptorService:
    @classmethod
    def create(cls, category: str, name: str, slug: str, description=None) -> Descriptor:
        descriptor = Descriptor(
            category=category,
            name=name,
            slug=slug,
            description=description
        )

        descriptor.save()
        return descriptor

    @classmethod
    def get_by_slug(cls, category: str, slug: str):
        descriptor = Descriptor.objects().filter(category=category, slug=slug).first()
        return descriptor

    @classmethod
    def list(cls, category: str) -> List[Descriptor]:
        descriptors = Descriptor.objects().filter(category=category)
        return list(descriptors)
