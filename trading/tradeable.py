# Root class for objects that can be traded.
import numpy as np
import time
import json
import logging

QUOTEABLE_SYMBOLS = [r"^DJI", r"^IXIC", r"^SPX", "BAR"]
TRADEABLE_SYMBOLS = ["DIA", "QQQ", "SPY", "FOO"]

TtoQ_dict = {T: Q for (T, Q) in zip(TRADEABLE_SYMBOLS, QUOTEABLE_SYMBOLS) if T != "FOO"}


class QuoteSystem:

	# Could add a dictionary to map tradeables to quoteables.
	# Think about how to create just one quote system.
	def __init__(self):
		pass

	@staticmethod
	def start():
		# start up the external quote system.
		logging.info("Quote system has been started")

	@staticmethod
	def get_last_price(symbol: str):
		print(f"getting price for {symbol}")
		base = np.random.randint(low=10, high=200)
		offset = np.random.random()
		return round(base+offset, 4)


class Quotable:

	quote_system = QuoteSystem()
	quote_system.start()

	def __init__(self, name: str):
		self.symbol = name
		pass

	@classmethod
	def get_price(cls, symbol_: str):
		return cls.quote_system.get_last_price(symbol=symbol_)
	
	
class Tradeable(Quotable):

	def __init__(self, name: str):
		super().__init__(name)

	def buy(self, quantity: int, price: float, price_range: float):
		fill_price = self.get_price(self.symbol)
		if abs(fill_price - price) < price_range:
			# Could have it filled with a variable amount that depends on where
			# price is relative to price_range.
			return f"order filled at", fill_price, quantity
		else:
			return "", 0, 0


def get_configuration(config_file: str):

	with open(config_file, 'r') as fp_:
		data = json.load(fp_)

	return data


if __name__ == "__main__":

	configuration_file = "/home/dctodd/dev/python/toy-algorithms/trading/config.json"
	configuration = get_configuration(config_file=configuration_file)
	dc = {t: q for (t, q) in zip(configuration["tradeable"]["t_list"], configuration["quoteable"]["q_list"])}

	if dc["SPY"] == TtoQ_dict["SPY"]:
		print("Dictionaries look good!")

	position = 0
	dollars = 2000

	SP_500_index = Quotable(r"^SPX")
	SPY = Tradeable(r"SPY")

	quantity_ = 10
	price_ = 75
	range_ = 10

	for i in range(300):
		(msg, filled_price, filled_quantity) = SPY.buy(quantity=quantity_, price=price_, price_range=range_)
		if len(msg) > 0:
			print(msg + " " + str(filled_price) + " for " + str(filled_quantity) + " shares.")
			quantity_ = (quantity_ * 7) // 10
			price_ = (price_ * 9) // 10
			range_ = (range_ * 8) // 10
		else:
			print("Nothing filled")

		position += filled_quantity
		dollars -= filled_price * filled_quantity
		time.sleep(.003)

		if dollars < 0 or quantity_ == 0:
			break

	out_str = f"\nFinal position is {position} and total dollars are {dollars}\n"
	print(out_str)
	results_file = "/home/dctodd/dev/python/toy-algorithms/trading/results.txt"
	with open(results_file, 'w') as fp:
		fp.write(out_str)
