from hikka.services.models.category import Category
from typing import List

class CategoryService:
    @classmethod
    def create(cls, name: str, slug: str, description=None) -> Category:
        category = Category(
            name=name,
            slug=slug,
            description=description
        )

        category.save()
        return category

    @classmethod
    def get_by_slug(cls, slug: str):
        category = Category.objects().filter(slug=slug).first()
        return category

    @classmethod
    def list(cls, page=0, limit=10) -> List[Category]:
        offset = page * limit
        category = Category.objects().filter().limit(limit).skip(offset)
        return list(category)
