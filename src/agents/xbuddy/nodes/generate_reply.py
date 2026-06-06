"""Generate reply node — creates conversational responses using the LLM."""

import logging
from langchain_core.messages import SystemMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI

from ..models import XBuddyState

logger = logging.getLogger(__name__)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)


async def generate_reply_node(state: XBuddyState, config: RunnableConfig) -> XBuddyState:
    """Generate a conversational reply for the current section."""
    context_packet = state.get("context_packet")
    if not context_packet:
        logger.warning("No context_packet found, skipping reply generation.")
        return {}

    # Build message history
    system_message = SystemMessage(content=context_packet.system_prompt)
    short_memory = state.get("short_memory", [])
    messages = [system_message] + short_memory

    logger.info("Generating reply for section: %s", context_packet.section_id)

    # Call the LLM
    response = await llm.ainvoke(messages, config=config)
    ai_message = AIMessage(content=response.content)

    # Update short memory with the new AI message
    updated_memory = short_memory + [ai_message]

    return {
        "messages": [ai_message],
        "short_memory": updated_memory,
        "awaiting_user_input": True,
    }