"""S2 EDA figures: categorical bar charts only (no histograms; bin edges deferred per mf-005/mf-006)."""
# ponytail: two plain functions, no styling layer

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

CLASSES = ["jump-down", "stable-low", "stable-high", "jump-up"]  # order per mf-002


def _bars(ax, names, counts, title):
    total = sum(counts)
    ax.bar(names, counts)
    ax.margins(y=0.15)  # room for the labels
    for i, c in enumerate(counts):
        ax.text(i, c, f"{c}\n({c / total:.1%})", ha="center", va="bottom")
    ax.set_title(title)
    ax.set_ylabel("events")


def _save(fig, path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def plot_missions(event_missions, path) -> None:
    """Bar chart of the number of events per mission_id (one row per event)."""
    counts = event_missions.groupby("mission_id").event_id.nunique().sort_index()
    fig, ax = plt.subplots(figsize=(8, 4))
    _bars(ax, [str(m) for m in counts.index], counts.tolist(), "Events per mission")
    ax.set_xlabel("mission_id")
    _save(fig, path)


def plot_imbalance(labels, event_table, path) -> None:
    """Two panels: y_hr counts (False/True) and jump_class counts (four classes)."""
    hr = event_table.y_hr.astype(bool).value_counts()
    jc = labels.jump_class.value_counts()
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    _bars(axes[0], ["False", "True"], [int(hr.get(False, 0)), int(hr.get(True, 0))], "y_hr")
    _bars(axes[1], CLASSES, [int(jc.get(c, 0)) for c in CLASSES], "jump_class")
    _save(fig, path)
