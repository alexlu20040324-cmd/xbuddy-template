"""Router node — handles section navigation and context loading."""

import logging
from langchain_core.runnables import RunnableConfig

from ..models import XBuddyState, ContextPacket, SectionState
from ..enums import SectionID, RouterDirective, SectionStatus
from ..sections.base_prompt import BASE_RULES
from ..sections.section_1 import SECTION_1_TEMPLATE
from ..sections.section_2 import SECTION_2_TEMPLATE
from ..sections.section_3 import SECTION_3_TEMPLATE
from ..sections.section_4 import SECTION_4_TEMPLATE
from ..sections.section_5 import SECTION_5_TEMPLATE

logger = logging.getLogger(__name__)

SECTION_TEMPLATES = {
    SectionID.COURSE_INFO: SECTION_1_TEMPLATE,
    SectionID.MATERIALS: SECTION_2_TEMPLATE,
    SectionID.KNOWLEDGE_CHECK: SECTION_3_TEMPLATE,
    SectionID.SCHEDULE: SECTION_4_TEMPLATE,
    SectionID.STUDY_PLAN: SECTION_5_TEMPLATE,
}


async def router_node(state: XBuddyState, config: RunnableConfig) -> XBuddyState:
    """Route to the correct section and load context."""
    directive = state.get("router_directive", RouterDirective.NEXT)
    current_section = state.get("current_section", SectionID.COURSE_INFO)
    section_states = state.get("section_states", {})

    # Handle NEXT directive — move to next section
    if directive == RouterDirective.NEXT:
        template = SECTION_TEMPLATES.get(current_section)
        if template and template.next_section:
            current_section = template.next_section
            logger.info("Moving to next section: %s", current_section)

    # Handle MODIFY directive — jump to a specific section
    elif isinstance(directive, str) and directive.startswith("modify:"):
        target = directive.split(":", 1)[1]
        try:
            current_section = SectionID(target)
            logger.info("Jumping to section: %s", current_section)
        except ValueError:
            logger.warning("Invalid section id in modify directive: %s", target)

    # Load the template for the current section
    template = SECTION_TEMPLATES.get(current_section)
    if not template:
        logger.error("No template found for section: %s", current_section)
        return {"finished": True}

    # Build system prompt
    system_prompt = BASE_RULES + "\n\n" + template.system_prompt_template

    # Get or create section state
    section_state = section_states.get(current_section.value) or SectionState(
        section_id=current_section,
        status=SectionStatus.IN_PROGRESS,
    )

    # Build context packet
    context_packet = ContextPacket(
        section_id=current_section,
        status=section_state.status,
        system_prompt=system_prompt,
        draft=section_state.content,
        validation_rules={"rules": [r.model_dump() for r in template.validation_rules]},
    )

    # Check if all sections are done
    all_done = all(
        section_states.get(s.value, SectionState(section_id=s)).status == SectionStatus.DONE
        for s in SectionID
        if s != SectionID.STUDY_PLAN
    )

    logger.info("Router: section=%s directive=%s", current_section, directive)

    return {
        "current_section": current_section,
        "context_packet": context_packet,
        "router_directive": RouterDirective.STAY,
        "finished": all_done,
    }