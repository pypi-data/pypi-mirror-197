from ..configs import DBconnectionHandler
from ..entities import Agent


class AgentsRepository:
    def __init__(self, database, echo=False):
        self.__database = DBconnectionHandler(database, echo)

    def insert(self, agent_id, name, nickname, active, default_queue):
        with self.__database as db:
            data_insert = Agent(
                agent_id=agent_id,
                name=name,
                nickname=nickname,
                active=active,
                default_queue=default_queue,
            )
            db.session.merge(data_insert)
            db.session.commit()
