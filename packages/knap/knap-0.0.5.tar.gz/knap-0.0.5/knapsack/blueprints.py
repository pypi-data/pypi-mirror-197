import json
import bisect
from pathlib import Path
from typing import Any, Dict, List, Tuple


class DataPointIndices(object):
    def __init__(
        self,
        start_idxs: List[int] = [],
        interval_lens: List[int] = [],
        filenames_to_idxs: Dict[str, int] = {},
    ):
        if start_idxs is None:
            self.start_idxs = []
        else:
            self.start_idxs = start_idxs

        if interval_lens is None:
            self.interval_lens = []
        else:
            self.interval_lens = interval_lens
        self.filenames_to_idxs = filenames_to_idxs

    def append_num_points(self, num_points: int) -> None:
        if len(self.start_idxs) == 0:
            self.start_idxs = [0]
            self.interval_lens.append(num_points)
        else:
            last_interval_len = self.interval_lens[-1]
            last_interval_len += num_points
            self.interval_lens[-1] = last_interval_len

    def record_original_filename(
        self,
        filename: str,
        idx: int
    ) -> None:
        self.filenames_to_idxs[filename] = idx

    def diff(self, m):
        """
        Takes the left-hand difference of two
        Metadatas. All points in this DPIndexMetadata but not
        in the second one, called 'm', are returned in a new
        DPIndexMetadata.
        """
        new_start_idxs = []
        new_interval_lens = []
        if m is None:
            return self
        for i, start_idx in enumerate(self.start_idxs):
            interval_len = self.interval_lens[i]
            diff_start_idxs, diff_interval_lens = self._interval_diff(
                start_idx, interval_len, m
            )
            new_start_idxs.extend(diff_start_idxs)
            new_interval_lens.extend(diff_interval_lens)
        return DataPointIndices(new_start_idxs, new_interval_lens)

    def _interval_diff(
        self,
        start_idx,
        interval_len,
        m
    ) -> Tuple[List[int], List[int]]:
        """
        Returns a list of start_idxs and interval_lens
        that describe the data points in
        [start_idx, start_idx+interval_len-1] but not
        in the DPIndexMetadata instance 'm'.
        """
        new_start_idxs = [start_idx]
        new_interval_lens = [interval_len]
        end_idx = start_idx + interval_len - 1
        for i, start_idx2 in enumerate(m.start_idxs):
            if start_idx2 > end_idx:
                break

            interval_len2 = m.interval_lens[i]
            end_idx2 = start_idx2 + interval_len2 - 1
            if start_idx2 <= end_idx:
                new_interval_lens[i] = start_idx2

            if end_idx2 >= end_idx:
                break
            elif end_idx2 < end_idx:
                new_start_idxs.append(end_idx2 + 1)
                new_interval_lens.append(end_idx - new_start_idxs[-1])

        return new_start_idxs, new_interval_lens

    def add(self, m) -> None:
        """
        Adds points from m to this DPIndexMetadata that
        aren't already in this instance's points.
        """
        for i, start_idx in enumerate(m.start_idxs):
            interval_len = m.interval_lens[i]
            diff_start_idxs, diff_interval_lens = self._interval_diff(
                start_idx, interval_len, self
            )
            self._merge_metadata(diff_start_idxs, diff_interval_lens)

    def _merge_metadata(
        self,
        new_start_idxs: List[int],
        new_interval_lens: List[int]
    ) -> None:
        """
        Merges new_start_idxs and new_interval_lens
        into self.start_idxs and self.interval_lens.

        This function does not check for correctness -
        arguments are assumed to be valid.
        """
        for i, new_start_idx in enumerate(new_start_idxs):
            loc = bisect.bisect_left(self.start_idxs, new_start_idx)
            self.start_idxs.insert(loc, new_start_idx)
            self.interval_lens.insert(loc, new_interval_lens[i])

    def get_highest_idx(self) -> int:
        if len(self.start_idxs) == 0:
            return -1
        last_start_idx = self.start_idxs[-1]
        last_interval_len = self.interval_lens[-1]
        return last_start_idx + last_interval_len

    def to_dict(self) -> Dict[str, Any]:
        out_dict = {
            "start_idxs": self.start_idxs,
            "interval_lens": self.interval_lens,
            "filenames_to_idxs": self.filenames_to_idxs,
        }
        return out_dict

    def __str__(self):
        return "<cls DataPointIndices>: " + str(self.to_dict())

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return self.to_dict()

    def __iter__(self):
        return self.DataPointIterator(self)

    def __len__(self) -> int:
        if self.interval_lens is None:
            return 0
        return sum(self.interval_lens)

    def __getitem__(self, idx: int):
        # TODO: optimize?
        curr_idx = 0
        for i, interval_len in enumerate(self.interval_lens):
            if idx >= curr_idx and idx < curr_idx + interval_len:
                return self.start_idxs[i] + idx
            curr_idx += interval_len
        raise IndexError("Index for DataPointIndices out of bounds.")

    @staticmethod
    def is_me(json_dict: dict) -> bool:
        """
        Used to determine if a json_dict represents
        a valid DataPointIndices object.
        """
        if ('start_idxs' in json_dict and
            'interval_lens' in json_dict):
            return True
        return False

    @staticmethod
    def from_json(json_dict: dict):
        return DataPointIndices(
            start_idxs=json_dict.get('start_idxs', []),
            interval_lens=json_dict.get('interval_lens', []),
            filenames_to_idxs=json_dict.get('filenames_to_idxs', {}),
        )

    def iterate(self) -> None:
        for i, start_idx in enumerate(self.start_idxs):
            interval_len = self.interval_lens[i]
            for j in range(start_idx, start_idx + interval_len, 1):
                yield j


class Blueprint(object):
    def __init__(
        self,
        repro_tag: str,
        dp_idxs: DataPointIndices,
        bucket_url: Path,
        parent_repro_tags: List[str]
    ):
        self.repro_tag = repro_tag
        self.dp_idxs = dp_idxs
        self.bucket_url = bucket_url
        self.parent_repro_tags = parent_repro_tags
        if self.parent_repro_tags is None:
            self.parent_repro_tags = []

    def get_repro_tag(self) -> str:
        return self.repro_tag

    def get_dp_indices(self) -> DataPointIndices:
        return self.dp_idxs

    def get_bucket_url(self) -> str:
        return self.bucket_url

    def get_num_data_points(self) -> int:
        return self.dp_idxs.get_highest_idx()

    def get_parent_repro_tags(self) -> List[str]:
        return self.parent_repro_tags

    def to_dict(self) -> Dict[str, Any]:
        out_dict = {
            self.repro_tag: {
                "bucket_url": self.bucket_url,
                "dp_idxs": self.dp_idxs.to_json(),
                "storage_url": self.bucket_url,
                "parent_repro_tags": self.parent_repro_tags,
            }
        }
        return out_dict

    def __str__(self):
        return "<cls Blueprint>: " + str(self.to_dict())

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return self.to_dict()

    @staticmethod
    def from_json(json_dict: dict):
        repro_tag = None
        bp_values = json_dict

        if not isinstance(json_dict, dict):
            return json_dict
        elif 'repro_tag' in json_dict:
            repro_tag = json_dict['repro_tag']
        else:
            for tag, values in json_dict.items():
                repro_tag = tag
                bp_values = values

        if ('dp_idxs' in bp_values and
            not isinstance(bp_values['dp_idxs'],
                            DataPointIndices)):
            dp_idxs = DataPointIndices.from_json(bp_values.get('dp_idxs', DataPointIndices()))
        elif ('dp_idxs' in bp_values and
              not isinstance(bp_values['dp_idxs'], DataPointIndices)):
            dp_idxs = bp_values['dp_idxs']
        else:
            dp_idxs = bp_values.get('dp_idxs', DataPointIndices())

        return Blueprint(
            repro_tag=repro_tag,
            dp_idxs=dp_idxs,
            bucket_url=bp_values.get('bucket_url', ''),
            parent_repro_tags=bp_values.get('parent_repro_tags', [])
        )


class Blueprints(object):
    def __init__(self, blueprints: List[Blueprint]):
        self.blueprints = blueprints
        self.repro_tag_to_blueprint = {
            b.repro_tag: b for b in blueprints
        }

    def get_blueprint(self, repro_tag: str) -> Blueprint:
        return self.repro_tag_to_blueprint.get(repro_tag, None)

    def update(self, blueprint: Blueprint) -> None:
        if not isinstance(blueprint, Blueprint):
            raise ValueError("update() only accepts a Blueprint.")
        repro_tag = blueprint.get_repro_tag()
        if repro_tag in self.repro_tag_to_blueprint:
            existing_blueprint = self.repro_tag_to_blueprint[repro_tag]
            existing_blueprint.dp_idxs = blueprint.dp_idxs
            existing_blueprint.bucket_url = blueprint.bucket_url
            existing_blueprint.parent_repro_tags = blueprint.parent_repro_tags
            existing_blueprint.repro_tag = repro_tag
        else:
            self.blueprints.append(blueprint)
        self.repro_tag_to_blueprint[blueprint.repro_tag] = blueprint

    def get_all_dp_indices_for_tag(self, repro_tag: str) -> DataPointIndices:
        # TODO: would be great to cache computation here.
        blueprint = self.get_blueprint(repro_tag)
        dp_indices = DataPointIndices([], [], {})
        dp_indices.add(blueprint.get_dp_indices())

        parent_repro_tags = blueprint.get_parent_repro_tags()
        while len(parent_repro_tags) > 0:
            parent_tag = parent_repro_tags.pop()
            blueprint = self.get_blueprint(parent_tag)
            parent_repro_tags += blueprint.get_parent_repro_tags()
            dp_indices.add(blueprint.get_dp_indices())
        return dp_indices

    def __str__(self):
        out_list = []
        for blueprint in self.blueprints:
            out_list.append(blueprint.__str__())
        return "<cls Blueprints>: " + json.dumps(out_list, ensure_ascii=False)

    def __repr__(self):
        return self.__str__()

    def to_json(self) -> dict:
        return {'blueprints': [b.to_json() for b in self.blueprints]}

    def __iter__(self):
        for blueprint in self.blueprints:
            yield blueprint

    @staticmethod
    def from_json(json_dict: dict):
        if len(json_dict) <= 0:
            return json_dict

        if 'blueprints' in json_dict:
            return Blueprints(
                blueprints=[
                    Blueprint.from_json(blueprint_json_dict)
                    for blueprint_json_dict in json_dict.get('blueprints', [])
                ]
            )
        elif DataPointIndices.is_me(json_dict):
            return DataPointIndices.from_json(json_dict)
        return json_dict
