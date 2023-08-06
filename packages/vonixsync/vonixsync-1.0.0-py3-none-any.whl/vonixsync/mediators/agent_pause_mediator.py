import warnings
from sqlalchemy.exc import OperationalError, IntegrityError
from ..utils import (
    fxn,
    ConnectionDatabaseError,
    print_finalized,
    NullPages,
    ApiKeyError,
)


async def sync_agent_pause(request, repository_dict, query_timestamp):
    timestamp = query_timestamp

    if query_timestamp == None:
        timestamp = repository_dict["agent_pause"].select_date()

    error_array = []

    try:
        pages = await request.async_summary_meta_request(timestamp)
        if pages == 0:
            raise NullPages("agent_event")

    except NullPages as error:
        print(SystemExit(f"\n{str(error)}"))
        error_array.append({type(error): "No new data found from api Request"})

    last_page = pages + 1
    try:
        for page in range(1, last_page):
            data_array = await request.async_summary_data_request(timestamp, page)
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    fxn()
                    try:
                        for agent_pause in data_array:
                            repository_dict["agent_pause"].insert(
                                agent_pause["agentId"],
                                agent_pause["queueId"],
                                agent_pause["period"],
                                agent_pause["pauseSecs"],
                                agent_pause["pauseReasonId"],
                            )
                    except KeyError as error:
                        error_array.append(
                            {
                                type(error): ApiKeyError(
                                    error, "agent_pause", agent_pause["agentId"]
                                )
                            }
                        )

            except IntegrityError as error:
                error_array.append({type(error): str(error.__dict__["orig"])})

    except OperationalError as error:
        error_array.append({"Database_connection_error": str(error.__dict__["orig"])})
        raise SystemExit(
            ConnectionDatabaseError(error_array).print_finalized()
        ) from error
    else:
        print_finalized(error_array, "agent_pause")
