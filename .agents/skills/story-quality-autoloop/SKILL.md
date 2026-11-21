---
name: story-quality-autoloop
description: Run the story2video editorial loop when asked to revise, blind-test, score, or select original Shorts stories. Coordinate a Writer and isolated staged readers, keep versioned evidence, and report only stories that pass the production-candidate gate.
---

# Story Quality AutoLoop

Read the repository's AGENTS.md, PLAN.md, and the current story cards and reviews. This workflow covers the editorial experiment in Issue #6. A passing result marks a story for the user's production decision. Stop before production, publishing, or merging.

1. Use the user's story order, with 10 → 03 → 07 for the first Issue #6 run. Use one evidence directory per batch and reuse it across retries. If the user asks to continue past a batch, record its outcome and start the next one with new revisions or different stories. Keep the same limits per batch and preserve earlier evidence.
2. Delegate revisions to a native Writer subagent. Provide the current card, reveal, English narration, and an anonymized description of the defect. Keep prior scores and reader identities out of the prompt. Request both Traditional Chinese card sections, the reveal, the complete English narration, the required core answers, and one testable change. The Writer does not score. Save the proposal and its parent version under a fresh draft ID.
3. Run the [local harness](references/run.md). It checks the isolated Codex CLI profile with an outside-workspace canary before tests, sends only staged content, and computes the decision from saved records. Native desktop subagents can write, but sharing their worktree means their reads are diagnostic only. Treat incomplete or unverified sessions as invalid.
4. If three independent readers of the same frozen draft each score at least 90 and every required core is supported without a blocking content defect, stop revising that story. If readers repeatedly flag the same design problem, change the design or move to the next story. Use at most four revisions total, two per story, and twelve reader sessions total. Retries consume reader slots and start fresh. Do not lower the gate or switch evidence directories to bypass limits.
5. Keep failed versions, prompts, raw replies, iteration counts and decision evidence. Update review materials or a PR when authorized. In the user-facing story list, include only versions that passed, or say that no story qualified.
