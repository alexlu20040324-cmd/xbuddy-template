"""Section 3 — Knowledge Check: self-assessed mastery level."""

from ...enums import SectionID
from ..base_prompt import SectionTemplate, ValidationRule

SECTION_3_TEMPLATE = SectionTemplate(
    section_id=SectionID.KNOWLEDGE_CHECK,
    name="Knowledge Check",
    description="Assess the student's self-rated mastery level for the course.",
    system_prompt_template="""
You are StudentBuddy, a friendly AI exam prep coach.

In this section, ask the student to rate their current understanding:
1. Overall mastery level (1-10 scale)
2. Which topics they feel weakest on
3. Which topics they feel most confident about

Guidelines:
- Ask one question at a time
- Be non-judgmental — any score is valid
- Once you have all answers, present a summary and ask if it's correct
""",
    validation_rules=[
        ValidationRule(
            field_name="mastery_level",
            rule_type="required",
            value=True,
            error_message="Please provide a mastery level between 1 and 10.",
        ),
    ],
    required_fields=["mastery_level", "weak_topics"],
    next_section=SectionID.SCHEDULE,
)