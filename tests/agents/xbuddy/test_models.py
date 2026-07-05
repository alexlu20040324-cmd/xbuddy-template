"""Tests for JobBuddy's XBuddyData and XBuddyState models (PR 1)."""

from src.agents.xbuddy.enums import SectionID
from src.agents.xbuddy.models import XBuddyData, XBuddyState


def test_xbuddy_data_defaults():
    """A freshly created XBuddyData should have safe, empty defaults."""
    data = XBuddyData()

    # Section 1 — TARGET_ROLE
    assert data.job_title is None
    assert data.work_type is None

    # Section 2 — BACKGROUND
    assert data.education is None
    assert data.skills == []
    assert data.projects == []

    # Section 3 — GAP_ANALYSIS
    assert data.skills_match == []
    assert data.skills_missing == []
    assert data.gap_confirmed is False

    # Section 4 — CONSTRAINTS
    assert data.timeline_months is None
    assert data.weekly_hours is None

    # Section 5 — RESUME_TIPS
    assert data.has_resume is None


def test_xbuddy_data_accepts_real_values():
    """XBuddyData should store real values once the user provides them."""
    data = XBuddyData(
        job_title="AI Engineer",
        work_type="full-time",
        skills=["Python", "Pandas"],
        skills_missing=["LangGraph"],
        gap_confirmed=True,
        timeline_months=3,
        weekly_hours=15.0,
        has_resume=True,
    )

    assert data.job_title == "AI Engineer"
    assert data.skills == ["Python", "Pandas"]
    assert data.skills_missing == ["LangGraph"]
    assert data.gap_confirmed is True
    assert data.timeline_months == 3
    assert data.has_resume is True


def test_xbuddy_state_defaults_to_target_role_section():
    """A freshly created XBuddyState should start at the TARGET_ROLE section."""
    state = XBuddyState()

    assert state.current_section == SectionID.TARGET_ROLE
    assert state.finished is False
    assert isinstance(state.user_data, XBuddyData)


def test_section_id_has_five_jobbuddy_sections():
    """SectionID should define exactly JobBuddy's 5 domain sections."""
    expected = {
        "target_role",
        "background",
        "gap_analysis",
        "constraints",
        "resume_tips",
    }
    actual = {member.value for member in SectionID}

    assert actual == expected
