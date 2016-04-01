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
import os
import os.path
import sys

sys.path.append(os.path.dirname(__file__))


class Hardware(object):
    @property
    def name(self):
        return self.__class__ \
            .__name__.lower()

    @property
    def exists(self):
        for device in self.devices:
            if os.path.isfile(str(device)):
                return True
        return False

    @property
    def is_powersave(self):
        raise NotImplementedError()

    @property
    def devices(self):
        raise NotImplementedError()

    def powersave(self):
        raise NotImplementedError()

    def perfomance(self):
        raise NotImplementedError()

    def _run(self, command):
        return os.popen(command).read()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __str__(self):
        raise NotImplementedError()


class Software(Hardware):
    @property
    def is_powersave(self):
        for device in self.devices:
            if os.path.isfile(device):
                if 'running' in self._run("%s status" % device):
                    return False
        return True

    def powersave(self):
        for device in self.devices:
            if os.path.isfile(device):
                yield "%s stop;" % device

    def devices(self):
        raise NotImplementedError()

    def perfomance(self):
        yield

    def __str__(self):
        raise NotImplementedError()
