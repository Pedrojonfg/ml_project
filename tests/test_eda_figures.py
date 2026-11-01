import pandas as pd

from src.eda.figures import CLASSES, plot_imbalance, plot_missions


def test_plot_missions(tmp_path):
    em = pd.DataFrame({"event_id": [1, 2, 3], "mission_id": [2, 2, 7]})
    p = tmp_path / "sub" / "m.png"
    plot_missions(em, p)
    assert p.stat().st_size > 0


def test_plot_imbalance(tmp_path):
    labels = pd.DataFrame({"jump_class": CLASSES + ["stable-low"]})
    table = pd.DataFrame({"y_hr": [True, False, False, False, False]})
    p = tmp_path / "i.png"
    plot_imbalance(labels, table, p)
    assert p.stat().st_size > 0
