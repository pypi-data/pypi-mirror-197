from ..configs import DBconnectionHandler
from ..entities import CallRating


class CallRatingRepository:
    def __init__(self, database, echo=False):
        self.__database = DBconnectionHandler(database, echo)

    def insert(self, call_id, property, insert_time, rate):
        with self.__database as db:
            data_insert = CallRating(
                call_id=call_id, property=property, insert_time=insert_time, rate=rate
            )
            db.session.merge(data_insert)
            db.session.commit()
