"""Section 4 — Schedule: exam date and available study hours."""

from ...enums import SectionID
from ..base_prompt import SectionTemplate, ValidationRule

SECTION_4_TEMPLATE = SectionTemplate(
    section_id=SectionID.SCHEDULE,
    name="Schedule",
    description="Find out the exam date and how many hours per day the student can study.",
    system_prompt_template="""
You are StudentBuddy, a friendly AI exam prep coach.

In this section, gather the student's schedule information:
1. Exam date (or how many days until the exam)
2. How many hours per day they can dedicate to studying

Guidelines:
- Ask one question at a time
- Be encouraging — even 1 hour a day is something to work with
- Once you have both answers, present a summary and ask if it's correct
""",
    validation_rules=[
        ValidationRule(
            field_name="exam_date",
            rule_type="required",
            value=True,
            error_message="Please provide your exam date or days remaining.",
        ),
        ValidationRule(
            field_name="daily_hours",
            rule_type="required",
            value=True,
            error_message="Please provide how many hours per day you can study.",
        ),
    ],
    required_fields=["exam_date", "daily_hours"],
    next_section=SectionID.STUDY_PLAN,
)
