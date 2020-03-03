from abc import ABC, abstractmethod


class AbstractBaseStrategy(ABC):

	name = "AbstractBaseStrategy"

	# @abstractmethod
	# def _generate_signal(self, data):
	# 	raise NotImplementedError
	
	# @abstractmethod
	# def _generate_all_stocks_signals(self):
	# 	raise NotImplementedError