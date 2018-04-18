from fabric.api import env, run
from fabric.operations import sudo

GIT_REPO = "pms"

env.user = 'ubuntu'
env.hosts = ['118.25.44.135']
env.port = '22'

def deploy():
    source_folder = '/home/ubuntu/pms/pms'
    run('cd {} && git checkout -f && git pull origin master '.format(source_folder))
    run(
        '''
        cd {} &&
        ~/venv/venv_pms/bin/pip install -r ../requirements.txt &&
        ~/venv/venv_pms/bin/python manage.py migrate
        '''.format(source_folder))
    sudo('restart pms')
    sudo('service nginx reload')