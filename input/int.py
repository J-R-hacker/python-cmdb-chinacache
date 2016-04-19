# -- coding:utf-8 --
import MySQLdb
import os, commands
from IPy import IP
#获取核心设备的上联端口信息
def info():
    conn=MySQLdb.connect(host='118.123.6.162',user='wangxc',passwd='111111',db='device',port=48001,charset="utf8")
    cur=conn.cursor()
    conn.select_db('device')
    cur.execute(''' select *
                    from device_device''')
    rows = cur.fetchall()
    conn.close()
    return rows

def wrdb(if_name, device_id, if_OID):
    conn=MySQLdb.connect(host='118.123.6.162',user='wangxc',passwd='111111',db='device',port=48001,charset="utf8")
    cur=conn.cursor()
    n = cur.execute("INSERT INTO device_interface (if_name, device_id, if_OID) VALUES (%s, %s, %s)" %(if_name, device_id, if_OID))
    conn.commit()
    conn.close()

rows = info()
conn.select_db('device')
for row in rows:
    ip = row[2]
    print ip
    if IP(ip).iptype() == 'PRIVATE':continue
    (status, result) = commands.getstatusoutput('snmpwalk -v2c -c %s %s %s' %("ChinaCache", ip, "IfDescr"))
    if "Timeout" in result:continue
    if_rows = result.split("\n")
    device_id = row[0]
    for if_row in if_rows:
        if_name = if_row.split('STRING:')[-1].strip()
        if_OID = if_row.split('ifDescr.')[-1].split("=")[0].strip()
        wrdb(if_name, device_id, if_OID)
