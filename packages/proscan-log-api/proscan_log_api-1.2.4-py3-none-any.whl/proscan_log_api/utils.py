import glob
import os
import re
from datetime import date, datetime, timedelta
from typing import List, Literal, Optional


def get_folders(
    folders: List[str] | str, area: Literal["MP", "G2", "G3", "O2"]
) -> List[str]:
    """Gets the folders containing the specified areas from all folders.

    Args:
        folders (List[str] | str): List or comma separated string containing all folders.
        area (Literal['MP', 'G2', 'G3', 'O2']): Area the foldername must contain.

    Returns:
        List[str]: List of folders
    """
    folders_list = []
    result = []
    if isinstance(folders, str):
        folders_list = folders.split(",")
    else:
        folders_list = folders
    for folder in folders_list:
        if area in folder:
            result.append(folder)
    return result


def _get_pass_file_by_date(d: date, folder: str) -> List[str]:
    """Get pass files by date.

    Args:
        d (date): date contained in the file name.
        folder (str): root folder that contains the file.

    Returns:
        List[str]: List of files.
    """
    files = []

    files = files + glob.glob(
        r"*%s.txt" % (d.isoformat()),
        root_dir=folder,
    )

    return files


def get_pass_files(
    folders: List[str],
    root_dir: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> List[str]:
    """Get the pass files. The get__files methods are separated, because the folder structures are very different.

    Args:
        folders (List[str]): List of relevant folders. Should be obtained by get_folders.
        root_dir (str): Root dir of the folders.
        start_date (Optional[date], optional): Earliest date the files should match. Defaults to None.
        end_date (Optional[date], optional): Latest date the files should match. Defaults to None.

    Returns:
        List[str]: List of files matching the parameters.
    """
    result = []
    all_files = []
    for folder in folders:
        folder = root_dir + folder
        if not start_date and not end_date:
            for file in os.listdir(folder):
                if file.endswith(".txt"):
                    if file not in all_files:
                        all_files.append(file)
                        file_path = os.path.join(folder, file)
                        if os.path.isfile(file_path):
                            result.append(file_path)
        else:
            files = []
            if not start_date or not end_date:
                datetime = start_date or end_date
                date = datetime.date()
                files = _get_pass_file_by_date(date, folder=folder)
            else:
                date = start_date
                while date <= end_date:
                    files = files + _get_pass_file_by_date(date, folder=folder)
                    date = date + timedelta(days=1)
            if files:
                for file in files:
                    if file not in all_files:
                        all_files.append(file)
                        result.append(os.path.join(folder, file))

    return result


def get_files(
    folders: List[str] | str,
    system: Literal["tds", "tvs"],
    tcs_type: Literal["SlowControl", "TcsTrace"],
    root_dir: Optional[str] = None,
    start_datetime: Optional[datetime] = None,
    end_datetime: Optional[datetime] = None,
    area: Optional[Literal["G2", "G3", "O2"]] = None,
) -> List[str]:
    """Get the tcs trace and slowControl files. The get__files methods are separated, because the folder structures are very different.

    Args:
        folders (List[str] | str): Relevant folders to be searched.
        system (Literal['tds', 'tvs']): System the file should log.
        tcs_type (Literal['SlowControl', 'TcsTrace']): Type of file.
        root_dir (Optional[str], optional): Root dir of folders. Defaults to None.
         start_date (Optional[date], optional): Earliest datetime the files should match. Defaults to None.
        end_date (Optional[date], optional): Latest datetime the files should match. Defaults to None.
        area (Optional[Literal['G2', 'G3', 'O2']], optional): Area the files should be from. Defaults to None.

    Raises:
        Exception: No files found

    Returns:
        List[str]: List of files.
    """
    files = []
    files_found = []
    _folders = []
    if start_datetime > end_datetime:
        start_datetime, end_datetime = end_datetime, start_datetime
    date_delta = end_datetime.date() - start_datetime.date()
    if date_delta.days > 0:
        days = [
            start_datetime.date() + timedelta(days=i) for i in range(date_delta.days)
        ]
    else:
        days = [start_datetime.date()]
    if isinstance(folders, str):
        folders = folders.split(",")
    for folder in folders:
        if folder.find(area.lower()) != -1:
            _folders.append(folder)
    for day in days:
        for folder in _folders:
            if root_dir:
                folder = os.path.join(root_dir, folder)

            files = files + glob.glob(
                os.path.join(
                    folder,
                    tcs_type,
                    f"*{system.lower()}*{datetime.strftime(day, '%Y%m%d')}*",
                )
            )

    if len(files) == 1:
        return files
    if not files:
        raise Exception(
            r"No files found! make sure the files are in $root_dir/path {area}/(TcsTrace/SlowControl)/*"
        )
    file_dict = {}
    for i, timestamp in enumerate(re.findall(r"\d{8}-\d{6}", "".join(files))):
        file_dict[datetime.strptime(timestamp, "%Y%m%d-%H%M%S")] = files[i]
    timestamps = list(file_dict.keys())
    closest_start_datetime = 0
    closest_end_datetime = len(timestamps)
    for index, timestamp in enumerate(sorted(timestamps)):
        if timestamp < start_datetime:
            closest_start_datetime = index
        if timestamp > end_datetime:
            closest_end_datetime = index
            break

    timestamps = timestamps[closest_start_datetime:closest_end_datetime]
    for t in timestamps:
        files_found.append(file_dict[t])
    return files_found
