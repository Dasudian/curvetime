from db.models import Stocks, StockPrice, StockFeature
import pandas as pd
import requests, time, json
from utils.utils import timestamp_to_utc, is_weekend
from multiprocessing import Pool
from django_redis import get_redis_connection
from app.celery import app
from curvetime.env.stock_env import WINDOW_SIZE


def parse_stocks(file='data/stocks.xlsx', header=None):
    df = pd.read_excel(file)
    for rowIndex, row in df.iterrows():
        for columnIndex, value in row.items():
            if value == 'nan':
                continue
            try:
                name = value.split('(')
                code = name[1].split(')')[0]
                name = name[0]
                if code[0] == '6':
                    code = 'sh' + code
                else:
                    code = 'sz' + code
                stock = Stocks(name=name, code=code)
                stock.save()
            except Exception:
                continue


def get_latest_df():
    while True:
        if is_weekend():
            time.sleep(60*60)
            continue
        now = time.time()
        now = timestamp_to_utc(now)
        hour = int(now[11:13])
        minute = int(now[14:16])
        if hour == 9 and minute < 30:
            time.sleep(10*60)
            continue
        if hour < 9 or hour >= 15:
            time.sleep(30*60)
            continue
        if hour == 12:
            time.sleep(10*60)
            continue
        if hour == 11 and minute > 30:
            time.sleep(10*60)
            continue
        conn = get_redis_connection('default')
        df = conn.get('STOCK_FRAME')
        if df is None:
            continue
        else:
            df = json.loads(df)
            return df



def fetch_price(period=5):
    codes = Stocks.objects.all()
    codes = sorted([c.code for c in codes])
    codes = [(c, [0]*29) for c in codes]
    total = len(codes)
    conn = get_redis_connection('default')
    while True:
        if is_weekend():
            time.sleep(60*60)
            continue
        now = time.time()
        now = timestamp_to_utc(now)
        hour = int(now[11:13])
        minute = int(now[14:16])
        if hour == 9 and minute < 30:
            time.sleep(10*60)
            continue
        if hour < 9 or hour >= 15:
            time.sleep(30*60)
            continue
        if hour == 12:
            time.sleep(10*60)
            continue
        if hour == 11 and minute > 30:
            time.sleep(10*60)
            continue
        codes = [batch_price(c[0], now, c[1]) for c in codes]
        data = [c[1] for c in codes]
        df = conn.get('STOCK_FRAME')
        if df is None:
            conn.set('STOCK_FRAME', json.dumps([data]))
        else:
            df = json.loads(df)
            if len(df) < WINDOW_SIZE:
                df.append(data)
            else:
                df = df[1:]
                df.append(data)
            conn.set('STOCK_FRAME', json.dumps(df))
        feature = Feature(time=now, frame=json.dumps(data))
        feature.save()
        #time.sleep(period*60)
        print('-----one round-----')
        break




@app.task
def batch_price(code, time, old):
    data = get_stock(code)
    if data is None or len(data) != 29:
        data = old
    else:
        data = [float(d) for d in data]
    return code, data


def get_stock(code):
    try:
        header = {'Referer':'https://finance.sina.com.cn'}
        res = requests.get('https://hq.sinajs.cn/list=' + code, headers=header)
        if res.status_code == 200:
            data = res.text.split(',')
            return data[1:30]
        else:
            return None
    except Exception:
        return None


def save_price(data, code, time):
    if len(data) < 29:
        return
    data = Price(open = data[0],
            close = data[1],
            price = data[2],
            high = data[3],
            low = data[4],
            ask = data[5],
            bid = data[5],
            volume = data[7],
            amount = data[8],
            ask_v1 = data[9],
            ask1 = data[10],
            ask_v2 = data[11],
            ask2 = data[12],
            ask_v3 = data[13],
            ask3 = data[14],
            ask_v4 = data[15],
            ask4 = data[16],
            ask_v5 = data[17],
            ask5 = data[18],
            bid_v1 = data[19],
            bid1 = data[20],
            bid_v2 = data[21],
            bid2 = data[22],
            bid_v3 = data[23],
            bid3 = data[24],
            bid_v4 = data[25],
            bid4 = data[26],
            bid_v5 = data[27],
            bid5 = data[28],
            code = code,
            time = time)
    data.save()


def rest_rule(period=2):
    while True:
        if is_weekend():
            time.sleep(60*60)
            continue
        now = time.time()
        now = timestamp_to_utc(now)
        hour = int(now[11:13])
        minute = int(now[14:16])
        if hour == 9 and minute < 30:
            time.sleep(10*60)
            continue
        if hour < 9 or hour >= 15:
            time.sleep(30*60)
            continue
        if hour == 12:
            time.sleep(10*60)
            continue
        if hour == 11 and minute > 30:
            time.sleep(10*60)
            continue
        time.sleep(period*60)
        print('-----one round-----')
        break
