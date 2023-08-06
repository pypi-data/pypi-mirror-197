import re
from datetime import datetime
from typing import List, Literal, Optional, Union

from proscan_log_api.utils import get_files


class TcsTraceClient:
    def __init__(
        self, root_dir: str = "/mnt/TCSlogs/", folders: List[str] | str = []
    ) -> None:
        """Initialize the Client.

        Args:
            root_dir (str, optional): Root dir of the log files. Defaults to "/mnt/TCSlogs/".
            folders (List[str] | str, optional): List of folders containing the logs Defaults to [].
        """
        self.root_dir = root_dir
        self.folders = folders

    def _create_pattern(
        self,
        timestamp: Union[int, float, datetime, None] = None,
        source: Optional[str] = None,
        signal_type: Optional[str] = None,
        message_regex: Optional[str] = None,
    ) -> re.Pattern:
        """Creates a pattern to filter the log-files for the selected parameters.

        Args:
            timestamp (Union[int, float, datetime, None], optional): Timestamp to filter the logs to. This only works for entries with this specific timestamp. For a rage use start end end datetime. Defaults to None.
            source (Optional[str], optional): source the log entries must contain. Defaults to None.
            signal_type (Optional[str], optional): signal type the log entries must contain. Defaults to None.
            message_regex (Optional[str], optional): message regex the messages must adhere to. Defaults to None.

        Returns:
            re.Pattern: Compiled regex pattern the log entries must match.
        """
        if timestamp:
            if timestamp.isinstance(int):
                time_str = datetime.strftime(
                    datetime.fromtimestamp(timestamp / 1000000), "%d.%m.%y %H:%M:%S.%f"
                )
            elif timestamp.isinstance(float):
                time_str = datetime.strftime(
                    datetime.fromtimestamp(timestamp), "%d.%m.%y %H:%M:%S.%f"
                )
            elif timestamp.isinstance(datetime):
                time_str = datetime.strftime(timestamp, "%d.%m.%y %H:%M:%S.%f")
            time_str = time_str[:21]
        else:
            time_str = r"\d{2}\.\d{2}\.\d{2}\s\d{2}\:\d{2}\:\d{2}.\d+"
        if not source:
            source = r"\w+"
        if not signal_type:
            signal_type = r"[^:]+"
        if not message_regex:
            message_regex = r"[^\n]+"
        if message_regex:
            message_regex = message_regex + r"[^\n]+"

        pattern = re.compile(
            r"(?P<timestamp>%s)\s(?P<source>%s)\s(?P<signal_type>%s):\s(?P<message>%s)"
            % (time_str, source, signal_type, message_regex)
        )
        return pattern

    def get(
        self,
        system: Literal["tds", "tvs"],
        area: Optional[Literal["G2", "G3", "O2"]],
        folders: List[str] | str = [],
        start_datetime: Optional[datetime] = None,
        end_datetime: Optional[datetime] = None,
        timestamp: Union[int, float, datetime, None] = None,
        source: Optional[str] = None,
        signal_type: Optional[str] = None,
        message_regex: Optional[str] = None,
    ) -> List[dict]:
        """Get the tcs trace log entries.

        Args:
            system (Literal['tds', 'tvs']):  Select the system of which the SlowControl logs should be returned.
            area (Optional[Literal['G2', 'G3', 'O2']]): Area of which the log files should be parsed.
            folders (List[str] | str, optional): List of folders to search. Defaults to [].
            start_datetime (datetime | None, optional): Earliest datetime that should be returned. Defaults to None.
            end_datetime (datetime | None, optional): Latest datetime that should be returned. Defaults to None.
            timestamp (Union[int, float, datetime, None], optional): Timestamp to filter the logs to. This only works for entries with this specific timestamp. For a rage use start end end datetime. Defaults to None.
            source (Optional[str], optional): source the log entries must contain. Defaults to None.
            signal_type (Optional[str], optional): signal type the log entries must contain. Defaults to None.
            message_regex (Optional[str], optional): message regex the messages must adhere to. Defaults to None.

        Raises:
            Exception: This exception gets raised if neither the client nor this method was provided a list of folders.
            Exception: Gets raised if no data has been found.

        Returns:
           List[dict]: List of dicts containing the log entries. Keys are timestamp, source, signal, message.
        """
        data_list = []
        pattern = self._create_pattern(timestamp, source, signal_type, message_regex)
        if not folders:
            if self.folders:
                folders = self.folders
            else:
                raise Exception("Please provide the folders to be searched!")

        for file in get_files(
            system=system,
            folders=folders,
            root_dir=self.root_dir,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            area=area,
            tcs_type="TcsTrace",
        ):
            with open(file, mode="r", encoding="utf-8") as file_obj:
                for row in pattern.finditer(file_obj.read()):
                    row_dict = row.groupdict()
                    row_datetime = datetime.strptime(
                        row_dict["timestamp"],
                        "%d.%m.%y %H:%M:%S.%f",
                    )
                    if (row_datetime >= start_datetime or not start_datetime) and (
                        row_datetime <= end_datetime or not end_datetime
                    ):
                        data_list.append(row_dict)

        if not data_list:
            raise Exception("No data found!")
        return data_list
