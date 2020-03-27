from hikka.services.models.vote import Vote
from hikka.services.models.user import User
from datetime import datetime

class VoteService:
    @classmethod
    def submit(cls, subject, account: User, rating: int) -> Vote:
        vote = Vote.objects().filter(subject=subject, account=account).first()

        if vote is None:
            vote = Vote(subject=subject, account=account, rating=rating)
            vote.save()

        else:
            vote.updated = datetime.now()
            vote.rating = rating

        return vote
