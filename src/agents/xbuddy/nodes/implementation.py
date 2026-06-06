"""Implementation node — generates the final study plan when all sections are complete."""

import logging
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI

from ..models import XBuddyState
from ..enums import SectionID

logger = logging.getLogger(__name__)

llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

STUDY_PLAN_PROMPT = """You are StudentBuddy, an expert AI exam prep coach.

Based on all the information collected from the student, generate a comprehensive, 
personalized day-by-day study plan.

The plan must include:
1. An urgency summary (e.g. "You have 3 days and rated yourself 4/10 — focus on X first")
2. A day-by-day schedule covering all remaining days before the exam
3. Which specific materials to use each day
4. Practice problem recommendations based on available resources
5. Tips for weak areas identified by the student

Format the plan clearly with headers for each day.
Be specific, actionable, and encouraging.
"""


async def implementation_node(state: XBuddyState, config: RunnableConfig) -> XBuddyState:
    """Generate the final study plan artifact."""
    section_states = state.get("section_states", {})

    # Gather all section content
    collected_info = []
    for section_id in SectionID:
        section_state = section_states.get(section_id.value)
        if section_state and section_state.content:
            collected_info.append(
                f"=== {section_id.value.upper()} ===\n{section_state.content.plain_text}"
            )

    if not collected_info:
        logger.warning("No section data found, cannot generate study plan.")
        return {"finished": True}

    # Build the prompt
    all_info = "\n\n".join(collected_info)
    messages = [
        SystemMessage(content=STUDY_PLAN_PROMPT),
        HumanMessage(content=f"Here is all the information collected from the student:\n\n{all_info}\n\nPlease generate the personalized study plan now."),
    ]

    logger.info("Generating final study plan...")

    # Call the LLM
    response = await llm.ainvoke(messages, config=config)
    study_plan = response.content

    logger.info("Study plan generated successfully.")

    return {
        "final_output": study_plan,
        "finished": True,
        "messages": [AIMessage(content=study_plan)],
    }