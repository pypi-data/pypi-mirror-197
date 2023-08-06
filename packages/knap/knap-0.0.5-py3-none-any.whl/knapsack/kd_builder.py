from os import listdir, walk
from os.path import join
from pathlib import Path
from typing import Dict, List

from tqdm import tqdm

from knapsack.split import Split


class KDBuilder(object):
    """
    Knapsack Dataset Builder
    """
    def __init__(self, root: str) -> None:
        self.root = root

        self.data_dirs = []
        self.data_dirs_to_num_files = {}
        self.files = None

    def add_dir_annotation(
        self,
        location: Path,
        inclusions: List[Path] = [],
        exclusions: List[Path] = [],
    ) -> None:
        """
        Adds annotation.

        This method is used by KnapsackDataset to 'understand' the
        local dataset in the case when the dataset is not already in
        KnapsackDataset standardized format (for example, the dataset was
        downloaded from the internet and not from Knapsack).

        Specifically, add_dir_annotation adds an annotation to the current dir.
        All the files in 'location' (intersection with inclusions,
        not in exclusions), will now be marked as part of the dataset.

        Args:
            location - Path relative to root that contains the data dir to add.
            inclusions - If inclusions is not empty, any dir or subdir encountered
                during this add operation that isn't in inclusions will be ignored.
            exclusions - Paths of dirs/subdirs to exclude. Exclusions are
                evaluated after inclusions.
        """
        data_locations = []
        for root, dirs, files in walk(join(self.root, location)):
            num_files = len(files)
            print(f"KNAPSACK FOUND {num_files} FILES.")
            relative_location = Path(root).relative_to(self.root)
            data_dirs = dirs
            if len(inclusions) > 0:
                data_dirs = [d for d in data_dirs
                             if Path(root) / Path(d) in inclusions]

            data_dirs = [join(relative_location, d)
                         for d in data_dirs
                         if Path(root) / Path(d) not in exclusions]
            if len(files) > 0:
                data_dirs += [location / Path(".")]
            data_locations += data_dirs

        self.data_dirs += data_locations
        self.data_dirs.sort()

        self.files = []
        for data_dir in self.data_dirs:
            matching_files = self._get_matching_files(Path(self.root) / Path(data_dir))
            self.files += matching_files
            self.data_dirs_to_num_files[data_dir] = len(matching_files)

    def get_root(self) -> str:
        return self.root

    def _get_num_files_in_dir(self, location) -> int:
        # TODO: someday, we might want this to filter out
        # files that are not data points?
        if location.is_file():
            return [location]
        all_items = listdir(str(location))
        return len(all_items)

    def get_total_num_data_points(self) -> int:
        total = 0
        for data_dir in self.data_dirs:
            location = Path(self.root) / Path(data_dir)
            total += self._get_num_files_in_dir(location)
        return total

    def _get_matching_files(self, location: Path) -> List[Path]:
        if location.is_file():
            return [location]
        all_items = listdir(str(location))
        return [Path(f) for f in all_items]

    def iterate_over_files(self):
        for data_dir in self.data_dirs:
            files = self._get_matching_files(Path(self.root) / Path(data_dir))
            for file in tqdm(files):
                full_file = Path(self.root) / Path(data_dir) / file
                yield full_file

    def __getitem__(self, i: int) -> Path:
        """
        Unfortunately, __getitem__ runs in less than O(1) time (worst
        case O(n) time).
        It would be great to make this more efficient.

        self.files helps, but having to iterate over the data_dirs sux.
        """
        current_idx = 0
        for data_dir in self.data_dirs:
            prev_idx = current_idx
            current_idx += self.data_dirs_to_num_files[data_dir]

            if i < current_idx and i >= prev_idx:
                file = self.files[i]
                full_file = Path(self.root) / Path(data_dir) / file
                return full_file
        raise IndexError(f"Index out of bounds for KDBuilder: {i}")
