import logging
import pytz
import logging
import datetime

from glob import glob


class Formatter(logging.Formatter):
    """override logging.Formatter to use an aware datetime object"""

    def converter(self, timestamp):
        # Create datetime in UTC
        dt = datetime.datetime.fromtimestamp(timestamp, tz=pytz.UTC)
        # Change datetime's timezone
        return dt.astimezone(pytz.timezone("Asia/Seoul"))

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        if datefmt:
            s = dt.strftime(datefmt)
        else:
            try:
                s = dt.isoformat(timespec="milliseconds")
            except TypeError:
                s = dt.isoformat()
        return s


def set_logger():
    """
    summary
        - 로깅 객체 및 포맷 정의
    """
    file_name = "logs/" + str(datetime.datetime.now()) + ".txt"
    logging.basicConfig(filename=file_name, level=logging.INFO)
    mylogger = logging.getLogger("process")
    mylogger.setLevel(logging.INFO)

    formatter = Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    mylogger.addHandler(stream_handler)

    return mylogger
