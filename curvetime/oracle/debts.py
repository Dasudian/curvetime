from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django_redis import get_redis_connection
from curvetime.db.serializer import DebtFeatureSerializer
from curvetime.db.models import DebtFeature, Debts
from .cn_debts import rest_rule
import json, time



class StockOracle:
    def __init__(self):
        self.stocks = Debts.objects.all()
        self.stocks = [s.code for s in self.stocks]

    def get_dataframe(self, frame_count, window_size, type='train', f=None):
        if type == 'train':
            return get_df(frame_count, window_size, f)
        else:
            rest_rule(3)
            conn = get_redis_connection('default')
            if f:
                return json.loads(conn.get('DEBT_FRAME_' + str(f)))
            else:
                return json.loads(conn.get('DEBT_FRAME'))



def get_frame(row=10, page=1, f=None):
    if f == 2:
        f = DebtFeature.objects.all()
    else:
        f = DebtFeature.objects.all()
    paginator = Paginator(f, row)
    try:
        p = paginator.page(page)
    except PageNotAnInteger:
        p = paginator.page(1)
    except EmptyPage:
        p = paginator.page(paginator.num_pages)

    if f == 2:
        p = [DebtFeatureSerializer(x).data['frame'] for x in p]
    else:
        p = [DebtFeatureSerializer(x).data['frame'] for x in p]
    return {'data': p, 'total': paginator.count}


def get_df(frame_count=1, window_size=10, f=None):
    total = get_frame(f=f)['total']
    if frame_count > total - window_size + 1:
        return None
    page1 = (frame_count-1) // window_size + 1
    page2 = page1 + 1
    frame1 = get_frame(window_size, page1, f)
    frame2 = get_frame(window_size, page2, f)
    frame1 = frame1['data']
    frame2 = frame2['data']
    frame = frame1 + frame2
    start = (frame_count-1) % window_size
    end = (frame_count-1) % window_size + window_size
    return frame[start:end]


def f_to_2():
    f = DebtFeature.objects.all()
    for ff in f:
        new_frame = []
        frame = json.loads(ff.frame)
        for r in frame:
            row = [r[0], r[1], r[2], r[7]]
            new_frame.append(row)
        o = DebtFeature2(time = ff.time, frame =json.dumps(new_frame))
        o.save()


