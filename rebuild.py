import scipy.signal
from gps_trans import distance


def all_active(DIVER):
    _x = 0.0
    _y = 0.0
    for p in DIVER:
        DIVER[p] = True
        x, y = p.split(',')
        x = float(x)
        y = float(y)
        _x += x
        _y += y
    return _x / len(DIVER), _y / len(DIVER)


def get_next(x, y, DIVER):
    dis_list = list()
    for p in DIVER:
        if not DIVER[p]:
            continue
        _x, _y = p.split(',')
        _x = float(_x)
        _y = float(_y)
        dis_list.append([p, distance(_y, _x, y, x)])

    return sorted(dis_list, key=lambda v: v[1])


def get_edge_point(DIVER):
    MAX_STEP = 999999999
    sx, sy = all_active(DIVER)
    while True:
        dis = get_next(sx, sy, DIVER)
        if len(dis) == 0 or dis[0][1] > MAX_STEP:
            break
        DIVER[dis[0][0]] = False
        sx, sy = dis[0][0].split(',')
        sx = float(sx)
        sy = float(sy)
        MAX_STEP = 500
    all_active(DIVER)
    return sx, sy


def rebuild_line(sx, sy, DIVER, GAP):
    line_x = list()
    line_y = list()

    now_lx = [sx]
    now_ly = [sy]
    while True:
        dis = get_next(sx, sy, DIVER)
        if len(dis) == 0:
            break

        if dis[0][1] > GAP:
            line_x.append(now_lx)
            line_y.append(now_ly)
            now_lx = list()
            now_ly = list()

        DIVER[dis[0][0]] = False
        sx, sy = dis[0][0].split(',')
        sx = float(sx)
        sy = float(sy)
        now_lx.append(sx)
        now_ly.append(sy)

    line_x.append(now_lx)
    line_y.append(now_ly)
    line_x = filter(lambda l: len(l) > 10, line_x)
    line_y = filter(lambda l: len(l) > 10, line_y)
    line_x = [scipy.signal.savgol_filter(l, 5, 3) for l in line_x]
    line_y = [scipy.signal.savgol_filter(l, 5, 3) for l in line_y]
    return line_x, line_y
