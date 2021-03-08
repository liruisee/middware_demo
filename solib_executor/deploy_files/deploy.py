import os
import subprocess


deploy_files_dir = os.path.abspath(__file__).rsplit('/', 1)[0]
project_path = deploy_files_dir.rsplit('/', 2)[0]
template_file_path = f'{deploy_files_dir}/conf.ini.template'
conf_file_path = f'{deploy_files_dir}/conf.ini'
workers = os.cpu_count()
render_dict = {
    'project_path': project_path,
    'workers': workers
}


with open(template_file_path, 'r') as f_r, open(conf_file_path, 'w') as f_w:
    content = f_r.read()
    write_content = content % render_dict
    f_w.write(write_content)


cmd = f'uwsgi --ini {conf_file_path}'
subprocess.check_call(cmd, shell=True)
