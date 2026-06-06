"""Section prompts and navigation helpers."""

from .enums import SectionID
from .sections.base_prompt import SectionTemplate
from .sections.section_1 import SECTION_1_TEMPLATE
from .sections.section_2 import SECTION_2_TEMPLATE
from .sections.section_3 import SECTION_3_TEMPLATE
from .sections.section_4 import SECTION_4_TEMPLATE
from .sections.section_5 import SECTION_5_TEMPLATE

SECTION_TEMPLATE_MAP = {
    SectionID.COURSE_INFO: SECTION_1_TEMPLATE,
    SectionID.MATERIALS: SECTION_2_TEMPLATE,
    SectionID.KNOWLEDGE_CHECK: SECTION_3_TEMPLATE,
    SectionID.SCHEDULE: SECTION_4_TEMPLATE,
    SectionID.STUDY_PLAN: SECTION_5_TEMPLATE,
}


def get_section_template(section_id: SectionID) -> SectionTemplate:
    """Return the template for a given section."""
    template = SECTION_TEMPLATE_MAP.get(section_id)
    if not template:
        raise ValueError(f"No template found for section: {section_id}")
    return template


def get_next_section(current: SectionID) -> SectionID | None:
    """Return the next section in sequence, or None if all complete."""
    order = list(SectionID)
    idx = order.index(current)
    if idx + 1 < len(order):
        return order[idx + 1]
    return None


def get_next_unfinished_section(section_states: dict) -> SectionID | None:
    """Find the first section that isn't done yet."""
    for section_id in SectionID:
        state = section_states.get(section_id.value)
        if not state or state.status != "done":
            return section_id
    return None