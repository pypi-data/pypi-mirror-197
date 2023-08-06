import datetime
import logging
import logging.handlers
from pathlib import Path
from rich.logging import RichHandler


class Logarithm(logging.Logger):
    def __init__(self, name, level=logging.DEBUG):
        super().__init__(name, level)
        self.propagate = False
        """
        left align : [%(levelname)-8s]
        right align : [%(levelname)8s]
        """
        self.formatter = logging.Formatter(f"%(asctime)s [%(levelname)8s] --- %(message)s (%(filename)s:%(lineno)s)")
        self.levels = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL,
        }
        self.stream_handler(level="INFO")
        # self.rich_handler(level="INFO")
        self.rotate_file_handler(filename=f"{str(Path.home())}/.endoscopie/endoscopie.log",
                                 when='D',
                                 interval=1,
                                 backupCount=10,
                                 level="DEBUG")


    def stream_handler(self, level):
        stream = logging.StreamHandler()
        stream.setLevel(self.levels[level])
        stream.setFormatter(logging.Formatter("%(message)s"))
        self.addHandler(stream)


    def rich_handler(self, level):
        rich_handler = RichHandler()
        rich_handler.setLevel(self.levels[level])
        rich_handler.setFormatter(logging.Formatter("%(message)s"))
        self.addHandler(rich_handler)


    def file_handler(self, filename, mode, level):
        file = logging.FileHandler(filename=filename, mode=mode, encoding='utf-8')
        file.setLevel(self.levels[level])
        file.setFormatter(self.formatter)
        self.addHandler(file)


    def rotate_file_handler(self, filename, when, interval, backupCount, level):
        rotate = logging.handlers.TimedRotatingFileHandler(filename=filename,
                                                           when=when,
                                                           interval=interval,
                                                           backupCount=backupCount,
                                                           encoding='utf-8',
                                                           atTime=datetime.time(0, 0, 0))
        rotate.suffix = '%Y-%m-%d'
        rotate.setLevel(self.levels[level])
        rotate.setFormatter(self.formatter)
        self.addHandler(rotate)
