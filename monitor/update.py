# -*- coding: utf-8 -*-
import rrdtool, time, multiprocessing
from getdeviceinfo import *
from snmpdate import *

def total_update(row, lock):
    node =  row[0]
    device = row[1]
    ip = row[2]
    ifoid = row[3]
    flow = total_flow(ip, ifoid)
    filename = 'uplinkflow/%s/%s_total.rrd' %(row[0], row[1])
    starttime=int (time.time ())
    curtime = time.strftime('%Y-%m-%d %X', time.localtime())
    if flow[0] != '' or flow[1] !='':
        update = rrdtool.updatev (str(filename), '%s:%s:%s' %  (str (starttime), str(flow[0]), str(flow[1])))
    with lock: 
        log = file('../log/rrdupdate.log', 'a+')
        if update['return_value'] == 0:
            log.write('updated success %s %s %s in:%s out:%s\n' % (curtime, starttime, device, str(flow[0]), str(flow[1])))
        else:
            log.write('updated fail %s %s %s in:%s out:%s\n' % (curtime, starttime, device, str(flow[0]), str(flow[1])))
        log.close()

def total_flow(ip, ifoid):
    inflowlist, outflowlist = [], []
    intotal, outotal = 0, 0
    for oid in ifoid.split(','):
        flow = port_flow(ip, oid)
        inflowlist.append(flow[0])
        outflowlist.append(flow[1])
    for inflow in inflowlist:
        intotal += int(inflow)
    for outflow in outflowlist:
        outotal += int(outflow)
    #为零是附空值，不知道初始为-1时是否可行
    if intotal == 0:
        intotal = ''
    if outotal == 0:
        outotal = ''
    return (intotal, outotal)


rows = CSW_uplink_info()
while True:
    lock = multiprocessing.Manager().Lock()
    p = multiprocessing.Pool(processes = 3)
    for row in rows:
        p.apply_async(total_update, (row, lock))
    p.close()
    time.sleep(300)
