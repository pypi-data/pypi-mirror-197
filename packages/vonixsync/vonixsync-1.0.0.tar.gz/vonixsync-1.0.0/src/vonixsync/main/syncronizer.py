import asyncio

from ..api import Request
from ..configs import UserConfigs
from ..mediators import sync_agent
from ..mediators import sync_agent_pause
from ..mediators import sync_agent_summary
from ..mediators import sync_call
from ..mediators import sync_chat
from ..mediators import sync_queue
from ..mediators import sync_queue_summary
from ..mediators import sync_agent_event

from ..repository import AgentsRepository
from ..repository import AgentSummaryRepository
from ..repository import AgentPauseRepository
from ..repository import QueueRepository
from ..repository import QueueSummaryRepository
from ..repository import ProfilerRepository
from ..repository import CallRatingRepository
from ..repository import CallRepository
from ..repository import ChatMessageRepository
from ..repository import ChatRepository
from ..repository import TreeRepository
from ..repository import AgentEventRepository

from ..utils import bcolors


class Syncronizer:
    def __init__(
        self,
        token,
        database_string,
        option="all",
        timestamp=None,
        echo=False,
        agent_event_id=None,
    ):
        self.__token = token
        self.__string_connection = database_string
        self.__endpoint = self.__define_endpoint(option)
        self.__echo = echo
        self.__repositories_connected = self.__configure_repositories(
            option, self.__echo
        )
        self.__timestamp = timestamp
        self.__agent_event_id = agent_event_id
        self.__option = option

    def __define_endpoint(self, option):
        options_dict = {
            "agent_event": "agents/history",
            "agent_pause": "pauses",
            "agent_summary": "agents",
            "agent": "agents",
            "all": "all",
            "call_rating": "calls",
            "call": "calls",
            "chat_message": "chats",
            "chat": "chats",
            "queue_summary": "queues",
            "queue": "queues",
        }
        try:
            return options_dict[option]
        except KeyError as exc:
            raise SystemExit(
                f"\n{bcolors.FAIL}Failed to identify which column to syncronize.\n\n{bcolors.WARNING}OptionError: {option}\n"
            ) from exc

    def __configure_repositories(self, options, echo):
        repository_dictionary = {
            "agent_event": AgentEventRepository(self.__string_connection, echo),
            "agent_pause": AgentPauseRepository(self.__string_connection, echo),
            "agent_summary": AgentSummaryRepository(self.__string_connection, echo),
            "agent": AgentsRepository(self.__string_connection, echo),
            "call_rating": CallRatingRepository(self.__string_connection, echo),
            "call": CallRepository(self.__string_connection, echo),
            "chat_message": ChatMessageRepository(self.__string_connection, echo),
            "chat": ChatRepository(self.__string_connection, echo),
            "profiler": ProfilerRepository(self.__string_connection, echo),
            "queue_summary": QueueSummaryRepository(self.__string_connection, echo),
            "queue": QueueRepository(self.__string_connection, echo),
            "tree": TreeRepository(self.__string_connection, echo),
        }

        if options == "all":
            return repository_dictionary

        if options == "call":
            return {
                "call_rating": CallRatingRepository(self.__string_connection, echo),
                "call": CallRepository(self.__string_connection, echo),
                "profiler": ProfilerRepository(self.__string_connection, echo),
                "tree": TreeRepository(self.__string_connection, echo),
            }
        if options == "chat":
            return {
                "chat_message": ChatMessageRepository(self.__string_connection, echo),
                "chat": ChatRepository(self.__string_connection, echo),
                "profiler": ProfilerRepository(self.__string_connection, echo),
                "tree": TreeRepository(self.__string_connection, echo),
            }
        return {f"{options}": repository_dictionary[f"{options}"]}

    def syncronize(self):
        request = Request(self.__endpoint, UserConfigs(self.__token))

        connected_repositories = self.__repositories_connected

        match self.__option:
            case "agent":
                return asyncio.run(sync_agent(request, connected_repositories))

            case "agent_event":
                return asyncio.run(
                    sync_agent_event(
                        request,
                        connected_repositories,
                        self.__agent_event_id,
                    )
                )

            case "agent_pause":
                return asyncio.run(
                    sync_agent_pause(request, connected_repositories, self.__timestamp)
                )

            case "agent_summary":
                return asyncio.run(
                    sync_agent_summary(
                        request, connected_repositories, self.__timestamp
                    )
                )

            case "call":
                return asyncio.run(
                    sync_call(request, connected_repositories, self.__timestamp)
                )

            case "chat":
                return asyncio.run(
                    sync_chat(request, connected_repositories, self.__timestamp)
                )

            case "queue":
                return asyncio.run(sync_queue(request, connected_repositories))

            case "queue_summary":
                return asyncio.run(
                    sync_queue_summary(
                        request, connected_repositories, self.__timestamp
                    )
                )

            case _:
                return (
                    asyncio.run(
                        sync_agent_event(
                            Request("agents/history", UserConfigs(self.__token)),
                            connected_repositories,
                            self.__agent_event_id,
                        )
                    ),
                    asyncio.run(
                        sync_call(
                            Request("calls", UserConfigs(self.__token)),
                            connected_repositories,
                            self.__timestamp,
                        )
                    ),
                    asyncio.run(
                        sync_agent(
                            Request("agents", UserConfigs(self.__token)),
                            connected_repositories,
                        )
                    ),
                    asyncio.run(
                        sync_agent_pause(
                            Request("pauses", UserConfigs(self.__token)),
                            connected_repositories,
                            self.__timestamp,
                        )
                    ),
                    asyncio.run(
                        sync_agent_summary(
                            Request("agents", UserConfigs(self.__token)),
                            connected_repositories,
                            self.__timestamp,
                        )
                    ),
                    asyncio.run(
                        sync_chat(
                            Request("chats", UserConfigs(self.__token)),
                            connected_repositories,
                            self.__timestamp,
                        )
                    ),
                    asyncio.run(
                        sync_queue(
                            Request("queues", UserConfigs(self.__token)),
                            connected_repositories,
                        )
                    ),
                    asyncio.run(
                        sync_queue_summary(
                            Request("queues", UserConfigs(self.__token)),
                            connected_repositories,
                            self.__timestamp,
                        )
                    ),
                )
