# -*- coding: utf-8 -*-
import os, commands

#10G端口可用的端口流量OID前缀，中间会调用get_snmp方法得到值
def port_flow(ip, ifoid):
    InOctetoid =  'ifHCInOctets.'  #ifHCInOctets
    OutOctetoid = 'ifHCOutOctets.' #ifHCOutOctets 
    in_oid = InOctetoid + ifoid
    out_oid = OutOctetoid + ifoid
    try:
        IfInOctet = int(get_snmp(ip, in_oid))
        IfOutOctet = int(get_snmp(ip, out_oid))
    except ValueError, e:
        f = file('../log/portflow.log','a+')
        f.write('IP:%s IF:%s is error(%s)\n' %(ip, ifoid, e))
        return (0, 0)
    return (IfInOctet, IfOutOctet)

#只需要给ip和OID就可以返回snmp后面的那个值
def get_snmp(ip, oid, comm='ChinaCache'):
    (status, result) = commands.getstatusoutput('snmpwalk -v2c -c %s %s %s' %(comm, ip, oid))
    result = result.split(':')[-1].strip()
    return result

