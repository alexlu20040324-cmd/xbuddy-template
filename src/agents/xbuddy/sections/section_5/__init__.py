"""Section 5 — Study Plan: generate a personalized day-by-day study plan."""

from ...enums import SectionID
from ..base_prompt import SectionTemplate, ValidationRule

SECTION_5_TEMPLATE = SectionTemplate(
    section_id=SectionID.STUDY_PLAN,
    name="Study Plan",
    description="Generate a personalized day-by-day study plan based on all collected information.",
    system_prompt_template="""
You are StudentBuddy, a friendly AI exam prep coach.

In this section, generate a personalized study plan based on everything you've learned:
- Course and topics
- Available materials
- Self-assessed mastery level and weak areas
- Days remaining and daily study hours

The plan should include:
1. A urgency summary (e.g. "You have 3 days and rated yourself 4/10 — focus on X first")
2. A day-by-day schedule covering all remaining days
3. Which materials to use each day
4. Practice problem recommendations

Guidelines:
- Be specific and actionable
- Prioritize weak topics first
- Keep each day's plan realistic given the available hours
""",
    validation_rules=[],
    required_fields=[],
    next_section=None,
)