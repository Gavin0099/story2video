"""Tests for the quality-vs-market join.

Run from this directory:
    python -m unittest test_pipeline -v

Unit tests are self-contained. Integration tests touch the local repo and skip
themselves when the file they need is absent, so the suite still runs on a
checkout without artifacts/.
"""
import csv
import hashlib
import json
import os
import unittest

import build_index
import build_table

HERE = os.path.dirname(os.path.abspath(__file__))

# 04-v7 frozen in PR #7 at commit 063cc51d, and the text its published master
# was built from. Both must hash to this value; the earlier version of this
# analysis reported 04-v7 as NOT_TESTED because it only scanned local artifacts/.
SHA_04_V7 = "6e3e945a06f251cccb44b43a8500bbfe6115831c347bd223681a51db10fbd6a3"


class StoryKey(unittest.TestCase):
    def test_hash_covers_exactly_the_four_frozen_fields(self):
        base = {"first": "a", "second": "b", "reveal": "c", "english": "d"}
        want = hashlib.sha256("a|b|c|d".encode("utf-8")).hexdigest()
        self.assertEqual(build_index.story_sha256(base), want)
        self.assertEqual(build_table.story_sha256(base), want)

    def test_other_fields_do_not_change_the_key(self):
        a = {"first": "x", "second": "y", "reveal": "z", "english": "w"}
        b = dict(a, title="different", parent="abc", cores={"k": "v"})
        self.assertEqual(build_index.story_sha256(a), build_index.story_sha256(b))

    def test_any_text_difference_changes_the_key(self):
        a = {"first": "x", "second": "y", "reveal": "z", "english": "w"}
        b = dict(a, reveal="z ")
        self.assertNotEqual(build_index.story_sha256(a), build_index.story_sha256(b))

    def test_empty_or_non_dict_has_no_key(self):
        self.assertIsNone(build_index.story_sha256({}))
        self.assertIsNone(build_index.story_sha256({"first": "", "second": "",
                                                    "reveal": "", "english": ""}))
        self.assertIsNone(build_index.story_sha256(None))
        self.assertIsNone(build_index.story_sha256("not a dict"))


class GateState(unittest.TestCase):
    """The contract lives in autoloop.py:
        passed = (len(valid) == 3 and all(score >= 90 and clear))
    All three conditions must be reproduced, not just the score."""

    def rec(self, minimum, cores="supported", count=3, clear="yes"):
        return {"reader_min": str(minimum), "cores": cores,
                "reader_count": str(count), "all_readers_clear": clear}

    def test_fewer_than_three_readers_cannot_pass(self):
        self.assertEqual(build_table.gate_state([self.rec(95, count=1)]),
                         "BELOW_GATE")
        self.assertEqual(build_table.gate_state([self.rec(95, count=2)]),
                         "BELOW_GATE")

    def test_more_than_three_readers_cannot_pass(self):
        self.assertEqual(build_table.gate_state([self.rec(95, count=4)]),
                         "BELOW_GATE")

    def test_a_reader_who_did_not_mark_it_clear_blocks_the_pass(self):
        self.assertEqual(build_table.gate_state([self.rec(98, clear="no")]),
                         "BELOW_GATE")

    def test_missing_clear_flag_is_not_silently_treated_as_pass_or_fail(self):
        self.assertEqual(build_table.gate_state([self.rec(95, clear="")]),
                         "CORES_NOT_RECORDED")

    def test_missing_reader_count_is_not_judged(self):
        rec = {"reader_min": "95", "cores": "supported", "all_readers_clear": "yes"}
        self.assertEqual(build_table.gate_state([rec]), "CORES_NOT_RECORDED")

    def test_no_record_is_not_tested_not_a_failure(self):
        self.assertEqual(build_table.gate_state([]), "NOT_TESTED")

    def test_all_readers_at_or_above_ninety_with_supported_cores_passes(self):
        self.assertEqual(build_table.gate_state([self.rec(91)]), "GATE_PASS")
        self.assertEqual(build_table.gate_state([self.rec(90)]), "GATE_PASS")

    def test_below_ninety_fails(self):
        self.assertEqual(build_table.gate_state([self.rec(89)]), "BELOW_GATE")

    def test_partial_cores_fail_even_at_high_scores(self):
        self.assertEqual(build_table.gate_state([self.rec(95, "partial")]),
                         "BELOW_GATE")

    def test_disagreeing_runs_on_the_same_text_are_flagged(self):
        self.assertEqual(build_table.gate_state([self.rec(91), self.rec(87)]),
                         "CONFLICTING_RUNS")

    def test_unrecorded_cores_are_not_reported_as_a_failure(self):
        self.assertEqual(build_table.gate_state([self.rec(95, "")]),
                         "CORES_NOT_RECORDED")


class Windows(unittest.TestCase):
    now = __import__("datetime").datetime(2026, 11, 26, 12, 0,
                                          tzinfo=build_table.TAIPEI)

    def test_parses_both_stamp_formats_in_the_market_csv(self):
        self.assertIsNotNone(build_table.parse_taipei("2026-11-21 21:25:37+08:00"))
        self.assertIsNotNone(build_table.parse_taipei("2026-11-22 11:41 +08:00"))
        self.assertIsNotNone(
            build_table.parse_taipei("2026-11-24T01:08:55.461843+08:00"))
        self.assertIsNone(build_table.parse_taipei(""))
        self.assertIsNone(build_table.parse_taipei("sometime last week"))

    def test_closed_window_without_data_is_not_called_pending(self):
        pub = build_table.parse_taipei("2026-11-21 21:25:37+08:00")
        self.assertEqual(build_table.window_state(pub, 3, False, self.now),
                         "CLOSED_NOT_COLLECTED")

    def test_open_window_is_pending(self):
        pub = build_table.parse_taipei("2026-11-24 01:08:55+08:00")
        self.assertEqual(build_table.window_state(pub, 7, False, self.now),
                         "PENDING_WINDOW")

    def test_collected_beats_both(self):
        pub = build_table.parse_taipei("2026-11-21 21:25:37+08:00")
        self.assertEqual(build_table.window_state(pub, 1, True, self.now),
                         "COLLECTED")

    def test_unknown_publish_time_is_its_own_state(self):
        self.assertEqual(build_table.window_state(None, 1, False, self.now),
                         "UNKNOWN_PUBLISH_TIME")

    def test_quartiles_interpolate(self):
        q1, q3 = build_table.quartiles([1, 2, 3, 4, 5])
        self.assertAlmostEqual(q1, 2.0)
        self.assertAlmostEqual(q3, 4.0)


class AvgViewedValidity(unittest.TestCase):
    """An avg % viewed printed against zero engaged views is missing, not 0%."""

    def rows(self):
        return build_table.build_rows()

    def test_zero_engaged_views_yields_no_valid_avg(self):
        rows = self.rows()
        bad = [r for r in rows
               if build_table.num(r["d1_engaged_views"]) == 0
               and r["d1_avg_viewed_pct_valid"] != ""]
        self.assertEqual(bad, [], "zero-engagement rows must not supply a retention value")

    def test_positive_engaged_views_keep_their_avg(self):
        rows = self.rows()
        kept = [r for r in rows
                if (build_table.num(r["d1_engaged_views"]) or 0) > 0
                and build_table.num(r["d1_avg_viewed_pct_raw"]) is not None]
        self.assertTrue(kept)
        for r in kept:
            self.assertEqual(r["d1_avg_viewed_pct_valid"],
                             build_table.num(r["d1_avg_viewed_pct_raw"]))


class Statistics(unittest.TestCase):
    def test_pearson_of_a_perfect_line(self):
        self.assertAlmostEqual(build_table.pearson([1, 2, 3], [2, 4, 6]), 1.0)
        self.assertAlmostEqual(build_table.pearson([1, 2, 3], [6, 4, 2]), -1.0)

    def test_pearson_needs_three_pairs_and_some_spread(self):
        self.assertIsNone(build_table.pearson([1, 2], [1, 2]))
        self.assertIsNone(build_table.pearson([5, 5, 5], [1, 2, 3]))

    def test_none_pairs_are_dropped_not_zero_filled(self):
        self.assertAlmostEqual(
            build_table.pearson([1, 2, 3, None], [2, 4, 6, 100]), 1.0)

    def test_spearman_sees_monotone_order_pearson_misses(self):
        xs = [1, 2, 3, 4]
        ys = [1, 2, 3, 400]
        self.assertAlmostEqual(build_table.spearman(xs, ys), 1.0)
        self.assertLess(build_table.pearson(xs, ys), 1.0)

    def test_ranks_average_ties(self):
        self.assertEqual(build_table.ranked([10, 20, 20, 30]), [1.0, 2.5, 2.5, 4.0])

    def test_outlier_detection_names_the_far_tail(self):
        rows = [{"code": "a", "v": "1"}, {"code": "b", "v": "1"},
                {"code": "c", "v": "2"}, {"code": "d", "v": "2"},
                {"code": "e", "v": "3"}, {"code": "f", "v": "900"}]
        self.assertIn("f", build_table.outlier_codes(rows, "v"))
        self.assertNotIn("c", build_table.outlier_codes(rows, "v"))


class RepoIntegration(unittest.TestCase):
    def read(self, name):
        path = os.path.join(HERE, name)
        if not os.path.exists(path):
            self.skipTest(name + " not built yet")
        with open(path, encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def test_04_v7_published_text_hashes_to_the_scored_text(self):
        path = build_table.TEXT_OVERRIDE["04-v7"]
        if not os.path.exists(path):
            self.skipTest("04-v7 approved-story.json not present")
        got = build_table.story_sha256(build_table.load_json(path))
        self.assertEqual(got, SHA_04_V7)

    def test_score_index_keys_every_record(self):
        rows = self.read("score-index.csv")
        self.assertTrue(rows)
        for r in rows:
            self.assertEqual(len(r["story_sha256"]), 64, r["source_path"])

    def test_version_ids_are_not_unique_so_they_cannot_be_the_key(self):
        rows = self.read("score-index.csv")
        by_id = {}
        for r in rows:
            by_id.setdefault(r["version_id"], set()).add(r["story_sha256"])
        reused = {k for k, v in by_id.items() if len(v) > 1}
        self.assertTrue(reused, "expected the known version-id collisions")
        self.assertLessEqual({"62-v1", "61-v2"}, reused)

    def test_unmerged_branch_evidence_is_included(self):
        rows = self.read("score-index.csv")
        self.assertTrue([r for r in rows if r["source_kind"] == "git"],
                        "git-sourced score records must be scanned, not just local")

    def test_published_table_never_claims_a_pass_without_the_text(self):
        rows = self.read("quality-vs-market.csv")
        for r in rows:
            if r["version_check"] == "VERSION_UNVERIFIED":
                self.assertNotEqual(r["ai_gate_state"], "GATE_PASS", r["code"])

    def test_time_windows_stay_in_their_own_columns(self):
        rows = self.read("quality-vs-market.csv")
        d1 = {k for k in rows[0] if k.startswith("d1_")}
        life = {k for k in rows[0] if k.startswith("lifetime_")}
        self.assertTrue(d1 and life and not (d1 & life))
        self.assertIn("d3_window", rows[0])
        self.assertIn("d7_window", rows[0])

    def test_window_status_is_derived_not_a_constant(self):
        rows = self.read("quality-vs-market.csv")
        d3 = {r["d3_window"] for r in rows}
        self.assertGreater(len(d3), 1,
                           "a single value means the window state was hardcoded")

    def test_repeat_play_values_are_flagged(self):
        rows = self.read("quality-vs-market.csv")
        for r in rows:
            v = build_table.num(r["d1_avg_viewed_pct_valid"])
            if v is None:
                self.assertEqual(r["d1_repeat_play"], "")
            else:
                self.assertEqual(r["d1_repeat_play"], "yes" if v > 100 else "no")

    def test_gaps_file_does_not_contradict_the_join(self):
        """The hand-maintained predecessor claimed 04-v7 had no score record."""
        gaps = self.read("data-gaps.csv")
        table = {r["code"]: r for r in self.read("quality-vs-market.csv")}
        for g in gaps:
            if g["state"] == "SCORE_RECORD_MISSING":
                row = table.get(g["code"])
                if row:
                    self.assertEqual(row["ai_gate_state"], "NOT_TESTED", g["code"])

    def test_every_score_record_carries_its_evidence_hash(self):
        """128 of 160 records live only in untracked artifacts/, so the hash is
        the only way another machine can check it read the same file."""
        for r in self.read("score-index.csv"):
            self.assertEqual(len(r["evidence_sha256"]), 64, r["source_path"])
            self.assertIn(r["all_readers_clear"], ("yes", "no"), r["source_path"])

    def test_an_unreadable_source_becomes_a_gap_not_an_empty_list(self):
        import build_gaps
        rows = build_gaps.unavailable("S9", "a source", "it was not readable")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["state"], "SOURCE_UNAVAILABLE")
        self.assertIn("not readable", rows[0]["note"])

    def test_market_columns_come_from_the_schema(self):
        schema = build_table.load_schema()
        rows = self.read("quality-vs-market.csv")
        for spec in schema["fields"]:
            self.assertIn(spec["field"], rows[0], spec["field"])
        for spec in schema["derived"]:
            self.assertIn(spec["field"], rows[0], spec["field"])

    def test_repeat_play_rows_stay_in_the_main_retention_set(self):
        """Replays are real viewing: flagged, not excluded."""
        rows = self.read("quality-vs-market.csv")
        over = [r for r in rows if r["d1_repeat_play"] == "yes"]
        self.assertTrue(over, "expected at least one replayed row")
        for r in over:
            self.assertNotEqual(r["d1_avg_viewed_pct_valid"], "")

    def test_gaps_cover_every_uncollected_window(self):
        gaps = self.read("data-gaps.csv")
        listed = {(g["code"], g["window"]) for g in gaps}
        for r in self.read("quality-vs-market.csv"):
            for name in ("d1", "d3", "d7"):
                if r[name + "_window"] != "COLLECTED":
                    self.assertIn((r["code"], name.upper()), listed, r["code"])


if __name__ == "__main__":
    unittest.main()
