"""Generate decision node — analyzes the conversation and decides next action."""

import logging
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI

from ..models import XBuddyState, ChatAgentDecision
from ..enums import RouterDirective

logger = logging.getLogger(__name__)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


DECISION_PROMPT = """You are analyzing a conversation to decide what to do next.

Based on the latest exchange, decide:
1. router_directive: 
   - "stay" — the current section is not complete yet, keep asking
   - "next" — the user has provided all required info, move to next section
   - "modify:<section_id>" — the user wants to change a previous section
2. is_satisfied: whether the user expressed satisfaction with the current section
3. should_save_content: whether to save the current section's content
4. user_satisfaction_feedback: any feedback the user gave

Respond in JSON format matching the ChatAgentDecision schema.
"""


async def generate_decision_node(state: XBuddyState, config: RunnableConfig) -> XBuddyState:
    """Analyze conversation and produce a structured decision."""
    context_packet = state.get("context_packet")
    short_memory = state.get("short_memory", [])

    if not context_packet or not short_memory:
        return {"router_directive": RouterDirective.STAY}

    # Build messages for decision
    messages = [
        SystemMessage(content=DECISION_PROMPT),
        HumanMessage(content=f"Current section: {context_packet.section_id}\n\nConversation so far:\n" +
                     "\n".join([f"{m.type}: {m.content}" for m in short_memory[-4:]])),
    ]

    logger.info("Generating decision for section: %s", context_packet.section_id)

    # Call LLM with structured output
    structured_llm = llm.with_structured_output(ChatAgentDecision)
    decision: ChatAgentDecision = await structured_llm.ainvoke(messages, config=config)

    logger.info("Decision: %s", decision)

    return {
        "router_directive": decision.router_directive,
        "awaiting_user_input": False,
        "awaiting_satisfaction_feedback": not decision.is_satisfied if decision.is_satisfied is not None else False,
        "agent_output": decision,
    }