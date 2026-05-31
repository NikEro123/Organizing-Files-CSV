"""
tests/test_analytics.py
Hand-computed checks on the vectorised logic. If the markdown rule ever drifts,
these fail loudly.

Run with pytest:        python -m pytest -q
Or without pytest:      python tests/test_analytics.py
"""
import os
import sys

import numpy as np

# make the project importable whether run via pytest or directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import analytics, benchmark  # noqa: E402

_DT = np.dtype([
    ("product_id", "i8"), ("product_name", "U48"), ("category", "U24"),
    ("batch_number", "i8"), ("quantity_on_hand", "i8"), ("days_to_expiry", "i8"),
    ("unit_price", "f8"), ("unit_cost", "f8"), ("daily_velocity", "f8"),
    ("lead_time_days", "i8"),
])


def _make(rows):
    arr = np.empty(len(rows), dtype=_DT)
    for i, r in enumerate(rows):
        for k, v in r.items():
            arr[k][i] = v
    return arr


def _row(**kw):
    base = dict(product_id=1, product_name="X", category="Dairy", batch_number=10,
                quantity_on_hand=10, days_to_expiry=10, unit_price=5.0, unit_cost=3.0,
                daily_velocity=2.0, lead_time_days=2)
    base.update(kw)
    return base


def test_markdown_tiers():
    rows = [
        _row(product_id=1, batch_number=10, days_to_expiry=-1),                       # expired -> -1
        _row(product_id=2, batch_number=20, days_to_expiry=1),                        # 1 day   -> 3
        _row(product_id=3, batch_number=30, days_to_expiry=3, quantity_on_hand=6),    # 3 day, low waste -> 2
        _row(product_id=4, batch_number=40, days_to_expiry=5, quantity_on_hand=100),  # 5 day, unsold    -> 1
        _row(product_id=5, batch_number=50, days_to_expiry=10, quantity_on_hand=5),   # healthy          -> 0
    ]
    dec, _ = analytics.analyze(_make(rows))
    assert list(dec["markdown_tier"]) == [-1, 3, 2, 1, 0]


def test_high_waste_escalates_to_t3():
    # 3 days left but massively overstocked -> waste ratio high -> tier 3, not 2
    dec, _ = analytics.analyze(_make([_row(days_to_expiry=3, quantity_on_hand=1000, daily_velocity=1)]))
    assert dec["markdown_tier"][0] == 3


def test_projected_waste_value():
    # qty 100, sells 2/day for 3 days -> 6 sold, 94 unsold, * cost 3 = 282 GEL
    dec, _ = analytics.analyze(_make([_row(days_to_expiry=3, quantity_on_hand=100,
                                           daily_velocity=2, unit_cost=3)]))
    assert abs(dec["projected_waste_value"][0] - 282.0) < 1e-9


def test_zero_stock_no_nan():
    # empty batch must not produce NaN in the waste ratio / value
    dec, _ = analytics.analyze(_make([_row(quantity_on_hand=0, days_to_expiry=1)]))
    assert dec["projected_waste_value"][0] == 0.0


def test_restock_trigger():
    # fast mover, tiny but healthy stock -> should flag restock
    dec, _ = analytics.analyze(_make([_row(quantity_on_hand=5, days_to_expiry=10,
                                           daily_velocity=20, lead_time_days=3)]))
    assert bool(dec["restock"][0]) is True


def test_no_restock_when_overstocked():
    # huge healthy stock, slow mover -> no restock
    dec, _ = analytics.analyze(_make([_row(quantity_on_hand=10_000, days_to_expiry=10,
                                           daily_velocity=2, lead_time_days=3)]))
    assert bool(dec["restock"][0]) is False


def test_benchmark_identical_and_faster():
    res = benchmark.run(n=50_000)
    assert res["identical"]
    assert res["speedup"] > 1


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS  {name}")
            except AssertionError as e:
                failures += 1
                print(f"FAIL  {name}: {e}")
    print("-" * 40)
    print("All tests passed." if not failures else f"{failures} test(s) failed.")
    sys.exit(1 if failures else 0)
