import re
from datetime import datetime
from typing import List, Literal

from proscan_log_api.utils import get_files


class SlowControlClient:
    """Simple Client to query SlowControl log-files."""

    def __init__(
        self, root_dir: str = "/mnt/TCSlogs/", folders: List[str] | str = []
    ) -> None:
        """Initialize the Client.

        Args:
            root_dir (str, optional): Root dir of the log files. Defaults to "/mnt/TCSlogs/".
            folders (List[str] | str, optional): List of folders containing the logs. Defaults to [].
        """
        self.root_dir = root_dir
        self.folders = folders
        self.signals_re = re.compile(
            r"(# (?P<title>(?!Title|Description|PROSCAN_TCS|Logging)[\S]+) +(?P<key>[\S]*) +(?P<description>.+)\n)"
        )

    def _get_signals(self, text: str) -> List[dict]:
        """Get the signals from the header of the file.

        Args:
            text (str): File content as str.

        Returns:
            List[dict]: List of signals with keys: title, key, description
        """
        signals = []
        for row in self.signals_re.finditer(text):
            signals.append(row.groupdict())
        return signals

    def _create_pattern(self, signal_names: List[str]) -> re.Pattern:
        """Creates the pattern to parse the rows of the log depending on the number of signals in the header.

        Args:
            signal_names (List[str]): List of signal names in the log file

        Returns:
            re.Pattern: compiled regex pattern for the row.
        """
        pattern = r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+"
        for i, _ in enumerate(signal_names):
            pattern = pattern + r"(?P<%s>\S+)\s+" % f"g{i}"
        pattern = pattern + r"\s*\n"
        return re.compile(pattern)

    def get(
        self,
        system: Literal["tvs", "tds"],
        folders: List[str] | str = [],
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
        area: Literal["G2", "G3", "O2"] | None = None,
    ) -> List[dict]:
        """Parsese the Slow Control log files.

        Args:
            system (Literal['tvs', 'tds']): Select the system of which the SlowControl logs should be returned.
            folders (List[str] | str, optional): List of folders to search. Defaults to [].
            start_datetime (datetime | None, optional): Earliest datetime that should be returned. Defaults to None.
            end_datetime (datetime | None, optional): Latest datetime that should be returned. Defaults to None.
            area (Literal['G2', 'G3', 'O2'] | None, optional): Area of which the log files should be parsed. Defaults to None.

        Raises:
            Exception: This exception gets raised if neither the client nor this method was provided a list of folders.

        Returns:
            List[dict]: Returns a list of dicts with the signals as key and values of the signal as value. First key is always timestamp with timestamp of values in dict.
        """
        data_list = []

        if not folders:
            if self.folders:
                folders = self.folders
            else:
                raise Exception("Please provide the folders to be searched!")

        for file in get_files(
            root_dir=self.root_dir,
            folders=folders,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            area=area,
            tcs_type="SlowControl",
            system=system,
        ):
            with open(file, mode="r", encoding="utf-8") as file_obj:
                text = file_obj.read()
                signals = self._get_signals(text)
                pattern = self._create_pattern(
                    [unit["title"] for unit in self._get_signals(text)]
                )
                for row in pattern.finditer(text):
                    row_dict = {}
                    group_values = list(row.groupdict().values())
                    row_dict["timestamp"] = group_values.pop(0)
                    for i, value in enumerate(group_values):
                        row_dict[signals[i]["title"]] = value

                    data_list.append(row_dict)
        return data_list
