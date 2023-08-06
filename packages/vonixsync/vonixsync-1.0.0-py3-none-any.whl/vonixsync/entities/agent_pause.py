from sqlalchemy import Column, VARCHAR, DateTime, BigInteger, Integer, SmallInteger
from ..configs import Base


class AgentPause(Base):
    __tablename__ = "agent_pause"
    agent_id = Column(Integer, primary_key=True, autoincrement=False)
    queue_id = Column(VARCHAR(128), primary_key=True, autoincrement=False)
    date = Column(DateTime, primary_key=True, nullable=True)
    pause_reason_id = Column(SmallInteger, primary_key=True, autoincrement=False)
    pause_secs = Column(BigInteger, default=0)
