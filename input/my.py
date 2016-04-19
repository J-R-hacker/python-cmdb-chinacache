# -- coding:utf-8 --
import MySQLdb
import os, commands
from IPy import IP
#获取核心设备的上联端口信息
def info():
    conn=MySQLdb.connect(host='localhost',user='root',passwd='111111',db='device',port=3306,charset="utf8")
    cur=conn.cursor()
    conn.select_db('device')
    cur.execute(''' select *
                    from device_device''')
    rows = cur.fetchall()
    conn.close()
    return rows

def wrdb(ip, manu_id):
    conn=MySQLdb.connect(host='localhost',user='root',passwd='111111',db='device',port=3306,charset="utf8")
    cur=conn.cursor()
    conn.select_db('device')
    print "update  device_device set manu_id=%s where device_ip='%s';" %(manu_id, ip)
    n = cur.execute("update device_device set manu_id='%s' where device_ip='%s'" %(manu_id, ip))
    conn.commit()
    conn.close()

rows = info()
for row in rows:
    ip = row[2]
    print ip
    if IP(ip).iptype() == 'PRIVATE':continue
    (status, result) = commands.getstatusoutput('snmpwalk -v2c -c %s %s %s' %("ChinaCache", ip, "sysDescr.0"))
    result = result.split('STRING:')[-1].strip()
    if 'S6700-24-EI' in result:
        manu_id = 3
    elif 'CE5810-48T4S-EI' in result:
        manu_id = 2
    elif 'n7000' in result:
        manu_id = 5
    elif 'ex3300-48t' in result:
        manu_id = 4
    elif 'C2960X' in result:
        manu_id = 6
    elif 'CE12800' in result:
        manu_id = 7
    else:
        manu_id = 1
    wrdb(ip, manu_id)
