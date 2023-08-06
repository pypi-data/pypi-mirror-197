from datetime import datetime
from time import time

from proscan_log_api.pass_log_client import PassClient
from proscan_log_api.slow_control_client import SlowControlClient
from proscan_log_api.tcs_trace_client import TcsTraceClient


def slow_control_example():
    """A simple example for the Slow Control Client, measuring timing of execution, length of return and logs."""
    start = time()
    slow_logs = SlowControlClient(root_dir="/mnt/tcs_logs/")
    logs = slow_logs.get(
        system="tvs",
        folders="g2prod/production/VxWorks/Log/,g3prod/production/VxWorks/Log/,o2prod/production/VxWorks/Log/",
        start_datetime=datetime(
            year=2023, month=2, day=22, hour=1, minute=0, microsecond=741000
        ),
        end_datetime=datetime(
            year=2023, month=2, day=23, hour=3, minute=0, microsecond=741000
        ),
        area="G2",
    )
    print("execution time: ", time() - start)
    print(len(logs))
    print(logs)


def tcs_trace_example():
    """A simple example for the TCS Trace Client, measuring timing of execution, length of return and logs."""
    start = time()
    trace_logs = TcsTraceClient(root_dir="/mnt/tcs_logs/")
    logs = trace_logs.get(
        system="tds",
        folders="g2prod/production/VxWorks/Log/,g3prod/production/VxWorks/Log/,o2prod/production/VxWorks/Log/",
        start_datetime=datetime(
            year=2022,
            month=12,
            day=1,
            hour=10,
        ),
        end_datetime=datetime(
            year=2022,
            month=12,
            day=1,
            hour=11,
        ),
        area="G2",
    )
    print("Excecution time: ", time() - start)
    print(len(logs))
    print(logs)


from pprint import pprint


def pass_log_example():
    """A simple example for the PASS Client, measuring timing of execution, length of return and logs."""
    PASS_LOG_DATA_DIR_ROOT = "/mnt/proscan-fs/"
    PASS_LOG_DATA_FOLDERS = (
        "PG2TC1-VME-PASS,PG3TC2-VME-PASS,PMPTC1-VME-PASS,PO2TC1-VME-PASS,"
    )
    api = PassClient(root_dir=PASS_LOG_DATA_DIR_ROOT, folders=PASS_LOG_DATA_FOLDERS)
    start = time()
    result = api.get(
        area="G2",
        # timestamp=1677020491.722127,
        end_datetime=datetime(year=2023, month=1, day=3),
        start_datetime=datetime(year=2023, month=1, day=3),
    )

    logs = [r for r in result]
    print("Excecution time: ", time() - start)
    print(len(logs))
    pprint(logs)


if __name__ == "__main__":
    # Uncomment the example you want to run.
    # slow_control_example()
    # tcs_trace_example()
    pass_log_example()
    pass
