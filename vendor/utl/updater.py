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
from apscheduler.schedulers.background import BackgroundScheduler
import time

class BackgroundUpdater(object):
    _interval = None
    _dispatcher = None
    _logger = None
    _scheduler = None

    def __init__(self, dispatcher, interval):
        self._logger = getLogger('updater')
        self._dispatcher = dispatcher
        self._scheduler = BackgroundScheduler()
        self._scheduler.add_job(self.on_interval_tick, 'interval', seconds=2)

    def on_interval_tick(self):
        event = self._dispatcher.new_event()
        self._dispatcher.dispatch('indicator.refresh', event)
        self._logger.debug('indicator.refresh: %s' % time.time())

    def start(self):
        self._scheduler.start()
