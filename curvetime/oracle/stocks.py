from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django_redis import get_redis_connection
from curvetime.db.serializer import StockFeatureSerializer
from curvetime.db.models import StockFeature, Stocks
from curvetime.env.stock_env import WINDOW_SIZE
import json



class StockOracle:
    def __init__(self, window_size=WINDOW_SIZE):
        self.window_size = window_size
        self.stocks = Stocks.objects.all()
        self.stocks = sorted([s.code for s in self.stocks])

    def get_dataframe(self, frame_count, type='train'):
        if type == 'train':
            return get_df(frame_count, self.window_size)
        else:
            conn = get_redis_connection('default')
            return json.loads(conn.get('STOCK_FRAME'))



def get_frame(row=10, page=1):
    f = StockFeature.objects.all()
    paginator = Paginator(f, row)
    try:
        p = paginator.page(page)
    except PageNotAnInteger:
        p = paginator.page(1)
    except EmptyPage:
        p = paginator.page(paginator.num_pages)

    p = [StockFeatureSerializer(x).data['frame'] for x in p]
    return {'data': p, 'total': paginator.count}


def get_df(frame_count=1, window_size=10):
    total = get_frame()['total']
    if frame_count > total - window_size + 1:
        return None
    page1 = (frame_count-1) // window_size + 1
    page2 = page1 + 1
    frame1 = get_frame(window_size, page1)
    frame2 = get_frame(window_size, page2)
    frame1 = frame1['data']
    frame2 = frame2['data']
    frame = frame1 + frame2
    start = (frame_count-1) % window_size
    end = (frame_count-1) % window_size + window_size
    return frame[start:end]