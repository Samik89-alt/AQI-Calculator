

from __future__ import annotations

import statistics
from typing import Any


DEFAULT_BREAKPOINTS: dict[str, list[tuple[float, float]]] = {
    "PM2.5": [
        (0, 30), (31, 60), (61, 90), (91, 120), (121, 250), (251, 380),
    ],
    "PM10": [
        (0, 50), (51, 100), (101, 250), (251, 350), (351, 430), (431, 510),
    ],
    "NO2": [
        (0, 40), (41, 80), (81, 180), (181, 280), (281, 400), (401, 520),
    ],
    "NH3": [
        (0, 200), (201, 400), (401, 800), (801, 1200), (1201, 1800), (1801, 2400),
    ],
    "SO2": [
        (0, 40), (41, 80), (81, 380), (381, 800), (801, 1600), (1601, 2400),
    ],
    "CO": [
        (0, 1.0), (1.1, 2.0), (2.1, 10), (11, 17), (18, 34), (35, 52),
    ],
    "O3": [
        (0, 50), (51, 100), (101, 168), (169, 208), (209, 748), (749, 1188),
    ],
}

AQI_BUCKETS: list[tuple[int, int]] = [
    (0, 50),
    (51, 100),
    (101, 200),
    (201, 300),
    (301, 400),
    (401, 500),
]

AQI_CATEGORIES: list[str] = [
    "Good",
    "Satisfactory",
    "Moderate",
    "Poor",
    "Very Poor",
    "Severe",
]

MEAN_POLLUTANTS: set[str] = {"PM2.5", "PM10", "NO2", "NH3", "SO2"}
MAX_POLLUTANTS: set[str] = {"CO", "O3"}

IDEAL_COUNTS: dict[str, int] = {
    "PM2.5": 16, "PM10": 16, "NO2": 16, "NH3": 16, "SO2": 16,
    "CO": 3, "O3": 3,
}

ALL_POLLUTANTS: list[str] = ["PM2.5", "PM10", "NO2", "NH3", "SO2", "CO", "O3"]


def compute_representative_concentration(pollutant: str, readings: list[float]) -> float:
    if pollutant in MAX_POLLUTANTS:
        return max(readings)
    return statistics.mean(readings)


def compute_sub_index(cp: float, breakpoints: list[tuple[float, float]]) -> float:
    for idx, (c_low, c_high) in enumerate(breakpoints):
        i_low, i_high = AQI_BUCKETS[idx]
        if cp <= c_high:
            denom = c_high - c_low
            if denom == 0:
                return float(i_low)
            return ((i_high - i_low) / denom) * (cp - c_low) + i_low

    c_low, c_high = breakpoints[-1]
    i_low, i_high = AQI_BUCKETS[-1]
    denom = c_high - c_low
    if denom == 0:
        return float(i_high)
    return ((i_high - i_low) / denom) * (cp - c_low) + i_low


def classify_aqi(value: float) -> str:
    for (lo, hi), label in zip(AQI_BUCKETS, AQI_CATEGORIES):
        if value <= hi:
            return label
    return "Severe"


def calculate_aqi(
    readings_map: dict[str, list[float]],
    breakpoints: dict[str, list[tuple[float, float]]] | None = None,
) -> dict[str, Any]:
    if breakpoints is None:
        breakpoints = DEFAULT_BREAKPOINTS

    sub_indices: dict[str, float] = {}
    data_health: list[str] = []

    for pollutant in ALL_POLLUTANTS:
        readings = readings_map.get(pollutant)

        if not readings:
            data_health.append(f"Missing: {pollutant}")
            continue

        ideal = IDEAL_COUNTS[pollutant]
        count = len(readings)
        if count < ideal:
            data_health.append(f"{pollutant}: Sparse ({count}/{ideal})")

        cp = compute_representative_concentration(pollutant, readings)

        bp = breakpoints.get(pollutant)
        if bp is None:
            data_health.append(f"{pollutant}: No breakpoints defined")
            continue

        si = compute_sub_index(cp, bp)
        sub_indices[pollutant] = round(si, 1)

    if sub_indices:
        aqi_value = max(sub_indices.values())
    else:
        aqi_value = 0.0

    return {
        "aqi_value": round(aqi_value, 1),
        "category": classify_aqi(aqi_value),
        "sub_indices": sub_indices,
        "data_health": data_health,
    }


def _print_report(result: dict[str, Any]) -> None:
    w = 56
    print()
    print("═" * w)
    print("  here's what i got".center(w))
    print("═" * w)

    aqi = result["aqi_value"]
    cat = result["category"]
    print(f"  final aqi  →  {aqi}")
    print(f"  category   →  {cat}")
    print("─" * w)

    subs = result.get("sub_indices", {})
    if subs:
        print("  breakdown by pollutant:")
        for p, v in subs.items():
            bar_len = min(int(v / 10), 40)
            bar = "█" * bar_len
            print(f"    {p:>6}  {v:>6.1f}  {bar}")
        print("─" * w)

    warnings = result.get("data_health", [])
    if warnings:
        print("  heads up — some data gaps:")
        for msg in warnings:
            print(f"      • {msg}")
        print("─" * w)

    print("═" * w)
    print()


AVERAGING_HINTS = {
    "PM2.5": "24-hr mean, µg/m³",
    "PM10":  "24-hr mean, µg/m³",
    "NO2":   "24-hr mean, µg/m³",
    "NH3":   "24-hr mean, µg/m³",
    "SO2":   "24-hr mean, µg/m³",
    "CO":    "8-hr max,  mg/m³",
    "O3":    "8-hr max,  µg/m³",
}


def interactive_cli() -> None:
    print()
    print("  hey! this is the ind-aqi calculator.")
    print("  it covers: PM2.5, PM10, NO2, NH3, SO2, CO, and O3.")
    print("  breakpoints are locked to the official ind-aqi standards.")
    print()
    print("  alright, let's get your readings.")
    print("  for each pollutant, type your values separated by spaces.")
    print("  if you don't have data for one, just hit enter to skip it.")
    print()

    readings_map: dict[str, list[float]] = {}

    for pollutant in ALL_POLLUTANTS:
        hint = AVERAGING_HINTS[pollutant]
        raw = input(f"  {pollutant:>6} ({hint}): ").strip()
        if not raw:
            continue
        try:
            values = [float(x) for x in raw.split()]
            if values:
                readings_map[pollutant] = values
        except ValueError:
            print(f"    hmm, couldn't parse that — skipping {pollutant}.")

    if not readings_map:
        print("\n  you didn't enter anything, so there's nothing to calculate.\n")
        return

    result = calculate_aqi(readings_map)
    _print_report(result)


if __name__ == "__main__":
    interactive_cli()