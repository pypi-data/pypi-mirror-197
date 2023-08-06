import warnings
from sqlalchemy.exc import OperationalError, IntegrityError
from ..utils import (
    fxn,
    ConnectionDatabaseError,
    print_finalized,
    NullPages,
    ApiKeyError,
)


async def sync_agent_event(request, repository_dict, query_agent_event_id):
    agent_event_id = query_agent_event_id

    if query_agent_event_id is None:
        agent_event_id = repository_dict["agent_event"].select_agent_event_id()
        if agent_event_id is None:
            agent_event_id = 0

    error_array = []

    try:
        pages = await request.async_summary_event_meta_request(agent_event_id)

        if pages == 0:
            raise NullPages("agent_event")

    except NullPages as error:
        print(SystemExit(f"\n{str(error)}"))
        error_array.append({type(error): "No new data found from api Request"})
    last_page = pages + 1
    try:
        for page in range(1, last_page):
            data_array = await request.async_summary_event_data_request(
                page, agent_event_id
            )
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    fxn()
                    for agent_event in data_array:
                        if "event" not in agent_event:
                            continue

                        if "reason" not in agent_event and "extensionId" in agent_event:
                            repository_dict["agent_event"].insert(
                                agent_event["id"],
                                agent_event["createdAt"],
                                agent_event["queueId"],
                                agent_event["agentId"],
                                agent_event["event"],
                                None,
                                agent_event["extensionId"],
                            )
                            continue

                        if "extensionId" not in agent_event and "reason" in agent_event:
                            repository_dict["agent_event"].insert(
                                agent_event["id"],
                                agent_event["createdAt"],
                                agent_event["queueId"],
                                agent_event["agentId"],
                                agent_event["event"],
                                agent_event["reason"],
                                None,
                            )
                            continue

                        try:
                            repository_dict["agent_event"].insert(
                                agent_event["id"],
                                agent_event["createdAt"],
                                agent_event["queueId"],
                                agent_event["agentId"],
                                agent_event["event"],
                                agent_event["reason"],
                                agent_event["extensionId"],
                            )
                        except KeyError as error:
                            error_array.append(
                                {
                                    type(error): ApiKeyError(
                                        error, "agent_event", agent_event["id"]
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
        print_finalized(error_array, "agent_event")
