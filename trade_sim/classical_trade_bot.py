from trade_sim.abstract_agent import AbstractTradeBot
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ClassicalTradeBot(AbstractTradeBot):

    name = "ClassicalTradeBot"

    def __init__(self, signal):
        self.signal = signal

    def trade(self):
        for time_step in range(len(self.signal)):
            logger.info("Current signal: {0}".format(time_step))
            if self.signal[time_step] == 0:
                print("Holding")
            elif self.signal[time_step] == 1:
                print("Buying")
                self.current_cash_sum = self.current_cash_sum - 100
                self.current_investment_sum = self.current_investment_sum + 100
            else:
                print("Selling")
                self.current_cash_sum = self.current_cash_sum + 200
                self.current_investment_sum = self.current_investment_sum - 100
        self.performance()


    def performance(self):
        print("{0} final cash sum (not incl. value of remaining open orders): {1}".format(self.name, self.current_cash_sum))