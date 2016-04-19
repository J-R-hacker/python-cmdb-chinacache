# -*- coding: utf-8 -*-
import rrdtool, time, os, sys

def getimestamp(ctime):
    #2015/10/21 00:00
    ctime = str(ctime).strip()
    print ctime
    timeArray = time.strptime(ctime, "%Y/%m/%d %H:%M")
    print timeArray
    timeStamp = int(time.mktime(timeArray))
    return timeStamp

def total_flow_graph(nodename, CSWname, timerange):
    pngfile = 'monitor/static/img/uplinkflow/' + nodename + '_total.png'
    rrdfile = 'monitor/uplinkflow/' + nodename + '/' + CSWname + '_total.rrd'
    titalname= nodename
    Alarm = '37580963840' #35G
    if timerange == 'None':
        GraphStart = str(int(time.time()) - 51480)
        GraphEnd = str(int(time.time()))
    else:
        GraphStart = str(getimestamp(timerange.split('-')[0]))
        GraphEnd = str(getimestamp(timerange.split('-')[1]))
    print GraphStart+":"+GraphEnd
    flow_graph_sh(pngfile, rrdfile, titalname, GraphStart, GraphEnd, Alarm)
    pngfile = 'img/uplinkflow/' + nodename + '_total.png'
    return pngfile

def flow_graph_sh(pngfile, rrdfile, titalname ,GraphStart, GraphEnd, Alarm):
    os.system("sh monitor/graph.sh '%s' '%s' '%s' '%s' '%s' '%s'" %(pngfile, rrdfile, titalname, GraphStart, GraphEnd, Alarm))

def flow_graph(filemane, path, soures):
    curtime = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
    #定义图表上方大标题
    if os.path.exists(soures):
        title= filemane + "(" + time.strftime('%Y-%m-%d', time.localtime(time.time())) + ")"
        #重点解释"--x-grid","MINUTE:12:HOUR:1:HOUR:1:0:%H"参数的作用（从左往右进行分解）“MINUTE:12”表示控制每隔12分钟放置一根次要格线
        #“HOUR:1”表示控制每隔1小时放置一根主要格线“HOUR:1”表示控制1个小时输出一个label标签“0:%H”0表示数字对齐格线，%H表示标签以小时显示
        rrdtool.graph( str(path), "--start", "-1d","--vertical-label=Bytes/s",
            "--x-grid","MINUTE:12:HOUR:1:HOUR:1:0:%H",
            "--width","850","--height","300","--title",str(title),
            "DEF:inoctets=%s:in:AVERAGE" %str(soures),#指定网卡入流量数据源DS及CF
            "DEF:outoctets=%s:out:AVERAGE" %str(soures), #指定网卡出流量数据源DS及CF
            "CDEF:total=inoctets,outoctets,+", #通过CDEF合并网卡出入流量，得出总流量total
            "CDEF:inbits=inoctets,8,*", #将入流量换算成bit，即*8，计算结果给inbits
            "CDEF:outbits=outoctets,8,*", #将出流量换算成bit，即*8，计算结果给outbits
            "AREA:inbits#00FF00:In traffic", #以面积方式绘制入流量
            "LINE1:outbits#0000FF:Out traffic", #以线条方式绘制出流量
            "HRULE:60000#FF0000:Alarm value\\r", #绘制水平线，作为告警线，阈值为6.1k
            "COMMENT:\\r",
            "GPRINT:inbits:AVERAGE:Avg In traffic\: %6.2lf %Sbps", #绘制入流量平均值
            "COMMENT: ",
            "GPRINT:inbits:MAX:Max In traffic\: %6.2lf %Sbps", #绘制入流量最大值
            "COMMENT: ",
            "GPRINT:inbits:MIN:Min In traffic\: %6.2lf %Sbps\\r", #绘制入流量最小值
            "COMMENT: ",
            "GPRINT:outbits:AVERAGE:Avg Out traffic\: %6.2lf %Sbps", #绘制出流量平均值
            "COMMENT: ",
            "GPRINT:outbits:MAX:Max Out traffic\: %6.2lf %Sbps", #绘制出流量最大值
            "COMMENT: ",
            "GPRINT:outbits:MIN:Min Out traffic\: %6.2lf %Sbps\\r") #绘制出流量最小值
    else:
        f = file('log/uplinkGraph.log','a+')
        f.write("%s %s isn't graphed!\n" %(curtime, filemane))
        f.close()
