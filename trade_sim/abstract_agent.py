from abc import ABC, abstractmethod
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AbstractTradeBot(ABC):
    name = "AbstractTradeBot"
    init_cash_sum = 1000
    current_cash_sum = 1000
    current_investment_sum = 0

    @abstractmethod
    def trade(self):
        pass

    @property
    def net_balance(self):
        return self.current_cash_sum + self.current_investment_sum
