from sqlalchemy import Column, VARCHAR, DateTime, Integer
from ..configs import Base


class AgentEvent(Base):
    __tablename__ = "agent_event"

    agent_event_id = Column(Integer, primary_key=True, autoincrement=False)
    date = Column(DateTime)
    queue_id = Column(VARCHAR(128))
    agent_id = Column(Integer)
    event = Column(VARCHAR(16))
    reason = Column(VARCHAR(256), default=None, nullable=True)
    extension_id = Column(VARCHAR(12), default=None, nullable=True)
