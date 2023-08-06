import warnings
from sqlalchemy.exc import OperationalError, IntegrityError
from ..utils import (
    fxn,
    ConnectionDatabaseError,
    print_finalized,
    NullPages,
    ApiKeyError,
)


async def sync_call(request, repository_dict, query_timestamp):
    timestamp = query_timestamp

    if query_timestamp == None:
        timestamp = repository_dict["call"].select_date()

    error_array = []
    try:
        pages = await request.async_summary_meta_request(timestamp)

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
                    for call in data_array:
                        profiler_array = call["profilers"]
                        tree_array = call["trees"]
                        call_rating_array = call["callsRatings"]
                        try:
                            repository_dict["call"].insert(
                                call["id"],
                                call["queueId"],
                                call["direction"],
                                call["agentOffers"],
                                call["callerNumber"],
                                call["callerInfo"],
                                call["holdSecs"],
                                call["talkSecs"],
                                call["ringSecs"],
                                call["status"],
                                call["reason"],
                                call["localityId"],
                                call["callTypeId"],
                                call["trunkingId"],
                                None,
                                call["abandonKey"],
                                call["initialPosition"],
                                call["abandonPosition"],
                                call["createdAt"],
                                call["answerAt"],
                                call["hangupAt"],
                                call["transferredTo"],
                                call["agentId"],
                            )
                        except KeyError as error:
                            error_array.append(
                                {type(error): ApiKeyError(error, "call", call["id"])}
                            )

                        if len(profiler_array) > 0:
                            try:
                                for profiler in profiler_array:
                                    repository_dict["profiler"].insert(
                                        profiler["id"],
                                        profiler["callId"],
                                        0,
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
                            try:
                                for tree in tree_array:
                                    repository_dict["tree"].insert(
                                        tree["id"],
                                        tree["callId"],
                                        0,
                                        call["createdAt"],
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
                        if len(call_rating_array) > 0:
                            try:
                                for call_rating in call_rating_array:
                                    repository_dict["call_rating"].insert(
                                        call_rating["callId"],
                                        call_rating["name"],
                                        call_rating["createdAt"],
                                        call_rating["value"],
                                    )
                            except KeyError as error:
                                error_array.append(
                                    {
                                        type(error): ApiKeyError(
                                            error, "call_rating", call_rating["callId"]
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
        print_finalized(error_array, "call, call_rating, profiler and tree")
