# Copyright 2015 Alex Woroschilow (alex.woroschilow@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from logging import *
from logging.handlers import RotatingFileHandler


class ServiceLogger(object):
    def __init__(self):
        handler = RotatingFileHandler(filename='/var/log/powermanager.log', maxBytes=(1024 * 100), backupCount=3)
        handler.setFormatter(Formatter('%(levelname)s;%(asctime)s;%(message)s'))

        self.__logger = Logger("powermanager")
        self.__logger.setLevel(INFO)
        self.__logger.addHandler(handler)
        pass

    def on_loaded(self, event, dispatcher):
        self.__logger.debug("[ServiceLogger] on_loaded")
        pass

    def on_started(self, event, dispatcher):
        self.__logger.debug("[ServiceLogger] on_started")
        pass

    def debug(self, message):
        self.__logger.debug(message)
        pass

    def info(self, message):
        self.__logger.info(message)
        pass

    def warning(self, message):
        self.__logger.warning(message)
        pass

    def error(self, message):
        self.__logger.error(message)
        pass

    def fatal(self, message):
        self.__logger.fatal(message)
        pass
