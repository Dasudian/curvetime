from curvetime.db.models import Debts, DebtFeature
from curvetime.utils.utils import timestamp_to_utc, is_weekend
import pandas as pd
import requests, time, json
from multiprocessing import Pool
from django_redis import get_redis_connection
from app.celery import app
#from curvetime.env.stock_env import WINDOW_SIZE
WINDOW_SIZE = 48 * 10  #10-days data


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
                stock = Debts(name=name, code=code)
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
        df = conn.get('DEBT_FRAME')
        if df is None:
            continue
        else:
            df = json.loads(df)
            return df



def fetch_price(period=2):
    codes = Debts.objects.all()
    codes = [c.code for c in codes]
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
        df = conn.get('DEBT_FRAME')
        if df is None:
            conn.set('DEBT_FRAME', json.dumps([data]))
        else:
            df = json.loads(df)
            if len(df) < WINDOW_SIZE:
                df.append(data)
            else:
                df = df[1:]
                df.append(data)
            conn.set('DEBT_FRAME', json.dumps(df))
        feature = DebtFeature(time=now, frame=json.dumps(data))
        feature.save()
        #pack_instant_data(F2_WINDOW_SIZE)
        time.sleep(period*60)
        print('-----one round for fetching debts prices-----')



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


def pack_instant_data(window_size, f=2):
    conn = get_redis_connection('default')
    df = conn.get('DEBT_FRAME')
    if not df:
        df = DebtFeature.objects.all().order_by('-time')[:window_size]
        df = list(reversed(df))
        df = [json.loads(dd.frame) for dd in df]
        if not f:
            conn.set('DEBT_FRAME', json.dumps(df))
    else:
        df = json.loads(df)
        if not f:
            latest = DebtFeature.objects.last()
            latest = json.loads(latest.frame)
            df = df[1:]
            df.append(latest[0])
            conn.set('DEBT_FRAME', json.dumps(df))
        else:
            latest = df[-1]
            df = conn.get('DEBT_FRAME_' + str(f))
            if not df:
                df = DebtFeature.objects.all().order_by('-time')[:window_size]
                df = list(reversed(df))
                df = [json.loads(dd.frame) for dd in df]
                new_df = []
                for frame in df:
                    new_frame = []
                    for r in frame:
                        row = [r[0], r[1], r[2], r[7]]
                        new_frame.append(row)
                    new_df.append(new_frame)
                conn.set('DEBT_FRAME_'+str(f), json.dumps(new_df))
            else:
                df = json.loads(df)
                new_frame = []
                for r in latest:
                    row = [r[0], r[1], r[2], r[7]]
                    new_frame.append(row)
                df = df[1:]
                df.append(new_frame)
                conn.set('DEBT_FRAME_'+str(f), json.dumps(df))
