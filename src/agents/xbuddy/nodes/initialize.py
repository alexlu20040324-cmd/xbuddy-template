"""Initialize node — validates and sets up conversation state."""

import logging
from langchain_core.runnables import RunnableConfig

from ..models import XBuddyState
from ..enums import SectionID, RouterDirective

logger = logging.getLogger(__name__)


async def initialize_node(state: XBuddyState, config: RunnableConfig) -> XBuddyState:
    """Initialize conversation state at the start of every invocation.

    1. Sets user_id and thread_id from config if not already in state
    2. Sets default values for current_section and router_directive
    3. Logs the initialization
    """
    configurable = config.get("configurable", {})

    # Set user_id from config if not already set
    user_id = state.get("user_id") or configurable.get("user_id", 1)

    # Set thread_id from config if not already set
    thread_id = state.get("thread_id") or configurable.get("thread_id", state["thread_id"])

    # Set default section and router directive if not already set
    current_section = state.get("current_section") or SectionID.SECTION_1
    router_directive = state.get("router_directive") or RouterDirective.NEXT

    logger.info(
        "Initializing XBuddy state | user_id=%s thread_id=%s section=%s",
        user_id,
        thread_id,
        current_section,
    )

    return {
        "user_id": user_id,
        "thread_id": thread_id,
        "current_section": current_section,
        "router_directive": router_directive,
    }