from sqlalchemy import Column, String, Integer, VARCHAR
from ..configs import Base


class Queue(Base):
    __tablename__ = "queue"
    queue_id = Column(String, primary_key=True, autoincrement=False)
    name = Column(VARCHAR(256))
    description = Column(String, default="")
    is_in = Column(Integer)
    is_out = Column(Integer)
    is_auto = Column(Integer)
    dialer_mode = Column(VARCHAR(36), default="dialerMode")

    def __repr__(self):
        return f"profiler {self.name}"
