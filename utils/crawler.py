import requests
import pandas as pd
import numpy as np
from tqdm import tqdm

def get_fund_k_history(fund_code: str, T: int = 90) -> pd.Series:
    '''

    Parameters
    ----------
    fund_code : 6 digit codes
    T : look back period

    Return
    ------
    pd.Series : historical daily log return
    '''
    # header
    EastmoneyFundHeaders = {
        'User-Agent': 'EMProjJijin/6.2.8 (iPhone; iOS 13.6; Scale/2.00)',
        'GTOKEN': '98B423068C1F4DEF9842F82ADF08C5db',
        'clientInfo': 'ttjj-iPhone10,1-iOS-iOS13.6',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'fundmobapi.eastmoney.com',
        'Referer': 'https://mpservice.com/516939c37bdb4ba2b1138c50cf69a2e1/release/pages/FundHistoryNetWorth',
    }
    # parameters
    data = {
        'FCODE': f'{fund_code}',
        'appType': 'ttjj',
        'cToken': '1',
        'deviceid': '1',
        'pageIndex': '1',
        'pageSize': f'{T}',
        'plat': 'Iphone',
        'product': 'EFund',
        'serverVersion': '6.2.8',
        'version': '6.2.8'
    }
    url = 'https://fundmobapi.eastmoney.com/FundMNewApi/FundMNHisNetList'
    json_response = requests.get(
        url, headers=EastmoneyFundHeaders, data=data).json()
    rows = []
    columns = ['date', 'unit_net_vale', 'cum_net_vale', 'returns']
    if json_response is None:
        return pd.DataFrame(rows, columns=columns)
    datas = json_response['Datas']
    if len(datas) == 0:
        return pd.DataFrame(rows, columns=columns)
    rows = []
    for stock in datas:
        date = stock['FSRQ']
        rows.append({
            'date': date,
            'unit_net_vale': stock['DWJZ'],
            'cum_net_vale': stock['LJJZ'],
            'returns': stock['JZZZL']
        })

    df = pd.DataFrame(rows)
    df['unit_net_vale'] = pd.to_numeric(df['unit_net_vale'], errors='coerce')

    df['cum_net_vale'] = pd.to_numeric(df['cum_net_vale'], errors='coerce')

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df.set_index('date', inplace=True)
    return df['returns']


def get_multiple_returns(codes: list[str], T: int=90) -> pd.DataFrame:
    '''

    Parameters
    ----------
    codes : list of fund codes
    T : look back period

    Return
    ------
    pd.DataFrame: historical return of funds
    '''
    df = []
    with tqdm(codes) as t:
        for code in t:
            df.append(get_fund_k_history(code, T))
            t.set_postfix({'fetching': code})
    df = pd.concat(df, axis=1)
    df.columns = codes
    df.replace('--', 0, inplace=True)
    df = df.astype(float)
    df = (df/100+1).apply(np.log)
    df.sort_index(inplace=True)
    return df.fillna(0)