import os, time, commands

f = file('/root/python/django/cc/log/updated.log','a+')
curtime = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
(status, result) = commands.getstatusoutput('ps aux | grep update')
if not 'python update.py' in result:
    os.chdir('/root/python/django/cc/monitor/')
    os.system('python update.py &')
    f.write('%s update is reset!\n' %curtime)
else:
    f.write('%s update is running!\n' %curtime)
f.close()
