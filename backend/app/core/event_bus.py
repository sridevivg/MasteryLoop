import asyncio
import logging
from datetime import datetime, timezone
from enum import Enum
from typing import Callable, Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class EventType(str, Enum):
    TEST_STARTED = "TEST_STARTED"
    QUESTION_ANSWERED = "QUESTION_ANSWERED"
    MASTERY_UPDATED = "MASTERY_UPDATED"
    TEST_COMPLETED = "TEST_COMPLETED"
    WEAKNESS_DETECTED = "WEAKNESS_DETECTED"
    RESOURCE_RECOMMENDED = "RESOURCE_RECOMMENDED"
    PRACTICE_COMPLETED = "PRACTICE_COMPLETED"
    RETENTION_REVIEW_DUE = "RETENTION_REVIEW_DUE"
    CHALLENGE_COMPLETED = "CHALLENGE_COMPLETED"
    CODE_SUBMITTED = "CODE_SUBMITTED"
    QUESTION_REVIEWED = "QUESTION_REVIEWED"


class Event:
    def __init__(
        self,
        event_type: EventType,
        payload: Dict[str, Any],
        user_id: Optional[str] = None,
        event_id: Optional[str] = None
    ):
        self.event_type = event_type
        self.payload = payload
        self.user_id = user_id
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.event_id = event_id or f"{event_type.value}_{datetime.now(timezone.utc).timestamp()}"


class EventBus:
    def __init__(self):
        self._subscribers: Dict[EventType, List[Callable[[Event], Any]]] = {
            evt: [] for evt in EventType
        }
        self._processed_events = set()

    def subscribe(self, event_type: EventType, handler: Callable[[Event], Any]):
        if handler not in self._subscribers[event_type]:
            self._subscribers[event_type].append(handler)
            logger.debug(f"Subscribed handler {handler.__name__} to {event_type.value}")

    async def publish(self, event: Event):
        # Prevent duplicate processing of the same event id
        if event.event_id in self._processed_events:
            logger.warning(f"Duplicate event ignored: {event.event_id}")
            return
        self._processed_events.add(event.event_id)

        # Evict old events to avoid memory growth
        if len(self._processed_events) > 5000:
            self._processed_events = set(list(self._processed_events)[-2500:])

        handlers = self._subscribers.get(event.event_type, [])
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
            except Exception as e:
                logger.error(f"Error executing event handler {handler.__name__} for {event.event_type.value}: {e}", exc_info=True)


# Global event bus singleton
event_bus = EventBus()
