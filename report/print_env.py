"""Print the computing environment for the Final Report (setup section).
Usage: python report/print_env.py   (run it in the SAME environment used for your experiments)
"""
import os, platform, sys
from importlib import metadata


MODULES = {"scikit-learn": "sklearn"}


def v(pkg):
    """Version of the module that is actually imported (dist-info can be stale)."""
    try:
        mod = __import__(MODULES.get(pkg, pkg))
        return getattr(mod, "__version__", "unknown") + f"  (dist-info: {metadata.version(pkg)})"
    except Exception:
        return "not installed"


print("OS:", platform.platform())
print("Python:", sys.version.split()[0], platform.python_implementation())
print("CPU:", platform.processor() or platform.machine(), "| logical cores:", os.cpu_count())
try:
    with open("/proc/cpuinfo") as f:
        print("CPU model:", next(l.split(":")[1].strip() for l in f if l.startswith("model name")))
    with open("/proc/meminfo") as f:
        print("RAM:", next(l.split(":")[1].strip() for l in f if l.startswith("MemTotal")))
except Exception:
    pass
for p in ["numpy", "pandas", "scipy", "scikit-learn", "torch", "pyarrow", "matplotlib", "joblib", "threadpoolctl"]:
    print(f"{p}: {v(p)}")
try:
    import torch
    print("torch CUDA available:", torch.cuda.is_available(), "| torch threads:", torch.get_num_threads())
except Exception as e:
    print("torch import failed:", e)
try:
    import numpy as np
    from threadpoolctl import threadpool_info
    print("BLAS:", [(d.get("internal_api"), d.get("version")) for d in threadpool_info()])
except Exception as e:
    print("BLAS info unavailable:", e)
