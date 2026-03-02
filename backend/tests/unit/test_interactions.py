"""Unit tests for interaction filtering logic."""

from app.models.interaction import InteractionLog
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


def test_filter_returns_all_when_item_id_is_none() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, None)
    assert result == interactions


def test_filter_returns_empty_for_empty_input() -> None:
    result = _filter_by_item_id([], 1)
    assert result == []


def test_filter_returns_interaction_with_matching_ids() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].id == 1

def test_filter_excludes_interaction_with_different_learner_id() -> None:
    # interaction with item_id=1 and learner_id=2
    interactions = [_make_log(1, 2, 1), _make_log(2, 1, 2)]
    
    result = _filter_by_item_id(interactions, 1)
    
    # The interaction with item_id=1 should be included, 
    # regardless of its learner_id.
    assert len(result) == 1
    assert result[0].id == 1


def test_filter_returns_empty_when_no_items_match() -> None:
    # Edge case: The list is not empty, but the target item_id does not exist in the list.
    interactions = [_make_log(1, 1, 2), _make_log(2, 2, 3)]
    result = _filter_by_item_id(interactions, 99)
    assert result == []


def test_filter_returns_multiple_matching_interactions() -> None:
    # Boundary case: Multiple interactions share the same item_id. 
    # Ensures the filter doesn't just stop at the first match.
    interactions = [
        _make_log(1, 1, 1),
        _make_log(2, 2, 99),
        _make_log(3, 3, 1)
    ]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 3


def test_filter_returns_all_when_all_match() -> None:
    # Boundary case: Every interaction in the list matches the target item_id.
    interactions = [_make_log(1, 1, 5), _make_log(2, 2, 5)]
    result = _filter_by_item_id(interactions, 5)
    assert result == interactions


def test_filter_handles_zero_item_id_correctly() -> None:
    # Edge case: 0 is a "falsy" value in Python. 
    # This ensures the logic uses `item_id is not None` rather than `if item_id:`
    # which would incorrectly return all logs when item_id=0.
    interactions = [_make_log(1, 1, 0), _make_log(2, 2, 1)]
    result = _filter_by_item_id(interactions, 0)
    assert len(result) == 1
    assert result[0].id == 1
    assert result[0].item_id == 0


def test_filter_handles_negative_item_id() -> None:
    # Boundary value: item_id is a negative number.
    # While IDs are usually positive, testing a negative ensures strict equality checks are used.
    interactions = [_make_log(1, 1, -5), _make_log(2, 2, 5)]
    result = _filter_by_item_id(interactions, -5)
    assert len(result) == 1
    assert result[0].id == 1
    assert result[0].item_id == -5

