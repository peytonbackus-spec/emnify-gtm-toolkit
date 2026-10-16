"""How much does the coverage answer depend on the two assumptions nobody has measured yet?

Sweeps ramp length and usage realization over the synthetic opportunities and prints expected realized revenue as a
share of the signed-value view. Synthetic units; the shape of the table is the point, not the numbers.

    python -m outbound.sensitivity
"""
from __future__ import annotations

from typing import Any, Dict, List

from outbound.coverage import realized_in_period
from outbound.run import OPPS

RAMPS = [3, 6, 9, 12]
REALIZATIONS = [0.6, 0.8, 1.0]


def grid(opps: List[Dict[str, Any]], period_months: int = 12) -> Dict[int, Dict[float, float]]:
    """{ramp_months: {realization: realized / signed-value-for-the-period}} for the expected case."""
    signed = sum(float(o["steady_monthly_revenue"]["expected"]) * max(0, period_months - int(o["go_live_month"])) for o in opps)
    return {r: {x: round(sum(realized_in_period(o, period_months, "expected", r, x) for o in opps) / signed, 2)
                for x in REALIZATIONS} for r in RAMPS}


def main() -> int:
    print("Expected realized revenue as a share of 'signed value from go-live' (12-month period, synthetic opportunities)")
    print("ramp months | " + " | ".join(f"realization {x:.0%}" for x in REALIZATIONS))
    for r, row in grid(OPPS).items():
        print(f"{r:>11} | " + " | ".join(f"{row[x]:>15.0%}" for x in REALIZATIONS))
    print("Read: a slow ramp or low realization can cut what a period realizes by a third or more versus counting signed value.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
