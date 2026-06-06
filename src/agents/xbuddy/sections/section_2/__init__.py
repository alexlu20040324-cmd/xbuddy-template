"""Section 2 — Materials: inventory the student's available study resources."""

from ...enums import SectionID
from ..base_prompt import SectionTemplate, ValidationRule

SECTION_2_TEMPLATE = SectionTemplate(
    section_id=SectionID.MATERIALS,
    name="Materials",
    description="Inventory available study materials the student has access to.",
    system_prompt_template="""
You are StudentBuddy, a friendly AI exam prep coach.

In this section, find out what study materials the student has available:
1. Lecture notes or slides
2. Assignments or past tests
3. Required textbook
4. Any other resources

Guidelines:
- Ask one question at a time
- Be encouraging — even one resource is enough to work with
- Once you have the list, present a summary and ask if it's correct
""",
    validation_rules=[
        ValidationRule(
            field_name="materials",
            rule_type="required",
            value=True,
            error_message="Please list at least one study material.",
        ),
    ],
    required_fields=["materials"],
    next_section=SectionID.KNOWLEDGE_CHECK,
)