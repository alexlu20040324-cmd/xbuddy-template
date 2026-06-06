"""Section 1 — Course Info: gather university, course name, and course code."""

from ...enums import SectionID
from ..base_prompt import SectionTemplate, ValidationRule

SECTION_1_TEMPLATE = SectionTemplate(
    section_id=SectionID.COURSE_INFO,
    name="Course Info",
    description="Identify the course the student is preparing for.",
    system_prompt_template="""
You are StudentBuddy, a friendly AI exam prep coach.

In this section, gather the following from the student:
1. University name
2. Course name
3. Course code (e.g. CS101)

Guidelines:
- Ask one question at a time
- Be warm and encouraging
- Once you have all three, present a summary and ask if it's correct
""",
    validation_rules=[
        ValidationRule(
            field_name="university",
            rule_type="required",
            value=True,
            error_message="Please provide your university name.",
        ),
        ValidationRule(
            field_name="course_name",
            rule_type="required",
            value=True,
            error_message="Please provide your course name.",
        ),
    ],
    required_fields=["university", "course_name", "course_code"],
    next_section=SectionID.MATERIALS,
)