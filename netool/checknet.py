#!/usr/bin/env python
#-*-   encoding: utf-8 -*-
import pxssh,telnetlib,time,types,socket,pexpect,IPy,commands,re

def route_uplink_id(RouteIfIndex):
        route_uplink_id_list = []
        for i in range (0,len(RouteIfIndex.split('\n'))):
                route_uplink_id_list.append(int(RouteIfIndex.split('\n')[i].split(':')[-1]))
        return route_uplink_id_list

def ifindex(route_uplink_id_list,ifDescr):
        ifname_dict = {}
        for i in range (0,len(route_uplink_id_list)):
                for j in range (0,len(ifDescr.split('\n'))):
                        ifDescr_id = int(ifDescr.split('\n')[j].split(':')[-2].split('.')[-1].split('=')[0])
                        if ifDescr_id == route_uplink_id_list[i]:
                                ifname_dict[ifDescr.split('\n')[j].split(':')[-1]] = ifDescr.split('\n')[j].split('=')[0].split('.')[-1]
        return ifname_dict


def vlan2if(vlanid,VlanIfIndex,VIfIndex):
        for i in range (0,len(VlanIfIndex.split('\n'))):
                if int(vlanid) == int(VlanIfIndex.split('\n')[i].split(':')[-1]):
                        VlanIf_Index = int(VlanIfIndex.split('\n')[i].split('=')[0].split('.')[-1])
                        for j in range (0,len(VIfIndex.split('\n'))):
                                if int(VIfIndex.split('\n')[j].split('=')[0].split('.')[-1]) == VlanIf_Index:
                                        vlan2if_id = int(VIfIndex.split('\n')[j].split(':')[-1])
                                        return vlan2if_id

def uplink(ip):
    (status, RouteIfIndex) = commands.getstatusoutput('snmpwalk -v2c -c ChinaCache %s ipCidrRouteIfIndex.0.0.0.0.0.0.0.0.0' %ip)
    (status, ifDescr) = commands.getstatusoutput('snmpwalk -v2c -c ChinaCache %s ifDescr' %ip)
    (status, VlanIfIndex) = commands.getstatusoutput('snmpwalk -v2c -c ChinaCache %s 1.3.6.1.4.1.2011.5.25.42.1.1.1.3.1.4' %ip)
    (status, VIfIndex) = commands.getstatusoutput('snmpwalk -v2c -c ChinaCache %s 1.3.6.1.4.1.2011.5.25.42.1.1.1.3.1.2' %ip)
    route_uplink_id_list = route_uplink_id(RouteIfIndex)
    #得到vlan信息
    ifname_dict = ifindex(route_uplink_id_list,ifDescr)
    vlan_list, iflist = [], []
    for key,value in ifname_dict.items():
        if 'Vlanif' in key:
                id = vlan2if(key.split('f')[-1],VlanIfIndex,VIfIndex)
                vlan_list.append(id)
                #print id
                #if id != -1:
                del ifname_dict[key]
                vlan_fname_dict = ifindex(vlan_list,ifDescr)
                ifname_dict.update(vlan_fname_dict)
    for key in ifname_dict.keys():
        iflist.append(key)
    return iflist



class connecty:
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password
    def telnet_connect(self):
        try:
            telnet = telnetlib.Telnet(self.ip, '23', timeout=10)
            telnet.read_until(':')
            time.sleep(1)
            telnet.write(self.username + '\n')
            time.sleep(1)
            telnet.read_until(':')
            telnet.write(self.password + '\n')
            #
            for i in range (0,10):
                time.sleep(1)
                content=telnet.read_very_eager()
                result = self.telnet_login_check(content)
                if 'login success' in result:
                    return telnet
                elif 'password error' in result:
                    return result
                else:continue
        except (socket.timeout,socket.error) as e:
            return e

    def telnet_command(self,telnet,command_line):
        for command in command_line:
                #can print input command
                telnet.write(command + '\n')
                time.sleep(1)
                self.command_timer(command)
        return telnet.read_very_eager()

    #判断是否登录成功,请在此设置
    def telnet_login_check(self,cont):
        #出现什么样的欢迎关键字
        login_sign_list = (
            'current login',
            'Welcome to Ubuntu',
            'The password needs to be changed. Change now?',
        )
        for login_sign in login_sign_list:
            if login_sign in cont:
                return 'login success'

        #再次出现认证，判断为密码不对
        password_error_sign_list = (
            'name',
            'login',
            'assword',
        )
        for password_error_sign in password_error_sign_list:
            if password_error_sign in cont:
                return 'password error'
        return 'again'


    #有些需要等待的命令可以写这里
    def command_timer(self,command):
        needtime_command_list = (
            'dis cur',
            'dis log',
            'dis int des',
            "dis vlan 1",
        )
        for needtime_command in needtime_command_list:
            if command in needtime_command:
                time.sleep(4)

    #类总方法
    def connect(self,cline):
        tn = self.telnet_connect()
        if type(tn) == types.InstanceType:
            something = self.telnet_command(tn,cline)
            tn.close()
            return something
        else:return tn

class common:
    def __init__(self, hostname, ip):
        self.hostname = hostname
        self.ip = ip
    def snmpt(self):
        (status, result) = commands.getstatusoutput('snmpwalk -v2c -c %s %s %s' %("ChinaCache", self.ip, "sysDescr.0"))
        if "Timeout" in result:
            snmpcheck = "不通"
        else:
            snmpcheck = "正常"
        if "Huawei" in result:
            snmpcheck = snmpcheck + ":Huawei"
        return snmpcheck
    def pingt(self):
        pingtpatt = re.compile(r'(?P<tran>\d+) packets transmitted, (?P<receive>\d+) received, (?P<loss>\w+\%) packet loss, time (?P<time>\w+)')
        timepatt = re.compile(r'rtt min/avg/max/mdev = \d+.\d+/\d+.\d+/(\d+.\d+)/\d+.\d+')
        (status, result) = commands.getstatusoutput('ping -c 10 -w 5 %s' %self.ip)
        pckt = re.findall(pingtpatt,result)[0]
        if pckt[0] == pckt[1]:
            maxtime = re.findall(timepatt,result)[0]
            pingcheck = "未丢包,最大时延%sms" %maxtime
        else:
            pingcheck = "丢包,请检查连通性"
        return pingcheck

class huawei(connecty):
    def __init__(self, ip, username, password):
        connecty.__init__(self, ip, username, password)
    def connect(self):
        cline = ("n",
                 "screen-length 0 temporary",
                 "dis cur",
                 "dis stp br",
                 "dis lldp nei b",
                 "dis clock",
                 "dis int des",
                 "dis vlan 1"
            )
        tn = self.telnet_connect()
        if type(tn) == types.InstanceType:
            something = self.telnet_command(tn,cline)
            tn.close()
            return something
        else:return tn
    def sysname(self, config):
        sysnamepatt = re.compile(r'sysname ([^#|!]*)')
        name = re.findall(sysnamepatt,config)[0]
        return name
    def globalldp(self, config):
        if re.search(r"lldp enable", config):
            return "全局已开"
        else:
            return "未检测到"
    def stpcheck(self, config):
        if re.search(r'Protocol Status\s+:Disabled', config):
            return u"已关闭"
        else:
            return u"状态未知"
    def defaultroute(self):
        (status, defroute) = commands.getstatusoutput('snmpwalk -v2c -c ChinaCache %s ipCidrRouteIfIndex.0.0.0.0.0.0.0.0.0' %self.ip)
        return len(defroute.split("\n"))
    def lldplink(self, config):
        CElldppatt = re.compile(r'(?P<localif>10\w+\d+/\d+/\d+|\w+/\w+/\w+/\w+)\s+\d+\s+(?P<peerif>\w+\d+/\d+/\d+)\s+(?P<peer>\w+\-\w+\-\w+\-\w+)')
        Slldppatt = re.compile(r'(?P<localif>\w+\d+/\d+/\d+)\s+(?P<peer>\w+-\w+-\w+-\w+)(-\w+)?\s+(\w+[-|/]\w+[-|/]\w+)\s+\d+')
        (status, result) = commands.getstatusoutput('snmpwalk -v2c -c %s %s %s' %("ChinaCache", self.ip, "sysDescr.0"))
        lldplink = []
        if "CE5810" in result or "CE12800" in result:
            lldplink = re.findall(CElldppatt,config)
            for i in range (0, len(lldplink)):
                lldplink[i] = list(lldplink[i])
                lldplink[i][1], lldplink[i][2] = lldplink[i][2], lldplink[i][1]
        elif "S6700" in result:
            lldplink = re.findall(Slldppatt,config)
            for i in range (0, len(lldplink)):
                lldplink[i] = list(lldplink[i])
                lldplink[i][2], lldplink[i][3] = lldplink[i][3], lldplink[i][2]
        return lldplink
    def ifADdown(self, config):
        ifADdownpatt = re.compile(r'(?P<if>\w+\d+/\d+/\d+)\s+down\s+down\s+')
        ifADdown = re.findall(ifADdownpatt,config)
        return ifADdown
    def timecheck(self, config):
        timepatt = re.compile(r'(\d{4}-\d{1,2}-\d{2}\s+(\d{2}:?){3})')
        #timezonepatt = re.compile(r'Time\s+Zone\(\w+\)\s+\:\s+(\w+.\d+\:\d+)')
        if re.search(timepatt,config):
            time = re.search(timepatt,config).group()
        else:
            time = "None"
        return time
    def descif(self, config):
        descpatt = re.compile(r'(\w+/\w+/\w+|Eth-Trunk\d+|\w+/\w+/\w+/\w+)\s+up\s+up +([A-Z|a-z])?')
        desc = re.findall(descpatt, config)
        nodesc = []
        for row in desc:
            if row[1] == '':
                nodesc.append(row[0])
        return nodesc
    def vlanonec(self, config):
        vonepatt = re.compile(r'(10GE\d+/\d+/\d+|XGE\d+/\d+/\d+|10GE\d+/\d+/\d+/\d+)\(U\)')
        vone = re.findall(vonepatt, config)
        return vone
    def checktotal(self):
        checkresult = {}
        #设备配置抓取
        config = self.connect()
        if "password error" in config:
            checkresult["passwordcheck"] =  "密码错误"
            return checkresult
        elif "timed out" in config:
            checkresult["passwordcheck"] =  "登录超时"
            return checkresult
        elif not "screen-length 0 temporary" in config:
            checkresult["passwordcheck"] = "登录异常"
            return checkresult
        else:
            checkresult["passwordcheck"] =  "密码正确"
        #checkresult["config"] = config
        #抓取设备名称
        checkresult["sysname"] = self.sysname(config)
        #显示设备时间
        checkresult["timecheck"] = self.timecheck(config)
        #生成树状态检查
        checkresult["stpcheck"] = self.stpcheck(config)
        #未手动关闭端口
        checkresult["ifADdown"] = self.ifADdown(config)
        #未加描述检查，只检查双UP端口
        checkresult["descif"] = self.descif(config)
        #未在网络互连接口上删除vlan1的
        checkresult["vlanonec"] =  self.vlanonec(config)
        #检查lldp信息
        checkresult["lldpstatu"] = self.globalldp(config)
        #lldplink链接数，只查看10G端口
        lldp = self.lldplink(config)
        #lldp链接状态
        if len(lldp) != 0:
            lldp.sort(key=lambda x:x[1])
            li = []
            for link in lldp:
                lin = " %-12s: %-15s%s" %(link[0], link[1],  link[2])
                li.append(lin)
            checkresult["lldplink"] = li
            checkresult["lldpnum"] = len(lldp)
        #默认路由出口数量
        checkresult["deroutenum"] = self.defaultroute()
        #默认路由接口名称，只支持access接口
        checkresult["deroute"] = uplink(self.ip)
        return checkresult



def checknet(username, password, hostname, ip):
    username = str(username)
    password = str(password)
    hostname = str(hostname)
    ip = str(ip)
    if IPy.IP(ip).iptype() == 'PRIVATE':
        checkresult = { "IP": "%s 为私网地址" %ip }
        return checkresult
    com = common(username, ip)
    snmpcheck = com.snmpt()
    pingcheck = com.pingt()
    checkresult = { "hostname": hostname, "ip": ip}
    if not "ms" in pingcheck:
        checkresult["pingcheck"] = "连通性有问题，%s" %pingcheck
        return checkresult
    else:
        if not "Huawei" in snmpcheck:
                checkresult["snmpcheck"] = "状态异常"
                return checkresult
    if "Huawei" in snmpcheck:
        hw = huawei(ip=ip, username=username, password=password)
        checkresult = hw.checktotal()
        checkresult["snmpcheck"] = snmpcheck
        checkresult["pingcheck"] = pingcheck
        checkresult["hostname"] = hostname
        checkresult["ip"] = ip
        return checkresult

