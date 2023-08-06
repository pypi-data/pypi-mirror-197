from sqlalchemy import Column, BigInteger, String, DateTime
from ..configs import Base


class QueueSummary(Base):
    __tablename__ = "queue_summary"
    queue_id = Column(String, primary_key=True, autoincrement=False)
    date = Column(DateTime, primary_key=True, autoincrement=False)
    in_completed = Column(BigInteger, default=0)
    in_transferred = Column(BigInteger, default=0)
    in_abandoned = Column(BigInteger, default=0)
    in_completed_sla = Column(BigInteger, default=0)
    in_abandoned_sla = Column(BigInteger, default=0)
    out_completed = Column(BigInteger, default=0)
    out_transferred = Column(BigInteger, default=0)
    out_discarded = Column(BigInteger, default=0)
    auto_completed = Column(BigInteger, default=0)
    auto_transferred = Column(BigInteger, default=0)
    auto_discarded = Column(BigInteger, default=0)
    auto_abandoned = Column(BigInteger, default=0)
    in_call_secs = Column(BigInteger, default=0)
    out_call_secs = Column(BigInteger, default=0)
    auto_call_secs = Column(BigInteger, default=0)
    in_hold_secs_completed = Column(BigInteger, default=0)
    in_hold_secs_abandoned = Column(BigInteger, default=0)
    out_try_secs_completed = Column(BigInteger, default=0)
    out_try_secs_discarded = Column(BigInteger, default=0)
    auto_hold_secs_completed = Column(BigInteger, default=0)
    auto_hold_secs_abandoned = Column(BigInteger, default=0)
    auto_try_secs_completed = Column(BigInteger, default=0)
    auto_try_secs_discarded = Column(BigInteger, default=0)

    def __repr__(self):
        return f"profiler {self.name}"
