# Root class for objects that can be traded.
import numpy as np
import time


class QuoteSystem:

	# Could add a dictionary to map tradeables to quoteables.
	def __init__(self):
		pass

	def start(self):
		# start up the external quote system.
		pass

	@staticmethod
	def get_last_price(symbol):
		print(f"getting price for {symbol}")
		base = np.random.randint(low=10, high=200)
		offset = np.random.random()
		return round(base+offset, 4)


class Quotable:

	quote_system = QuoteSystem()
	quote_system.start()

	def __init__(self, name):
		self.symbol = name
		pass

	@classmethod
	def get_price(cls, symbol_):
		return cls.quote_system.get_last_price(symbol=symbol_)
	
	
class Tradeable(Quotable):

	def __init__(self, name):
		super().__init__(name)

	def buy(self, quantity, price, price_range):
		fill_price = self.get_price(self.symbol)
		if abs(fill_price - price) < price_range:
			# Could have it filled with a variable amount that depends on where
			# price is relative to price_range.
			return f"order filled at", fill_price, quantity
		else:
			return "", 0, 0


if __name__ == "__main__":
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
		time.sleep(.3)

		if dollars < 0 or quantity_ == 0:
			break

	print(f"\nFinal position is {position} and total dollars are {dollars}\n")
