import os
import csv
import pandas as pd
from helper import Helper


class StockPriceCsvModel():
    app_folder = os.path.dirname(os.path.realpath(__file__))
    database_folder = os.path.join(app_folder, 'database')
    
    # Save data to csv files
    @classmethod
    def save_stock_data_to_csv(cls, df):
        temp_df = df.copy()
        try:
            symbol = temp_df.iloc[0, 0]
            output_file = os.path.join(cls.database_folder, f'{symbol}.csv')
            temp_df['date'] = temp_df['date'].dt.strftime('%Y/%m/%d') # For Amibroker format
            temp_df.to_csv(output_file, index=False, header=None)
            print(f'Success: {symbol} Saved to CSV file')
        except Exception as e:
            print(f'Error: {symbol} Saved to CSV file. Detail: {e}')
    
    # Get list of stock that are need to be updated (not in database or not updated till the last working day)
    @classmethod
    def get_symbols_to_be_scraped(cls, full_symbol_list):
        # Get symbols not exist in the database
        symbols_exist = [os.path.splitext(file)[0] for file in os.listdir(cls.database_folder)]
        symbols_not_exist = [symbol for symbol in full_symbol_list if symbol not in symbols_exist]

        # Get symbols exist but not updated till the last working day
        symbols_exist_but_not_updated = []
        lwd = Helper.get_last_working_day()
        for filename in os.listdir(cls.database_folder):
            if filename.endswith('.csv'):
                try:
                    with open(os.path.join(cls.database_folder, filename), 'r') as f:
                        last_row = list(csv.reader(f))[-1] # Get the last row of csv file
                    if last_row[1] != lwd: # Check if the last date is equal to the last_working_day
                        symbols_exist_but_not_updated.append(os.path.splitext(filename)[0])
                except:
                    symbols_exist_but_not_updated.append(os.path.splitext(filename)[0])
        
        # Concat 2 lists and remove duplicates
        symbols_to_be_scraped = list(set(symbols_not_exist + symbols_exist_but_not_updated))
        symbols_to_be_scraped.sort()
        return symbols_to_be_scraped
    

# For testing purposes only
if __name__ == "__main__":
    data = {
        'symbol': ['AAPL', 'AAPL', 'AAPL'],
        'date': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'open': [150.0, 152.0, 154.0],
        'high': [155.0, 157.0, 159.0],
        'low': [149.0, 151.0, 153.0],
        'close': [152.0, 154.0, 156.0],
        'volume': [1000, 1200, 1100]
    }
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    StockPriceCsvModel.save_stock_data_to_csv(df)
    