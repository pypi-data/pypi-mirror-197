import warnings
from sqlalchemy.exc import OperationalError, IntegrityError
from ..utils import fxn, ConnectionDatabaseError, print_finalized, NullPages


async def sync_queue(request, repository_dict):
    error_array = []

    try:
        pages = await request.async_meta_request()

        if pages == 0:
            raise NullPages("agent")

    except NullPages as error:
        print(SystemExit(f"\n{str(error)}"))
        error_array.append({type(error): "No new data found from api Request"})

    last_page = pages + 1
    try:
        for page in range(1, last_page):
            data_array = await request.async_data_request(page)
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    fxn()
                    for queue in data_array:
                        try:
                            repository_dict["queue"].insert(
                                queue["id"],
                                queue["name"],
                                queue["description"],
                                queue["directionIn"],
                                queue["directionOut"],
                                queue["directionAuto"],
                                queue["dialerMode"],
                            )
                        except KeyError as error:
                            error_array.append({type(error): str(error)})

            except IntegrityError as error:
                error_array.append({type(error): str(error.__dict__["orig"])})

    except OperationalError as error:
        error_array.append({"Database_connection_error": str(error.__dict__["orig"])})
        raise SystemExit(
            ConnectionDatabaseError(error_array).print_finalized()
        ) from error

    else:
        print_finalized(error_array, "queue")
