from models.release_type import Genre
from services.func import update_document

class ReleaseTypeService:
	@classmethod
	def create(cls, name: str, description: str, slug: str) -> Genre:
		release_type = Genre(name=name, description=description, slug=slug)
		release_type.save()
		return release_type

	@classmethod
	def get_by_slug(cls, slug: str):
		release_type = Genre.objects().filter(slug=slug).first()
		return release_type

	@classmethod
	def update(cls, release_type: Genre, **kwargs):
		release_type = update_document(release_type, kwargs)
		release_type.save()
