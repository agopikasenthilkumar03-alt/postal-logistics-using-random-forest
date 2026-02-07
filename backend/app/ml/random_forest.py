import json
import math
import random
from dataclasses import dataclass
from pathlib import Path

from app.core.config import settings


FEATURES = [
    "route_distance",
    "historical_delivery_time",
    "rainfall",
    "wind_speed",
    "temperature",
    "flood_risk",
    "month",
]


@dataclass
class Stump:
    feature: str
    threshold: float
    left_value: float
    right_value: float


@dataclass
class SimpleRandomForest:
    model_version: str
    classification_trees: list[Stump]
    regression_trees: list[Stump]

    def predict_delay(self, features: dict[str, float]) -> tuple[bool, int]:
        class_votes = []
        reg_votes = []
        for tree in self.classification_trees:
            value = tree.left_value if features[tree.feature] <= tree.threshold else tree.right_value
            class_votes.append(value)
        for tree in self.regression_trees:
            value = tree.left_value if features[tree.feature] <= tree.threshold else tree.right_value
            reg_votes.append(value)
        class_probability = sum(class_votes) / max(len(class_votes), 1)
        delay_days = int(round(sum(reg_votes) / max(len(reg_votes), 1)))
        return class_probability >= 0.5, max(delay_days, 0)

    def to_dict(self) -> dict:
        return {
            "model_version": self.model_version,
            "classification_trees": [tree.__dict__ for tree in self.classification_trees],
            "regression_trees": [tree.__dict__ for tree in self.regression_trees],
        }

    @staticmethod
    def from_dict(payload: dict) -> "SimpleRandomForest":
        return SimpleRandomForest(
            model_version=payload["model_version"],
            classification_trees=[Stump(**tree) for tree in payload["classification_trees"]],
            regression_trees=[Stump(**tree) for tree in payload["regression_trees"]],
        )


def _build_stump(rows: list[dict], feature: str, target_key: str) -> Stump:
    values = sorted(row[feature] for row in rows)
    threshold = values[len(values) // 2]
    left_rows = [row for row in rows if row[feature] <= threshold]
    right_rows = [row for row in rows if row[feature] > threshold]

    def _aggregate(rows_subset: list[dict]):
        if not rows_subset:
            return 0.0
        return sum(row[target_key] for row in rows_subset) / len(rows_subset)

    left_value = _aggregate(left_rows)
    right_value = _aggregate(right_rows)
    return Stump(feature=feature, threshold=threshold, left_value=left_value, right_value=right_value)


def train_simple_random_forest(rows: list[dict], tree_count: int = 25) -> SimpleRandomForest:
    if not rows:
        raise ValueError("Training data is required to train the model.")
    random.seed(42)
    classification_trees: list[Stump] = []
    regression_trees: list[Stump] = []
    for _ in range(tree_count):
        sampled = [random.choice(rows) for _ in range(len(rows))]
        feature = random.choice(FEATURES)
        classification_trees.append(_build_stump(sampled, feature, "delay_yes_no"))
        regression_trees.append(_build_stump(sampled, feature, "delay_days"))
    return SimpleRandomForest(
        model_version="simple-rf-1.0",
        classification_trees=classification_trees,
        regression_trees=regression_trees,
    )


def load_training_data(path: str) -> list[dict]:
    rows: list[dict] = []
    with open(path, "r", encoding="utf-8") as handle:
        headers = handle.readline().strip().split(",")
        for line in handle:
            values = line.strip().split(",")
            row = {key: float(value) for key, value in zip(headers, values)}
            rows.append(row)
    return rows


def load_or_train_model(data_path: str | None = None) -> SimpleRandomForest:
    model_path = Path(settings.model_path)
    if model_path.exists():
        payload = json.loads(model_path.read_text(encoding="utf-8"))
        return SimpleRandomForest.from_dict(payload)
    if data_path is None:
        raise FileNotFoundError("Model not found and no training data path provided.")
    rows = load_training_data(data_path)
    model = train_simple_random_forest(rows)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    model_path.write_text(json.dumps(model.to_dict(), indent=2), encoding="utf-8")
    return model
