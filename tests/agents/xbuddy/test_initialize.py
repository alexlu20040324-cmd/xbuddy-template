"""Tests for initialize_node (PR 1)."""

import pytest

from agents.xbuddy.enums import RouterDirective, SectionID
from agents.xbuddy.models import XBuddyState
from agents.xbuddy.nodes.initialize import initialize_node


@pytest.mark.asyncio
async def test_initialize_node_sets_defaults_for_new_conversation():
    """A brand-new state should be initialized to TARGET_ROLE with NEXT directive."""
    state = XBuddyState()
    config = {"configurable": {}}

    result = await initialize_node(state, config)

    assert result["current_section"] == SectionID.TARGET_ROLE
    assert result["router_directive"] == RouterDirective.NEXT
    assert result["user_id"] == 1
    assert result["thread_id"] == state.thread_id


@pytest.mark.asyncio
async def test_initialize_node_uses_config_user_id_when_state_has_none():
    """If config provides a user_id, initialize_node should use it."""
    state = XBuddyState()
    config = {"configurable": {"user_id": 42}}

    result = await initialize_node(state, config)

    assert result["user_id"] == 42


@pytest.mark.asyncio
async def test_initialize_node_preserves_existing_section():
    """If the conversation already has a current_section, don't reset it."""
    state = XBuddyState(current_section=SectionID.GAP_ANALYSIS)
    config = {"configurable": {}}

    result = await initialize_node(state, config)

    assert result["current_section"] == SectionID.GAP_ANALYSIS
