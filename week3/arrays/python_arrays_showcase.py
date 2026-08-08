#!/usr/bin/env python3
"""
python_arrays_showcase.py

A side‑by‑side demo of three "array-like" options in Python:
1) list
2) array.array
3) numpy.ndarray

What you'll see:
- Creation & typing behavior
- Indexing & slicing
- Elementwise operations
- Memory footprint
- Micro-benchmarks (timeit) for common tasks

Run:
    python python_arrays_showcase.py

Notes:
- NumPy is optional. If it's not installed, the script will still run (skips NumPy parts).
- Adjust N, REPEATS as needed.
"""

from __future__ import annotations

import sys
import timeit
import math
import statistics as stats
from dataclasses import dataclass
from typing import Callable, Optional

# Optional NumPy
try:
    import numpy as np  # type: ignore
except Exception:
    np = None  # Fallback if NumPy isn't installed


# -----------------------------
# Config
# -----------------------------

N = 1_000_00  # number of elements for demos/benchmarks (100k). Bump to 1_000_000 for bigger effects.
REPEATS = 5   # number of timeit repeats per task


# -----------------------------
# Helpers
# -----------------------------

def human_bytes(n: int) -> str:
    """Nicely format bytes -> KB/MB/GB."""
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    f = float(n)
    while f >= 1024 and i < len(units) - 1:
        f /= 1024.0
        i += 1
    if f >= 100:
        return f"{f:,.0f} {units[i]}"
    elif f >= 10:
        return f"{f:,.1f} {units[i]}"
    else:
        return f"{f:,.2f} {units[i]}"


@dataclass
class BenchResult:
    label: str
    times: list[float]

    @property
    def best(self) -> float:
        return min(self.times)

    @property
    def mean(self) -> float:
        return sum(self.times) / len(self.times)

    @property
    def stdev(self) -> float:
        return stats.pstdev(self.times) if len(self.times) > 1 else 0.0

    def pretty(self) -> str:
        return f"{self.label:<35} best={self.best:.6f}s  mean={self.mean:.6f}s  stdev={self.stdev:.6f}s"


def run_timeit(stmt: str, setup: str, repeats: int = REPEATS) -> BenchResult:
    tms = timeit.repeat(stmt=stmt, setup=setup, repeat=repeats, number=1)
    return BenchResult(label=stmt, times=tms)


# -----------------------------
# Demos
# -----------------------------

def demo_lists():
    print("\n=== 1) Python list: dynamic, can hold mixed types ===")
    nums = [1, 2, 3, 4]
    print("nums:", nums)
    nums.append(5)
    nums[1] = 20
    print("modified:", nums)
    print("slice nums[1:4]:", nums[1:4])

    # Mixed types allowed
    mixed = [1, "two", 3.0, True]
    print("mixed types list:", mixed)

    # Elementwise ops via list comp / loop
    doubled = [x * 2 for x in nums]
    print("doubled via list comprehension:", doubled)


def demo_array_module():
    print("\n=== 2) array.array: fixed type, compact memory ===")
    import array
    arr = array.array("i", [1, 2, 3, 4])  # signed int
    arr.append(5)
    arr[1] = 20
    print("arr:", arr.tolist())
    print("slice arr[1:4]:", arr[1:4].tolist())

    # Elementwise ops require loops
    doubled = array.array("i", (x * 2 for x in arr))
    print("doubled via generator:", doubled.tolist())


def demo_numpy():
    if np is None:
        print("\n=== 3) NumPy not installed; skipping demo. Install via: pip install numpy ===")
        return
    print("\n=== 3) NumPy ndarray: fixed type, vectorized, multi‑dimensional ===")
    arr = np.array([1, 2, 3, 4], dtype=np.int32)
    print("arr:", arr)
    arr[1] = 20
    print("modified:", arr)
    print("slice arr[1:4]:", arr[1:4])

    # Vectorized elementwise ops
    doubled = arr * 2
    print("vectorized doubled:", doubled)

    # 2D array (matrix)
    mat = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.int32)
    print("2D matrix:\n", mat)
    print("mat[1, 2] =", mat[1, 2])
    print("row 0:", mat[0])
    print("column 1:", mat[:, 1])

    # Broadcasting example
    print("mat + 10:\n", mat + 10)


# -----------------------------
# Memory comparison
# -----------------------------

def memory_footprint():
    import array

    print("\n=== Memory footprint (approximate) ===")
    # Build data
    data_py = [i for i in range(N)]

    # Python list object overhead + elements (references). getsizeof is only the container object.
    list_container_bytes = sys.getsizeof(data_py)

    # element references cost is implementation-dependent; we at least show container size
    print(f"list: container size = {human_bytes(list_container_bytes)} (does not include per-element objects)")

    # array('i') stores raw C ints
    arr = array.array("i", data_py)
    array_bytes = sys.getsizeof(arr)
    print(f"array('i'): container+buffer size = {human_bytes(array_bytes)}")

    if np is not None:
        np_arr = np.array(data_py, dtype=np.int32)
        print(f"numpy int32: buffer nbytes = {human_bytes(np_arr.nbytes)}; numpy object size = {human_bytes(sys.getsizeof(np_arr))}")
    else:
        print("numpy not available: install with `pip install numpy` to compare.")


# -----------------------------
# Benchmarks
# -----------------------------

def benchmarks():
    print("\n=== Micro-benchmarks (lower is faster) ===")
    print(f"N={N:,} elements, REPEATS={REPEATS}")

    # Common setup strings for timeit
    setup_list = f"import random; data = list(range({N}))"
    setup_array = f"import array, random; data = array.array('i', range({N}))"
    setup_numpy = None
    if np is not None:
        setup_numpy = f"import numpy as np; data = np.arange({N}, dtype=np.int32)"

    results: list[BenchResult] = []

    # 1) Sum reduction
    results.append(run_timeit("sum(data)", setup_list))
    results.append(run_timeit("sum(data)", setup_array))
    if setup_numpy:
        results.append(run_timeit("data.sum()", setup_numpy))

    # 2) Elementwise multiply by 2 (create new container)
    results.append(run_timeit("[x*2 for x in data]", setup_list))
    results.append(run_timeit("array.array('i', (x*2 for x in data))", setup_array))
    if setup_numpy:
        results.append(run_timeit("data * 2", setup_numpy))

    # 3) Elementwise add two arrays of same size
    results.append(run_timeit("[(a+b) for a,b in zip(data, data)]", setup_list))
    results.append(run_timeit("array.array('i', (a+b for a,b in zip(data, data)))", setup_array))
    if setup_numpy:
        results.append(run_timeit("data + data", setup_numpy))

    # 4) Slicing (create middle slice)
    results.append(run_timeit("data[len(data)//4: 3*len(data)//4]", setup_list))
    results.append(run_timeit("data[len(data)//4: 3*len(data)//4]", setup_array))
    if setup_numpy:
        results.append(run_timeit("data[len(data)//4: 3*len(data)//4]", setup_numpy))

    # Print neatly
    # Grouped by task for readability
    labels = [
        "sum(list)",
        "sum(array('i'))",
        "sum(numpy)",
        "[x*2 for x in list]",
        "array('i')*2 via gen",
        "numpy * 2",
        "list pairwise add",
        "array('i') pairwise add",
        "numpy + numpy",
        "slice list mid-half",
        "slice array mid-half",
        "slice numpy mid-half",
    ]

    print("\n--- Results ---")
    i = 0
    for res in results:
        # Map results to friendlier labels in output order
        if i < len(labels):
            label = labels[i]
        else:
            label = res.label
        print(f"{label:<28}  best={res.best:.6f}s  mean={res.mean:.6f}s  stdev={res.stdev:.6f}s")
        i += 1

    if np is None:
        print("\n(Install NumPy for vectorized speedups: `pip install numpy`)")


# -----------------------------
# Main
# -----------------------------

def main():
    print("Python 'Arrays' Showcase\n")
    demo_lists()
    demo_array_module()
    demo_numpy()
    memory_footprint()
    benchmarks()


if __name__ == "__main__":
    main()
