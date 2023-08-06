from sqlalchemy import Column, String, Integer, BOOLEAN, VARCHAR, Numeric
from ..configs import Base


class Agent(Base):
    __tablename__ = "agent"
    agent_id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(VARCHAR(256))
    nickname = Column(VARCHAR(256), nullable=True)
    active = Column(BOOLEAN)
    default_queue = Column(VARCHAR(128))

    def __repr__(self):
        return f"agent {self.name}"
