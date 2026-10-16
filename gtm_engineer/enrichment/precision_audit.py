"""Precision audit: check a vendor's list-precision claim on your own accounts.

A vendor benchmark ("we beat X on list precision") is only as good as its sample
size, labeling and ICP. This module lets a team run the same test on its own list:

1. Build a blind labeling sheet (tool names stripped, order shuffled).
2. Have someone who knows the market label each contact correct / not correct.
3. Report precision per tool with a 95% Wilson interval, and an exact paired
   comparison between two tools on the accounts both returned.

Input labels CSV columns: account_id, tool, correct  (1/0, true/false, yes/no).
Run:  python -m gtm_engineer.enrichment.precision_audit labels.csv --a ToolA --b ToolB
      python -m gtm_engineer.enrichment.precision_audit --demo        (synthetic data)

Assumptions [ASSUME]: labels are independent, the labeled accounts are a fair sample
of your ICP, and the labeler was blind to the tool. The interval covers sampling
error only; it cannot detect a biased sample or inconsistent labels.
"""
import argparse
import csv
import math
import random
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple

TRUE_VALUES = {"1", "true", "yes", "y", "correct"}
FALSE_VALUES = {"0", "false", "no", "n", "incorrect"}


def wilson_interval(successes: int, n: int, z: float = 1.96) -> Tuple[float, float]:
    """Wilson score interval for a proportion, clamped to [0, 1]."""
    if n <= 0:
        raise ValueError("n must be positive")
    if successes < 0 or successes > n:
        raise ValueError("successes must be between 0 and n")
    p = successes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


@dataclass
class ToolResult:
    tool: str
    n: int
    correct: int
    precision: float
    lo: float
    hi: float


def _parse_bool(raw: str) -> bool:
    v = str(raw).strip().lower()
    if v in TRUE_VALUES:
        return True
    if v in FALSE_VALUES:
        return False
    raise ValueError(f"unrecognised label value: {raw!r}")


def load_labels(path: str) -> List[Dict[str, object]]:
    """Read a labels CSV into rows of {account_id, tool, correct(bool)}."""
    rows: List[Dict[str, object]] = []
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        missing = {"account_id", "tool", "correct"} - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"missing columns: {sorted(missing)}")
        for r in reader:
            rows.append({"account_id": r["account_id"].strip(), "tool": r["tool"].strip(),
                         "correct": _parse_bool(r["correct"])})
    return rows


def summarize(rows: Iterable[Dict[str, object]]) -> List[ToolResult]:
    """Precision and 95% interval per tool, best first."""
    counts: Dict[str, List[int]] = {}
    for r in rows:
        c = counts.setdefault(str(r["tool"]), [0, 0])
        c[1] += 1
        c[0] += 1 if r["correct"] else 0
    out = []
    for tool, (k, n) in counts.items():
        lo, hi = wilson_interval(k, n)
        out.append(ToolResult(tool, n, k, k / n, lo, hi))
    return sorted(out, key=lambda t: (-t.precision, t.tool))


def paired_comparison(rows: Iterable[Dict[str, object]], tool_a: str, tool_b: str) -> Dict[str, float]:
    """Exact paired comparison on accounts labeled for both tools (McNemar exact test).

    Counts accounts where only A was correct, only B was correct, both, neither.
    The two-sided p-value tests whether the disagreements split evenly.
    """
    labels: Dict[str, Dict[str, bool]] = {}
    for r in rows:
        if r["tool"] in (tool_a, tool_b):
            labels.setdefault(str(r["account_id"]), {})[str(r["tool"])] = bool(r["correct"])
    a_only = b_only = both = neither = 0
    for per in labels.values():
        if tool_a not in per or tool_b not in per:
            continue
        a, b = per[tool_a], per[tool_b]
        if a and b:
            both += 1
        elif a:
            a_only += 1
        elif b:
            b_only += 1
        else:
            neither += 1
    paired_n = a_only + b_only + both + neither
    disagree = a_only + b_only
    if disagree == 0:
        p_value = 1.0
    else:
        tail = sum(math.comb(disagree, k) for k in range(0, min(a_only, b_only) + 1))
        p_value = min(1.0, 2 * tail / 2 ** disagree)
    diff = ((a_only - b_only) / paired_n) if paired_n else 0.0
    return {"paired_n": paired_n, "a_only": a_only, "b_only": b_only, "both": both,
            "neither": neither, "precision_diff_a_minus_b": diff, "p_value": p_value}


def blind_sheet(candidates: List[Dict[str, str]], seed: int = 7) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    """Shuffle candidate contacts and strip tool names.

    candidates: rows with account_id, tool, contact. Returns (sheet, key). Give the
    labeler only `sheet`; keep `key` (blind_id -> account_id, tool) to join labels back.
    """
    order = list(range(len(candidates)))
    random.Random(seed).shuffle(order)
    sheet, key = [], []
    for new_id, idx in enumerate(order, start=1):
        c = candidates[idx]
        bid = f"B{new_id:04d}"
        sheet.append({"blind_id": bid, "account_id": c["account_id"], "contact": c["contact"], "correct": ""})
        key.append({"blind_id": bid, "account_id": c["account_id"], "tool": c["tool"]})
    return sheet, key


def demo_rows(n_accounts: int = 100, seed: int = 11) -> List[Dict[str, object]]:
    """Synthetic, seeded labels for two imaginary tools (not real vendor data)."""
    rng = random.Random(seed)
    rows = []
    for i in range(n_accounts):
        shared = rng.random()
        rows.append({"account_id": f"A{i:03d}", "tool": "ToolA", "correct": shared < 0.82 or rng.random() < 0.05})
        rows.append({"account_id": f"A{i:03d}", "tool": "ToolB", "correct": shared < 0.74 or rng.random() < 0.05})
    return rows


def format_report(rows: List[Dict[str, object]], tool_a: Optional[str], tool_b: Optional[str]) -> str:
    lines = ["Tool        n  correct  precision  95% interval"]
    for t in summarize(rows):
        lines.append(f"{t.tool:<8} {t.n:>4} {t.correct:>8}  {t.precision:>8.1%}  {t.lo:.1%} to {t.hi:.1%}")
    if tool_a and tool_b:
        pc = paired_comparison(rows, tool_a, tool_b)
        lines.append("")
        lines.append(f"Paired on {int(pc['paired_n'])} accounts: only {tool_a} correct {int(pc['a_only'])}, "
                     f"only {tool_b} correct {int(pc['b_only'])}, both {int(pc['both'])}, neither {int(pc['neither'])}")
        lines.append(f"Difference ({tool_a} minus {tool_b}): {pc['precision_diff_a_minus_b']:+.1%}, exact p = {pc['p_value']:.3f}")
    lines.append("")
    lines.append("Sampling error only. Check ICP fit, label quality and blind labeling before relying on this.")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("labels", nargs="?", help="labels CSV (account_id, tool, correct)")
    ap.add_argument("--a")
    ap.add_argument("--b")
    ap.add_argument("--demo", action="store_true", help="run on synthetic seeded data")
    args = ap.parse_args(argv)
    if args.demo:
        rows, a, b = demo_rows(), "ToolA", "ToolB"
    elif args.labels:
        rows, a, b = load_labels(args.labels), args.a, args.b
    else:
        ap.error("provide a labels CSV or --demo")
    print(format_report(rows, a, b))


if __name__ == "__main__":
    main()
