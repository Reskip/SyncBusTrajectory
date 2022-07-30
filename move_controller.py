import time
import copy
from gps_trans import gcj02_to_wgs84, distance, mps_to_kmph
from location import set_location


class Move(object):
    def __init__(self, line_x, line_y, step=0.00005):
        self.now_lat = None
        self.now_lng = None

        self.lat_que = copy.deepcopy(line_x)
        self.lng_que = copy.deepcopy(line_y)
        self.total_point_cnt = len(self.lat_que)
        self.step = step
        self.eps = 0.00000001
        self.xs = list()
        self.ys = list()
        self.total_dis = 0.0
        self.start_time = None

    def do_move(self):
        if len(self.lat_que) == 0:
            return
        if self.start_time is None:
            self.start_time = time.time()
        if self.now_lat is None:
            self.now_lat = self.lat_que[0]
            self.now_lng = self.lng_que[0]

        _lat = self.lat_que[0]
        _lng = self.lng_que[0]
        if abs(_lat-self.now_lat) + abs(_lng-self.now_lng) < self.eps:
            self.lat_que = self.lat_que[1:]
            self.lng_que = self.lng_que[1:]
            return
        lat_delta = _lat - self.now_lat
        lng_delta = _lng - self.now_lng
        norm = (lat_delta ** 2 + lng_delta ** 2) ** 0.5

        e_step = min(self.step, norm)
        new_lat = self.now_lat + lat_delta * e_step / norm
        new_lng = self.now_lng + lng_delta * e_step / norm
        self.total_dis += distance(new_lng, new_lat, self.now_lng, self.now_lat)
        self.now_lat = new_lat
        self.now_lng = new_lng

        self.xs.append(new_lat)
        self.ys.append(new_lng)
        _xs, _ys = gcj02_to_wgs84(self.xs[-1], self.ys[-1])
        set_location(str(_ys)+' '+str(_xs))
        return self.ys[-1], self.xs[-1]

    def move_end(self):
        return len(self.lat_que) == 0

    def progress(self):
        remain = len(self.lat_que)
        return "{a} / {b}".format(a=self.total_point_cnt-remain, b=self.total_point_cnt)

    def speed(self):
        work_time = time.time() - self.start_time
        return mps_to_kmph(self.total_dis / work_time)
