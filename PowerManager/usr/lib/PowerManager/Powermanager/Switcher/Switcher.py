__author__ = 'sensey'

from abc import ABCMeta, abstractmethod


class Switcher(metaclass=ABCMeta):
    @abstractmethod
    def powersave(self):
        pass

    @abstractmethod
    def perfomance(self):
        pass