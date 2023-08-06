from sqlalchemy import Column, BigInteger, String, DateTime, VARCHAR
from ..configs import Base


class ChatMessage(Base):
    __tablename__ = "chat_message"
    message_id = Column(BigInteger, primary_key=True)
    chat_id = Column(BigInteger, index=True)
    message = Column(String)
    direction = Column(String)

    created_at = Column(DateTime, index=True)
    delivered_at = Column(DateTime)
    readed_at = Column(DateTime)
    answered_at = Column(DateTime)
    type = Column(VARCHAR(16))

    def __repr__(self):
        return f"chat_message {self.name}"
