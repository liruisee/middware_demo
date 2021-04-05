import os
import subprocess
import traceback
import time


project_path = str(os.path.abspath(__file__).rsplit('/', 2)[0])
project_name = project_path.rsplit('/', 1)[1]
host1 = 'admin@www.shhy.tech'
path1 = '/home/admin'
host2 = 'nuoer@192.168.3.101'
path2 = '/home/nuoer'

cmd = f'rsync -e "ssh -p 10022" -avpgo --progress {project_path} {host1}:{path1}'

while 1:
    try:
        subprocess.check_call(cmd, shell=True)
        break
    except Exception:
        print(traceback.format_exc())
        time.sleep(3)


cmd = f'ssh -p 10022 {host1} "rsync -avpgo --progress {path1}/{project_name} {host2}:{path2}"'

while 1:
    try:
        subprocess.check_call(cmd, shell=True)
        break
    except Exception:
        print(traceback.format_exc())
        time.sleep(3)

