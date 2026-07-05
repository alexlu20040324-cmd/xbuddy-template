"""Enumerations for your XBuddy Agent."""

from enum import Enum


class SectionStatus(str, Enum):
    """Status of an agent section."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class RouterDirective(str, Enum):
    """Router directive for navigation control."""
    STAY = "stay"
    NEXT = "next"
    MODIFY = "modify"  # Format: "modify:section_id"
    

class SectionID(str, Enum):
    TARGET_ROLE = "target_role"
    BACKGROUND = "background"
    GAP_ANALYSIS = "gap_analysis"
    CONSTRAINTS = "constraints"
    RESUME_TIPS = "resume_tips"
