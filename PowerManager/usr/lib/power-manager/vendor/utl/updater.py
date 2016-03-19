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
import time
from threading import Thread


class BackgroundUpdater(Thread):
    _dispatcher = []

    @property
    def dispatcher(self):
        return self._dispatcher

    @dispatcher.setter
    def dispatcher(self, dispatcher):
        self._dispatcher = dispatcher

    def run(self):
        while 1:
            time.sleep(10)
            event = self._dispatcher.new_event()
            self._dispatcher.dispatch('indicator.refresh', event)

