from ..configs import DBconnectionHandler
from ..entities import Tree


class TreeRepository:
    def __init__(self, database, echo=False):
        self.__database = DBconnectionHandler(database, echo)

    def insert(
        self,
        branch_id,
        call_id,
        chat_id,
        created_at,
        branch_label,
    ):
        with self.__database as db:
            data_insert = Tree(
                branch_id=branch_id,
                call_id=call_id,
                chat_id=chat_id,
                created_at=created_at,
                branch_label=branch_label,
            )
            db.session.merge(data_insert)
            db.session.commit()
