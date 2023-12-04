import pandas as pd
from helper import Helper
from stock_price import StockPrice
from company_info import CompanyInfo
from csv_model import StockPriceCsvModel


class StockPriceScraper():
    @staticmethod
    def scrape():
        # Stock list
        stock_list = CompanyInfo.get_stock_list_from_ssi()['symbol'].to_list()
        stock_df = pd.DataFrame(stock_list, columns=['symbol'])
        stock_df['type'] = 'stock'
        # Index list
        index_list = ['VNINDEX', 'VN30', 'HNX', 'HNX30', 'UPCOM', 'VNXALLSHARE']
        index_df = pd.DataFrame(index_list, columns=['symbol'])
        index_df['type'] = 'index'
        # Concat dataframes
        symbol_df = pd.concat([stock_df, index_df], ignore_index=True)
        
        # Statistics
        print(f'Total number of symbols: {len(symbol_df)}')
        symbols_to_be_scraped_list = StockPriceCsvModel.get_symbols_to_be_scraped(symbol_df['symbol'].to_list())
        symbol_df = symbol_df[symbol_df['symbol'].isin(symbols_to_be_scraped_list)]
        print(f'The number of symbols that need to be scraped: {len(symbol_df)}')
        
        # Scrape data
        tasks = [(StockPrice.get_ohlcv_data, (row['symbol'], row['type'])) for index, row in symbol_df.iterrows()]
        result = Helper.execute_thread_pool(tasks)
        result = [x for x in result if x is not None] # Remove items that are None
        
        # Save data to CSV files
        for df in result:
            StockPriceCsvModel.save_stock_data_to_csv(df)


# For testing purposes only
if __name__ == "__main__":
    Helper.measure_time(StockPriceScraper.scrape)
    