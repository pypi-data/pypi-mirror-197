# -*- coding: utf-8 -*-
import logging
import os
import datetime


class Logger(logging.Logger):
    
    __log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))
    __log_file = "log{0}.txt".format(
        datetime.datetime.now().strftime("%Y-%m-%d"))
    __log_path = os.path.join(__log_dir, "logs", __log_file)

    def __init__(self, logger_name="logger", level="DEBUG"):
        super().__init__(logger_name)
        self.setLevel(level)

        console_fmt = logging.Formatter(
            fmt="%(name)s--->%(levelname)s--->%(asctime)s--->%(message)s")
        file_fmt = logging.Formatter(
            fmt="%(lineno)d--->%(name)s--->%(levelname)s--->%(asctime)s--->%(message)s")

        file_handler = logging.FileHandler(
            self.__log_path, mode="a", encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(file_fmt)
        self.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(console_fmt)
        self.addHandler(console_handler)


if __name__ == "__main__":
    logger = Logger().debug("this is debug log info...")
