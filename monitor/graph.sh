#!/bin/bash
pngfile=$1
rrdfile=$2                    
titlename=$3          
GraphStart=$4       
GraphEnd=$5       
Alarm=$6  
rrdtool graph ${pngfile} \
-w 770 -h 180 \
-n TITLE:9:${font}  \
-n UNIT:8:${font}  \
-n UNIT:8:${font}  \
-n UNIT:8:${font}  \
-c SHADEA#808080 \
-c SHADEB#808080 \
-c FRAME#006600 \
-c ARROW#FF0000 \
-c AXIS#000000 \
-c FONT#000000 \
-c CANVAS#eeffff \
-c BACK#ffffff \
--x-grid MINUTE:15:HOUR:1:HOUR:2:0:%H  \
--title ${titlename}  \
--lower-limit=0 \
--base=1024 \
--start now-1d  \
--end now    \
--start ${GraphStart}  \
--end ${GraphEnd}   \
DEF:IN=${rrdfile}:ifin:AVERAGE   \
DEF:OUT=${rrdfile}:ifout:AVERAGE  \
CDEF:INFLOW=IN,8,*  \
CDEF:OUTFLOW=OUT,8,*  \
CDEF:TOTAL_FLOW=INFLOW,OUTFLOW,+   \
COMMENT:" \n" \
LINE1:TOTAL_FLOW#00ff00:TO_FLOW  \
GPRINT:TOTAL_FLOW:AVERAGE:"AVERAGE\:%0.2lf %Sbps"  \
GPRINT:TOTAL_FLOW:MAX:"MAX\:%0.2lf %Sbps"  \
GPRINT:TOTAL_FLOW:MIN:"MIN\:%0.2lf %Sbps"  \
COMMENT:" \n" \
AREA:OUTFLOW#0011ff:OUTFLOW \
GPRINT:OUTFLOW:AVERAGE:"AVERAGE\:%0.2lf %Sbps"  \
GPRINT:OUTFLOW:MAX:"MAX\:%0.2lf %Sbps"  \
GPRINT:OUTFLOW:MIN:"MIN\:%0.2lf %Sbps"  \
COMMENT:" \n" \
LINE1:INFLOW#cc0000:IN_FLOW \
GPRINT:INFLOW:AVERAGE:"AVERAGE\:%0.2lf %Sbps"  \
GPRINT:INFLOW:MAX:"MAX\:%0.2lf %Sbps"  \
GPRINT:INFLOW:MIN:"MIN\:%0.2lf %Sbps"  \
COMMENT:" \n" \
HRULE:${Alarm}#ff0000:"Alarm" \
COMMENT:" \n" \
COMMENT:"\t\t\t\t\t\t\t\t\t\t\t\t\tlast updated \:$(date '+%Y-%m-%d %H\:%M')\n"