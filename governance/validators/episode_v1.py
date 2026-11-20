from pathlib import Path

from governance_tools.validator_interface import DomainValidator, ValidatorResult
from story2video.domain.episode import EpisodeManifest

RULE_ID = "story2video-episode-v1"


class EpisodeV1Validator(DomainValidator):
    @property
    def rule_ids(self) -> list[str]:
        return [RULE_ID]

    def validate(self, payload: dict) -> ValidatorResult:
        checks = payload.get("checks", {})
        manifest = checks.get("episode_manifest") if isinstance(checks, dict) else None
        if not isinstance(manifest, str) or not manifest.strip():
            return ValidatorResult(
                ok=False, rule_ids=self.rule_ids, violations=["episode_manifest evidence is required"]
            )
        try:
            episode = EpisodeManifest.read(Path(manifest))
        except (OSError, ValueError) as error:
            return ValidatorResult(ok=False, rule_ids=self.rule_ids, violations=[str(error)])
        return ValidatorResult(
            ok=True,
            rule_ids=self.rule_ids,
            evidence_summary="Episode v1 manifest passed structural validation",
            metadata={"episode_id": episode.episode_id, "input_hash": episode.input_hash},
        )
