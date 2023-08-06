from pathlib import Path

from knapsack.knapsack_dataset import KnapsackDataset


def annotate(root: Path) -> KnapsackDataset:
    """
    Attempts to understand the local dataset at 'root'.

    Returns a KnapsackDataset that contains the understood structure(s).
    """
    return KnapsackDataset(root)
