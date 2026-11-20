import pytest

from story2video.domain.states import RETRYABLE_STAGES, State, require_transition


@pytest.mark.parametrize("current", sorted(set(State) - {State.PUBLISH_APPROVED}))
def test_only_publish_approval_can_lead_to_published(current):
    with pytest.raises(ValueError, match="Illegal state transition"):
        require_transition(current, State.PUBLISHED)


@pytest.mark.parametrize("stage", sorted(RETRYABLE_STAGES))
def test_retry_returns_to_the_recorded_stage(stage):
    require_transition(stage, State.FAILED_RETRYABLE)
    require_transition(State.FAILED_RETRYABLE, stage, failed_stage=stage)
    for other in RETRYABLE_STAGES - {stage}:
        with pytest.raises(ValueError, match="Illegal state transition"):
            require_transition(State.FAILED_RETRYABLE, other, failed_stage=stage)


@pytest.mark.parametrize("current", [State.REJECTED, State.QA_FAILED])
def test_rejected_episode_must_restart_validation(current):
    require_transition(current, State.DRAFT)
    with pytest.raises(ValueError, match="Illegal state transition"):
        require_transition(current, State.VALIDATED)


def test_failed_stage_is_required_for_retry():
    with pytest.raises(ValueError, match="Illegal state transition"):
        require_transition(State.FAILED_RETRYABLE, State.RENDERING)
