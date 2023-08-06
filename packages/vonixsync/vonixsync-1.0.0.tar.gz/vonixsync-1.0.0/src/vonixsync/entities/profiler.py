from sqlalchemy import BigInteger, VARCHAR, DateTime, String, Column
from ..configs import Base


class Profiler(Base):
    __tablename__ = "profiler"
    field_id = Column(BigInteger, primary_key=True, autoincrement=False)
    call_id = Column(VARCHAR(128), primary_key=True, autoincrement=False, default="0")
    chat_id = Column(BigInteger, primary_key=True, autoincrement=False, default=0)
    created_at = Column(DateTime, primary_key=True, autoincrement=False)
    field_name = Column(VARCHAR(256))
    field_value = Column(String)

    def __repr__(self):
        return f"profiler {self.name}"
