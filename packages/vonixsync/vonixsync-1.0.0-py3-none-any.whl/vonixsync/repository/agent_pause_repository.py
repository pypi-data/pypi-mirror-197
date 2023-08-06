from ..configs import DBconnectionHandler
from ..entities import AgentPause

from sqlalchemy import select
from sqlalchemy import func
from datetime import datetime, timedelta

from sqlalchemy import (
    Column,
    Table,
    BigInteger,
    SmallInteger,
    VARCHAR,
    MetaData,
    DateTime,
)

meta = MetaData()

agent_pause = Table(
    "agent_pause",
    meta,
    Column("agent_id", BigInteger, primary_key=True, autoincrement=False),
    Column("queue_id", VARCHAR(128), primary_key=True, autoincrement=False),
    Column("date", DateTime, primary_key=True, nullable=True),
    Column("pause_reason_id", SmallInteger, primary_key=True, autoincrement=False),
    Column("pause_secs", BigInteger, default=0),
)


class AgentPauseRepository:
    def __init__(self, database, echo=False):
        self.__database = DBconnectionHandler(database, echo)

    def insert(self, agent_id, queue_id, date, pause_secs, pause_reason_id):
        with self.__database as db:
            data_insert = AgentPause(
                agent_id=agent_id,
                queue_id=queue_id,
                date=date,
                pause_secs=pause_secs,
                pause_reason_id=pause_reason_id,
            )
            db.session.merge(data_insert)
            db.session.commit()

    def select_date(self):
        with self.__database as db:
            statement = select(func.max(agent_pause.c["date"]).label("last_date"))

            for row in db.session.execute(statement):
                if row[0] is None:
                    yesterday = datetime.now() - timedelta(days=1)
                    print(yesterday)

                    return int(yesterday.timestamp())

                timestamp_from_database = int(datetime.timestamp(row[0]))
                return timestamp_from_database

            db.session.commit()
