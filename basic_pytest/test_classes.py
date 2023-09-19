class SMAEMA():
    def __init__(self, symbol, SMA, EMA, start, end, tc):
        self.symbol = symbol
        self.SMA = SMA
        self.EMA = EMA
        self.start = start
        self.end = end
        self.tc = tc
        self.results = None

    def __repr__(self):
        return "SMAEMABacktester(symbol = {}, SMA = {}, EMA = {}, start = {}, end = {})".format(self.symbol, self.SMA, self.EMA, self.start, self.end)

    def get_data(self):
        ''' Retrieves and prepares the data.
        '''
        api = tpqoa.tpqoa("oanda.cfg")
        raw = api.get_history(instrument=self.symbol, start=self.start,
                              end=self.end, granularity="H1", price="A")
        raw = raw[["c"]]
        raw.rename(columns={"c": "Price"}, inplace=True)
        raw["Returns"] = np.log(raw / raw.shift(1))
        raw = raw.dropna()
        raw["SMA"] = raw["Price"].rolling(self.SMA).mean()
        raw["EMA"] = raw["Price"].ewm(span=self.EMA, min_periods=self.EMA).mean()
        pd.options.display.max_rows = 100
        print(raw)


def test_classes_compare():
    symbol_1 = SMAEMA("EUR_USD", 43, 36, "2020-01-01", "2023-09-01", .00007)
    symbol_2 = SMAEMA("EUR_USD", 43, 36, "2020-01-01", "2023-09-01", .00007)
    assert symbol_1.symbol == symbol_2.symbol


