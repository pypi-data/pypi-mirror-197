from ..configs import DBconnectionHandler
from ..entities import QueueSummary

from sqlalchemy import select
from sqlalchemy import func
from datetime import datetime, timedelta

from sqlalchemy import (
    Column,
    Table,
    VARCHAR,
    MetaData,
    DateTime,
    BigInteger,
)

meta = MetaData()

queue_summary = Table(
    "queue_summary",
    meta,
    Column("queue_id", VARCHAR(128), primary_key=True, autoincrement=False),
    Column("date", DateTime, primary_key=True, autoincrement=False),
    Column("in_completed", BigInteger, default=0),
    Column("in_transferred", BigInteger, default=0),
    Column("in_abandoned", BigInteger, default=0),
    Column("in_completed_sla", BigInteger, default=0),
    Column("in_abandoned_sla", BigInteger, default=0),
    Column("out_completed", BigInteger, default=0),
    Column("out_transferred", BigInteger, default=0),
    Column("out_discarded", BigInteger, default=0),
    Column("auto_completed", BigInteger, default=0),
    Column("auto_transferred", BigInteger, default=0),
    Column("auto_discarded", BigInteger, default=0),
    Column("auto_abandoned", BigInteger, default=0),
    Column("in_call_secs", BigInteger, default=0),
    Column("out_call_secs", BigInteger, default=0),
    Column("auto_call_secs", BigInteger, default=0),
    Column("in_hold_secs_completed", BigInteger, default=0),
    Column("in_hold_secs_abandoned", BigInteger, default=0),
    Column("out_try_secs_completed", BigInteger, default=0),
    Column("out_try_secs_discarded", BigInteger, default=0),
    Column("auto_hold_secs_completed", BigInteger, default=0),
    Column("auto_hold_secs_abandoned", BigInteger, default=0),
    Column("auto_try_secs_completed", BigInteger, default=0),
    Column("auto_try_secs_discarded", BigInteger, default=0),
)


class QueueSummaryRepository:
    def __init__(self, database, echo=False):
        self.__database = DBconnectionHandler(database, echo)

    def insert(
        self,
        queue_id,
        date,
        in_completed,
        in_transferred,
        in_abandoned,
        in_completed_sla,
        in_abandoned_sla,
        out_completed,
        out_transferred,
        out_discarded,
        auto_completed,
        auto_transferred,
        auto_discarded,
        auto_abandoned,
        in_call_secs,
        out_call_secs,
        auto_call_secs,
        in_hold_secs_completed,
        in_hold_secs_abandoned,
        out_try_secs_completed,
        out_try_secs_discarded,
        auto_hold_secs_completed,
        auto_hold_secs_abandoned,
        auto_try_secs_completed,
        auto_try_secs_discarded,
    ):
        with self.__database as db:
            data_insert = QueueSummary(
                queue_id=queue_id,
                date=date,
                in_completed=in_completed,
                in_transferred=in_transferred,
                in_abandoned=in_abandoned,
                in_completed_sla=in_completed_sla,
                in_abandoned_sla=in_abandoned_sla,
                out_completed=out_completed,
                out_transferred=out_transferred,
                out_discarded=out_discarded,
                auto_completed=auto_completed,
                auto_transferred=auto_transferred,
                auto_discarded=auto_discarded,
                auto_abandoned=auto_abandoned,
                in_call_secs=in_call_secs,
                out_call_secs=out_call_secs,
                auto_call_secs=auto_call_secs,
                in_hold_secs_completed=in_hold_secs_completed,
                in_hold_secs_abandoned=in_hold_secs_abandoned,
                out_try_secs_completed=out_try_secs_completed,
                out_try_secs_discarded=out_try_secs_discarded,
                auto_hold_secs_completed=auto_hold_secs_completed,
                auto_hold_secs_abandoned=auto_hold_secs_abandoned,
                auto_try_secs_completed=auto_try_secs_completed,
                auto_try_secs_discarded=auto_try_secs_discarded,
            )
            db.session.merge(data_insert)
            db.session.commit()

    def select_date(self):
        with self.__database as db:
            statement = select(func.max(queue_summary.c["date"]).label("last_date"))

            for row in db.session.execute(statement):
                if row[0] is None:
                    yesterday = datetime.now() - timedelta(days=1)
                    return int(yesterday.timestamp())

                timestamp_from_database = int(datetime.timestamp(row[0]))

                return timestamp_from_database

            db.session.commit()
