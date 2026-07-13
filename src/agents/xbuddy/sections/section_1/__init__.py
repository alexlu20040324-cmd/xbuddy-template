"""Section 1 — Target Role: identify the job the user wants and why."""

from ...enums import SectionID
from ..base_prompt import SectionTemplate, ValidationRule

SECTION_1_TEMPLATE = SectionTemplate(
    section_id=SectionID.TARGET_ROLE,
    name="Target Role",
    description="Identify the job title the user wants, why they want it, and their work preferences.",
    system_prompt_template="""
You are JobBuddy, a friendly AI career coach.

In this section, gather the following from the user:
1. Job title they are targeting (e.g. "Data Analyst", "Backend Engineer")
2. Why they want this role (motivation)
3. Work type preference: full-time, internship, contract, etc.
4. Location preference: remote, specific city/country, etc.

Guidelines:
- Ask one question at a time
- Be warm and encouraging
- Once you have all four, present a summary and ask if it's correct
""",
    validation_rules=[
        ValidationRule(
            field_name="job_title",
            rule_type="required",
            value=True,
            error_message="Please tell me the job title you're targeting.",
        ),
    ],
    required_fields=["job_title", "job_motivation"],
    next_section=SectionID.BACKGROUND,
)
