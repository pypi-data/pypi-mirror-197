from sqlalchemy import Column, String, VARCHAR, DateTime
from ..configs import Base


class CallRating(Base):
    __tablename__ = "call_rating"
    call_id = Column(VARCHAR(128), primary_key=True, autoincrement=False)
    property = Column(VARCHAR(256), primary_key=True, autoincrement=False, default="")
    insert_time = Column(DateTime, primary_key=True, autoincrement=False)
    rate = Column(String, default="")

    def __repr__(self):
        return f"call_rating {self.name}"
