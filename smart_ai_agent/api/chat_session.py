import uuid
from datetime import datetime, timedelta

from .models import UserSession, User


class ChatSession:
    def __init__(self, user: User):
        self.user = user
        self.session_time_out = 4

    def create(self) -> UserSession:
        expiry_time = datetime.now() + \
            timedelta(minutes=60 * self.session_time_out)
        session = UserSession.objects.create(
            user=self.user,
            session_id=str(uuid.uuid4()),
            expire_at=expiry_time
        )
        return session

    def get_current_session(self) -> UserSession | None:
        current_time = datetime.now()
        sessions = UserSession.objects.filter(
            user_id=self.user.id, expire_at__lte=current_time)
        if not sessions:
            return None
        else:
            return sessions.first()
