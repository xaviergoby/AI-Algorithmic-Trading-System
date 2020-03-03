## Trading Simulation Work/Process Flow/Steps:

__Stage I: TradingSimulator Initialisation (Instantiation)__

Via e.g.: sim = TradingSimulator(stock_symbols_list, trade_bots_num)

Requirements:
1) A list of stock symbols.
2) The # of trade bots to generate.
3) A specific trading strategy.
4) A source for the (historical) market data e.g. YahooStockDataFeed()

Jobs:
1) Initialisation of the trading simulation.
2) Retrieval of necessary stock market data from the provided data source
3) Generation of a population of trade bots.
4) Supplying of updated market data to all trade bots at for each 
tick/heartbeat of the market.





