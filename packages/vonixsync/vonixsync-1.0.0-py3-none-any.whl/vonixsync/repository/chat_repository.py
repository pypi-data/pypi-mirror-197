from ..configs import DBconnectionHandler
from ..entities import Chat

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
    BigInteger,
)

meta = MetaData()

chat = Table(
    "chat",
    meta,
    Column("chat_id", BigInteger, primary_key=True),
    Column("agent_id", BigInteger, index=True),
    Column("queue_id", VARCHAR(128), index=True),
    Column("source", VARCHAR(36)),
    Column("source_id", VARCHAR(256)),
    Column("name", VARCHAR(256)),
    Column("direction", VARCHAR(12)),
    Column("status", VARCHAR(36)),
    Column("hold_secs", Integer, default=0),
    Column("talk_secs", Integer, default=0),
    Column("chat_secs", Integer, default=0),
    Column("created_at", DateTime, index=True),
    Column("answered_at", DateTime, index=True),
    Column("finished_at", DateTime, index=True),
)


class ChatRepository:
    def __init__(self, database, echo=False):
        self.__database = DBconnectionHandler(database, echo)

    def insert(
        self,
        chat_id,
        agent_id,
        queue_id,
        source,
        source_id,
        name,
        direction,
        status,
        hold_secs,
        talk_secs,
        chat_secs,
        created_at,
        answered_at,
        finished_at,
    ):
        with self.__database as db:
            data_insert = Chat(
                chat_id=chat_id,
                agent_id=agent_id,
                queue_id=queue_id,
                source=source,
                source_id=source_id,
                name=name,
                direction=direction,
                status=status,
                hold_secs=hold_secs,
                talk_secs=talk_secs,
                chat_secs=chat_secs,
                created_at=created_at,
                answered_at=answered_at,
                finished_at=finished_at,
            )
            db.session.merge(data_insert)
            db.session.commit()

    def select_date(self):
        with self.__database as db:
            statement = select(func.max(chat.c["created_at"]).label("last_date"))

            for row in db.session.execute(statement):
                if row[0] is None:
                    yesterday = datetime.now() - timedelta(days=1)
                    return int(yesterday.timestamp())

                timestamp_from_database = int(datetime.timestamp(row[0]))

                return timestamp_from_database

            db.session.commit()
