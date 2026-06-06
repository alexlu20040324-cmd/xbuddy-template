"""Memory updater node — persists section state and manages completion."""

import logging
from langchain_core.runnables import RunnableConfig

from ..models import XBuddyState, SectionState, SectionContent
from ..enums import SectionID, SectionStatus, RouterDirective

logger = logging.getLogger(__name__)


async def memory_updater_node(state: XBuddyState, config: RunnableConfig) -> XBuddyState:
    """Update section state, persist data, check completion."""
    agent_output = state.get("agent_output")
    current_section = state.get("current_section")
    section_states = dict(state.get("section_states", {}))

    if not agent_output or not current_section:
        return {"router_directive": RouterDirective.STAY}

    # Get or create section state
    section_state = section_states.get(current_section.value) or SectionState(
        section_id=current_section,
        status=SectionStatus.IN_PROGRESS,
    )

    # Save content if decision says so
    if agent_output.should_save_content:
        short_memory = state.get("short_memory", [])
        content_text = "\n".join([
            f"{m.type}: {m.content}"
            for m in short_memory
        ])
        section_state = SectionState(
            section_id=current_section,
            status=SectionStatus.DONE,
            content=SectionContent(
                content={"text": content_text},
                plain_text=content_text,
            ),
            satisfaction_status="satisfied" if agent_output.is_satisfied else "needs_improvement",
        )
        logger.info("Saved content for section: %s", current_section)

    # Update section states
    section_states[current_section.value] = section_state

    # Check if all sections except STUDY_PLAN are done
    all_done = all(
        section_states.get(s.value, SectionState(section_id=s)).status == SectionStatus.DONE
        for s in SectionID
        if s != SectionID.STUDY_PLAN
    )

    should_generate_final = all_done and agent_output.router_directive == RouterDirective.NEXT

    logger.info(
        "Memory updated | section=%s directive=%s all_done=%s",
        current_section,
        agent_output.router_directive,
        all_done,
    )

    return {
        "section_states": section_states,
        "router_directive": agent_output.router_directive,
        "should_generate_final_output": should_generate_final,
        "short_memory": state.get("short_memory", []),
    }