from enum import StrEnum


class State(StrEnum):
    DRAFT = "DRAFT"
    VALIDATING = "VALIDATING"
    REJECTED = "REJECTED"
    VALIDATED = "VALIDATED"
    ASSET_GENERATING = "ASSET_GENERATING"
    FAILED_RETRYABLE = "FAILED_RETRYABLE"
    ASSET_READY = "ASSET_READY"
    RENDERING = "RENDERING"
    RENDERED = "RENDERED"
    QA_RUNNING = "QA_RUNNING"
    QA_FAILED = "QA_FAILED"
    QA_PASSED = "QA_PASSED"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    APPROVED = "APPROVED"
    UPLOADING_PRIVATE = "UPLOADING_PRIVATE"
    UPLOADED_PRIVATE = "UPLOADED_PRIVATE"
    PUBLISH_APPROVED = "PUBLISH_APPROVED"
    PUBLISHED = "PUBLISHED"
    ANALYZED = "ANALYZED"


TRANSITIONS = {
    State.DRAFT: {State.VALIDATING},
    State.VALIDATING: {State.REJECTED, State.VALIDATED},
    State.REJECTED: {State.DRAFT},
    State.VALIDATED: {State.ASSET_GENERATING},
    State.ASSET_GENERATING: {State.FAILED_RETRYABLE, State.ASSET_READY},
    State.FAILED_RETRYABLE: set(),
    State.ASSET_READY: {State.RENDERING},
    State.RENDERING: {State.FAILED_RETRYABLE, State.RENDERED},
    State.RENDERED: {State.QA_RUNNING},
    State.QA_RUNNING: {State.QA_FAILED, State.QA_PASSED},
    State.QA_FAILED: {State.DRAFT},
    State.QA_PASSED: {State.AWAITING_APPROVAL},
    State.AWAITING_APPROVAL: {State.REJECTED, State.APPROVED},
    State.APPROVED: {State.UPLOADING_PRIVATE},
    State.UPLOADING_PRIVATE: {State.FAILED_RETRYABLE, State.UPLOADED_PRIVATE},
    State.UPLOADED_PRIVATE: {State.PUBLISH_APPROVED},
    State.PUBLISH_APPROVED: {State.PUBLISHED},
    State.PUBLISHED: {State.ANALYZED},
    State.ANALYZED: set(),
}

RETRYABLE_STAGES = {
    state for state, targets in TRANSITIONS.items() if State.FAILED_RETRYABLE in targets
}


def require_transition(
    current: State, target: State, *, failed_stage: State | None = None
) -> None:
    if current == State.FAILED_RETRYABLE:
        if target in RETRYABLE_STAGES and target == failed_stage:
            return
    elif target in TRANSITIONS[current]:
        return
    raise ValueError(f"Illegal state transition: {current} -> {target}")
