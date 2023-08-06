import warnings
from sqlalchemy.exc import OperationalError, IntegrityError
from ..utils import (
    fxn,
    ConnectionDatabaseError,
    print_finalized,
    NullPages,
    ApiKeyError,
)


async def sync_agent(request, repository_dict):
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
                    try:
                        for agent in data_array:
                            repository_dict["agent"].insert(
                                int(agent["id"]),
                                agent["name"],
                                agent["nickname"],
                                agent["active"],
                                agent["defaultQueueId"],
                            )
                    except KeyError as error:
                        error_array.append(
                            {type(error): ApiKeyError(error, "agent", agent["id"])}
                        )

            except IntegrityError as error:
                error_array.append({type(error): str(error.__dict__["orig"])})

    except OperationalError as error:
        error_array.append({"Database_connection_error": str(error.__dict__["orig"])})
        raise SystemExit(
            ConnectionDatabaseError(error_array).print_finalized()
        ) from error
    else:
        print_finalized(error_array, "agent")
