# -- coding:utf-8 --
import MySQLdb
#获取核心设备的上联端口信息
def CSW_uplink_info():
    conn=MySQLdb.connect(host='localhost',user='root',passwd='111111',db='device',port=3306,charset="utf8")
    cur=conn.cursor()
    conn.select_db('device')
    cur.execute(''' select node_name, device_name, device_ip, device_uplinkoid
                    from device_node, device_device
                    where device_node.id = device_device.node_id
                    AND device_role="CSW"''')
    rows = cur.fetchall()
    #print 'node_name,device_name,device_ip,device_uplinkoid'
    conn.close()
    return rows
