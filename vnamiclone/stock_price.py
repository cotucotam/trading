from datetime import datetime, timedelta
import requests
import pandas as pd


class StockPrice():
    # Get price data of a single symbol
    @classmethod
    def get_ohlcv_data(cls, symbol, type='stock', start_date='2000-01-01', end_date=datetime.today().strftime('%Y-%m-%d'), time_frame='1D', beautify=True, source='entrade'):
        """
        Get historical price data. The unit price is thousand VND.
        Parameters:
            symbol (str): ticker of a stock or index. Available indices are: VNINDEX, VN30, HNX, HNX30, UPCOM, VNXALLSHARE, VN30F1M, VN30F2M, VN30F1Q, VN30F2Q
            type (str): stock, index, or derivative. Default is 'stock'
            start_date (str): start date of the historical price data. Default is 2000-01-01
            end_date (str): end date of the historical price data. Default is today
            time_frame (str): time frame of the historical price data. Default is '1D' (daily), other options are '1' (1 min), '5' (5 mins), '15' (15 mins), '30' (30 mins), '1H' (hourly)
            beautify (bool): if True, convert OHLC to thousand VND for stock symbols (not for index). Default is True
            source (str): source of the data
        Returns:
            :obj:`pandas.DataFrame`:
            | symbol |    date    | open | high | low | close | volume |
            | ------ | ---------- | ---- | ---- | --- | ----- | ------ |
            |  XXXX  | YYYY-mm-dd | xxxx | xxxx | xxx | xxxxx | xxxxxx |
        """

        try:
            if source == 'entrade':
                df = cls.get_ohlcv_data_from_entrade(symbol, type, start_date, end_date, time_frame, beautify)
            
            if df is not None:
                df['symbol'] = symbol # Add symbol column
                df = df.reindex(columns=['symbol'] + list(df.columns[:-1])) # Rearrange columns
                df = df.drop_duplicates(subset=['symbol', 'date'])
                df['date'] = pd.to_datetime(df['date']) # Convert date string to pandas datetime
                df = df.sort_values('date')  # Sort the values in ascending order by 'date'
                df = df.reset_index(drop=True) # Reset the index
                return df
            else:
                return None
        except:
            return None

    # Get price data of a single symbol using Entrade API
    @classmethod
    def get_ohlcv_data_from_entrade(cls, symbol, type, start_date, end_date, time_frame, beautify):
        """
        Get historical price data from entrade.com.vn. The unit price is thousand VND.
        Parameters:
            symbol (str): ticker of a stock or index. Available indices are: VNINDEX, VN30, HNX, HNX30, UPCOM, VNXALLSHARE, VN30F1M, VN30F2M, VN30F1Q, VN30F2Q
            type (str): stock, index, or derivative.
            start_date (str): start date of the historical price data
            end_date (str): end date of the historical price data
            time_frame (str): time frame of the historical price data. Accepted options are '1D' (daily), '1' (1 min), '5' (5 mins), '15' (15 mins), '30' (30 mins), '1H' (hourly)
            beautify (bool): if True, convert OHLC to thousand VND for stock symbols (not for index)
        Returns:
            :obj:`pandas.DataFrame`:
            |    date    | open | high | low | close | volume |
            | ---------- | ---- | ---- | --- | ----- | ------ |
            | YYYY-mm-dd | xxxx | xxxx | xxx | xxxxx | xxxxxx |
        """

        # Convert input to the accepted format for calling API
        end_date = (datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d') # Add one more day to end_date
        # Convert start_date, end_date to timestamp
        from_timestamp = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp())
        to_timestamp = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp())
        # If time_frame is not 1D, then calculate the start date that is last 90 days from the end date
        if time_frame != '1D':
            new_from_timestamp = to_timestamp - 90 * 24 * 60 * 60
            # If new_from_timestamp > from_timestamp, then print a notice to user that data is limit to 90 days
            if new_from_timestamp > from_timestamp:
                from_timestamp = new_from_timestamp
                print('Warning: Data is limited to the last 90 days for all time_frame in minutes')
        
        # Get data from API
        url = f'https://services.entrade.com.vn/chart-api/v2/ohlcs/{type}?from={from_timestamp}&to={to_timestamp}&symbol={symbol}&resolution={time_frame}'
        headers = {
            'authority': 'services.entrade.com.vn',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'dnt': '1',
            'origin': 'https://banggia.dnse.com.vn',
            'referer': 'https://banggia.dnse.com.vn/',
            'sec-ch-ua': '"Edge";v="114", "Chromium";v="114", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1788.0'
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            df = pd.DataFrame(response_data)
            df['t'] = pd.to_datetime(df['t'], unit='s') # Convert timestamp to datetime
            df = df.rename(columns={'t': 'date', 'o': 'open', 'h': 'high', 'l': 'low', 'c': 'close', 'v': 'volume'}).drop(columns=['nextTime']) # Rename columns
            df['date'] = df['date'].dt.tz_localize('UTC').dt.tz_convert('Asia/Ho_Chi_Minh') # Convert timezone
            # If time_frame is 1D, then convert time to date
            if time_frame == '1D':
                df['date'] = df['date'].dt.date
            # If type=stock and beautify=True, then convert OHLC to thousand VND, elif type=index then keep it as it is
            if type == 'stock' and beautify == True:
                df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']] * 1000
                df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']].astype(int) # Convert OHLC to integer
            if len(df) > 0:
                print(f'Success: {symbol} Scraped data till {df["date"].iloc[-1]}')
                return df
            else:
                print(f'Error: Empty data of {symbol} from Entrade')
                return None
        else:
            print(f'Error: Cound not get data of {symbol} from Entrade - Status code {response.status_code}')
            return None


# For testing purposes only
if __name__ == "__main__":
    data = StockPrice.get_ohlcv_data("HPG")
    print(data)

    data = StockPrice.get_ohlcv_data("VNINDEX", type='index')
    print(data)
    