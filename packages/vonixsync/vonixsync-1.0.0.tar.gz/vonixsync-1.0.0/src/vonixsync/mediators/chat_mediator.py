import warnings
from sqlalchemy.exc import OperationalError, IntegrityError
from ..utils import (
    fxn,
    ConnectionDatabaseError,
    print_finalized,
    NullPages,
    ApiKeyError,
)


async def sync_chat(request, repository_dict, query_timestamp):
    timestamp = query_timestamp

    if query_timestamp == None:
        timestamp = repository_dict["chat"].select_date()

    error_array = []
    pages = await request.async_summary_meta_request(timestamp)
    try:
        if pages == 0:
            raise NullPages("agent")

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
                    for chat in data_array:
                        messages_array = chat["chatMessages"]
                        profiler_array = chat["profilers"]
                        tree_array = chat["trees"]
                        try:
                            repository_dict["chat"].insert(
                                chat["id"],
                                chat["agentId"],
                                chat["queueId"],
                                chat["source"],
                                chat["sourceId"],
                                chat["name"],
                                chat["direction"],
                                chat["status"],
                                chat["holdSecs"],
                                chat["talkSecs"],
                                chat["chatSecs"],
                                chat["createdAt"],
                                chat["answeredAt"],
                                chat["finishedAt"],
                            )
                        except KeyError as error:
                            error_array.append({type(error): str(error)})

                        if len(messages_array) > 0:
                            for message in messages_array:
                                try:
                                    repository_dict["chat_message"].insert(
                                        message["chatId"],
                                        message["id"],
                                        message["message"],
                                        message["direction"],
                                        message["createdAt"],
                                        message["deliveredAt"],
                                        message["readedAt"],
                                        message["answeredAt"],
                                        message["type"],
                                    )
                                except KeyError as error:
                                    error_array.append(
                                        {
                                            type(error): ApiKeyError(
                                                error, "chat_message", profiler["id"]
                                            )
                                        }
                                    )

                        if len(profiler_array) > 0:
                            for profiler in profiler_array:
                                try:
                                    repository_dict["profiler"].insert(
                                        profiler["id"],
                                        "0",
                                        profiler["chatId"],
                                        profiler["createdAt"],
                                        profiler["name"],
                                        profiler["value"],
                                    )
                                except KeyError as error:
                                    error_array.append(
                                        {
                                            type(error): ApiKeyError(
                                                error, "profiler", profiler["id"]
                                            )
                                        }
                                    )

                        if len(tree_array) > 0:
                            for tree in tree_array:
                                try:
                                    repository_dict["tree"].insert(
                                        tree["id"],
                                        "0",
                                        tree["chatId"],
                                        chat["createdAt"],
                                        tree["label"],
                                    )
                                except KeyError as error:
                                    error_array.append(
                                        {
                                            type(error): ApiKeyError(
                                                error, "tree", tree["id"]
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
        print_finalized(error_array, "chat, chat_message, profiler and tree")
