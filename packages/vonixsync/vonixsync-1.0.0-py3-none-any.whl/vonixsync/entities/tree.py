from sqlalchemy import Column, String, Integer, VARCHAR, BigInteger, DateTime
from ..configs import Base


class Tree(Base):
    __tablename__ = "tree"
    branch_id = Column(VARCHAR(36), primary_key=True, autoincrement=False)
    call_id = Column(String, primary_key=True, autoincrement=False)
    chat_id = Column(BigInteger, primary_key=True, autoincrement=False)
    created_at = Column(DateTime, primary_key=True, autoincrement=False)
    branch_label = Column(VARCHAR(256))

    def __repr__(self):
        return f"profiler {self.name}"
