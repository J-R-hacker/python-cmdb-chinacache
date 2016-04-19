# -*- coding: utf-8 -*-
import rrdtool, time, os
from getdeviceinfo import *

#给端口创建一个in、out的rrd数据库
def create_flow(filename):
    cur_time=str (int (time.time ()))
    rrd = rrdtool.create(filename, '--step', '300', '--start', cur_time,
                        'DS:ifin:COUNTER:600:0:U',
                        'DS:ifout:COUNTER:600:0:U',
                        'RRA:AVERAGE:0.5:1:600',
                        'RRA:AVERAGE:0.5:6:700',
                        'RRA:AVERAGE:0.5:24:775',
                        'RRA:AVERAGE:0.5:288:797',
                        'RRA:MAX:0.5:1:600',
                        'RRA:MAX:0.5:6:700',
                        'RRA:MAX:0.5:24:775',
                        'RRA:MAX:0.5:444:797',
                        'RRA:MIN:0.5:1:600',
                        'RRA:MIN:0.5:6:700',
                        'RRA:MIN:0.5:24:775',
                        'RRA:MIN:0.5:444:797')
    if rrd:
        return rrdtool.error()

def uplink():
    rows = CSW_uplink_info()
    for row in rows:
        if not os.path.exists('uplinkflow/%s' %row[0]):
            os.mkdir('uplinkflow/%s' %row[0])
        if not os.path.exists('uplinkflow/%s/%s_total.rrd' %(row[0], row[1])):
            filename = 'uplinkflow/%s/%s_total.rrd' %(row[0], row[1])
            create_flow(str(filename))

uplink()
