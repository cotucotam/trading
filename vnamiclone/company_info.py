import requests
import pandas as pd


class CompanyInfo():
    @staticmethod
    def get_stock_list_from_ssi(lang='vi'):
        """
        Get all available stock symbols from SSI API.
        Parameters:
            lang (str): language of the data. Default is 'vi', other options are 'en'
        """
        
        url = f'https://fiin-core.ssi.com.vn/Master/GetListOrganization?language={lang}'
        headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
            'DNT': '1',
            'sec-ch-ua-mobile': '?0',
            'X-Fiin-Key': 'KEY',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Fiin-User-ID': 'ID',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
            'X-Fiin-Seed': 'SEED',
            'sec-ch-ua-platform': 'Windows',
            'Origin': 'https://iboard.ssi.com.vn',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://iboard.ssi.com.vn/',
            'Accept-Language': 'en-US,en;q=0.9,vi-VN;q=0.8,vi;q=0.7'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data['items'])
            df['comGroupCode'].loc[df['comGroupCode'] == 'UpcomIndex'] = 'UPCOM'
            df['comGroupCode'].loc[df['comGroupCode'] == 'HNXIndex'] = 'HNX'
            df['comGroupCode'].loc[df['comGroupCode'] == 'VNINDEX'] = 'HOSE'
            df = df.rename(columns={'ticker': 'symbol', 'organName': 'full_name', 'comGroupCode': 'exchange'}) # Rename columns
            df = df[['symbol', 'full_name', 'exchange']]
            df = df.sort_values('symbol', ascending=True)
            df = df.reset_index(drop=True)
            return df
        else:
            print('Error in API response', response.text)


# For testing purposes only
if __name__ == "__main__":
    df = CompanyInfo.get_stock_list_from_ssi()
    print(df)
    