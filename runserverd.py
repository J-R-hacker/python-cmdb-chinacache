import os, time, commands

f = file('/root/python/django/cc/log/runserverd.log','a+')
curtime = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
(status, result) = commands.getstatusoutput('ps aux | grep 0.0.0.0:8000')
if not 'python manage.py runserver 0.0.0.0:8000' in result:
    os.chdir('/root/python/django/cc/')
    #os.system('python manage.py runserver 0.0.0.0:8000 &')
    f.write('%s runserver is reset!\n' %curtime)
else:
    f.write('%s running is running!\n' %curtime)
f.close()
