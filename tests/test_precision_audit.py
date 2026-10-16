import csv

import pytest

from gtm_engineer.enrichment.precision_audit import (
    blind_sheet,
    demo_rows,
    format_report,
    load_labels,
    paired_comparison,
    summarize,
    wilson_interval,
)


class TestWilson:
    def test_known_value_80_of_100(self):
        lo, hi = wilson_interval(80, 100)
        assert lo == pytest.approx(0.7112, abs=0.001)
        assert hi == pytest.approx(0.8666, abs=0.001)

    def test_interval_narrows_with_n(self):
        w_small = wilson_interval(20, 25)
        w_big = wilson_interval(800, 1000)
        assert (w_big[1] - w_big[0]) < (w_small[1] - w_small[0])

    def test_bounds_clamped(self):
        assert wilson_interval(0, 10)[0] == 0.0
        assert wilson_interval(10, 10)[1] == 1.0

    @pytest.mark.parametrize("k,n", [(1, 0), (-1, 5), (6, 5)])
    def test_invalid_inputs(self, k, n):
        with pytest.raises(ValueError):
            wilson_interval(k, n)


def _rows(spec):
    # spec: list of (account, tool, correct)
    return [{"account_id": a, "tool": t, "correct": c} for a, t, c in spec]


class TestSummarize:
    def test_precision_per_tool_sorted(self):
        rows = _rows([("1", "A", True), ("2", "A", True), ("1", "B", True), ("2", "B", False)])
        out = summarize(rows)
        assert [t.tool for t in out] == ["A", "B"]
        assert out[0].precision == 1.0 and out[1].precision == 0.5
        assert out[1].n == 2 and out[1].correct == 1


class TestPaired:
    def test_exact_p_value_known_case(self):
        spec = []
        for i in range(9):
            spec += [(f"a{i}", "A", True), (f"a{i}", "B", False)]
        spec += [("b0", "A", False), ("b0", "B", True)]
        res = paired_comparison(_rows(spec), "A", "B")
        assert (res["a_only"], res["b_only"]) == (9, 1)
        assert res["p_value"] == pytest.approx(0.021484375)

    def test_no_disagreement_gives_p_one(self):
        res = paired_comparison(_rows([("1", "A", True), ("1", "B", True)]), "A", "B")
        assert res["p_value"] == 1.0 and res["both"] == 1

    def test_ignores_accounts_missing_one_tool(self):
        res = paired_comparison(_rows([("1", "A", True), ("2", "A", True), ("2", "B", False)]), "A", "B")
        assert res["paired_n"] == 1


class TestBlindSheet:
    CANDS = [{"account_id": f"A{i}", "tool": "ToolX" if i % 2 else "ToolY", "contact": f"c{i}"} for i in range(10)]

    def test_deterministic_and_hides_tool(self):
        s1, k1 = blind_sheet(self.CANDS, seed=3)
        s2, _ = blind_sheet(self.CANDS, seed=3)
        assert s1 == s2
        assert all("tool" not in row for row in s1)
        assert {r["tool"] for r in k1} == {"ToolX", "ToolY"}
        assert len(s1) == len(self.CANDS)


class TestLoadAndReport:
    def test_load_labels_and_bad_value(self, tmp_path):
        p = tmp_path / "labels.csv"
        with open(p, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["account_id", "tool", "correct"])
            w.writerow(["1", "A", "yes"])
            w.writerow(["2", "A", "0"])
        rows = load_labels(str(p))
        assert [r["correct"] for r in rows] == [True, False]
        bad = tmp_path / "bad.csv"
        bad.write_text("account_id,tool,correct\n1,A,maybe\n")
        with pytest.raises(ValueError):
            load_labels(str(bad))

    def test_missing_columns(self, tmp_path):
        p = tmp_path / "x.csv"
        p.write_text("account_id,tool\n1,A\n")
        with pytest.raises(ValueError):
            load_labels(str(p))

    def test_demo_report_runs(self):
        text = format_report(demo_rows(), "ToolA", "ToolB")
        assert "95% interval" in text and "Paired on 100 accounts" in text
