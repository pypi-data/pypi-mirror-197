from ..configs import DBconnectionHandler
from ..entities import Call

from sqlalchemy import select
from sqlalchemy import func
from datetime import datetime, timedelta

from sqlalchemy import (
    Column,
    Table,
    Integer,
    VARCHAR,
    MetaData,
    DateTime,
)

meta = MetaData()

call = Table(
    "call",
    meta,
    Column("call_id", VARCHAR(128), primary_key=True),
    Column("queue_id", VARCHAR(128), primary_key=True, index=True),
    Column("direction", VARCHAR(12)),
    Column("offers", Integer, default=0),
    Column("caller_id", VARCHAR(30), index=True),
    Column("caller_info", VARCHAR(30)),
    Column("hold_secs", Integer, default=0),
    Column("talk_secs", Integer, default=0),
    Column("ring_secs", Integer, default=0),
    Column("status", VARCHAR(16), index=True),
    Column("status_cause", VARCHAR(255)),
    Column("locality", VARCHAR(256), default=""),
    Column("call_type", VARCHAR(256)),
    Column("trunking", VARCHAR(256)),
    Column("carrier", VARCHAR(256)),
    Column("exit_key", Integer),
    Column("initial_position", Integer),
    Column("abandon_position", Integer),
    Column("start_time", DateTime, index=True),
    Column("answer_time", DateTime),
    Column("hangup_time", DateTime),
    Column("transferred_to", VARCHAR(255)),
    Column("agent_id", Integer, index=True),
)


class CallRepository:
    def __init__(self, database, echo=False):
        self.__database = DBconnectionHandler(database, echo)

    def insert(
        self,
        call_id,
        queue_id,
        direction,
        offers,
        caller_id,
        caller_info,
        hold_secs,
        talk_secs,
        ring_secs,
        status,
        status_cause,
        locality,
        call_type,
        trunking,
        carrier,
        exit_key,
        initial_position,
        abandon_position,
        start_time,
        answer_time,
        hangup_time,
        transferred_to,
        agent_id,
    ):
        with self.__database as db:
            data_insert = Call(
                call_id=call_id,
                queue_id=queue_id,
                direction=direction,
                offers=offers,
                caller_id=caller_id,
                caller_info=caller_info,
                hold_secs=hold_secs,
                talk_secs=talk_secs,
                ring_secs=ring_secs,
                status=status,
                status_cause=status_cause,
                locality=locality,
                call_type=call_type,
                trunking=trunking,
                carrier=carrier,
                exit_key=exit_key,
                initial_position=initial_position,
                abandon_position=abandon_position,
                start_time=start_time,
                answer_time=answer_time,
                hangup_time=hangup_time,
                transferred_to=transferred_to,
                agent_id=agent_id,
            )
            db.session.merge(data_insert)
            db.session.commit()

    def select_date(self):
        with self.__database as db:
            statement = select(func.max(call.c["start_time"]).label("last_date"))

            for row in db.session.execute(statement):
                if row[0] is None:
                    yesterday = datetime.now() - timedelta(days=1)
                    return int(yesterday.timestamp())

                timestamp_from_database = int(datetime.timestamp(row[0]))

                return timestamp_from_database

            db.session.commit()
