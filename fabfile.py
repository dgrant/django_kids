from fabric.api import run, env, cd, shell_env, execute, sudo

from fabric.network import ssh
ssh.util.log_to_file("paramiko.log", 10)
env.hosts = ['linode']
env.use_ssh_config = True
ROOT='/home/david/public_html/django/django_kids/public'

def restart():
    with cd(ROOT):
        sudo('touch /etc/uwsgi/apps-available/django_kids.ini')

def update():
    with cd(ROOT):
        run('git pull --rebase')

def schema():
    with cd(ROOT), shell_env(DJANGO_SETTINGS_MODULE='django_kids.settings.production'):
        run('env/bin/python ./manage.py migrate')

def backupdb():
    with cd(ROOT):
        run('./backupLocalDB.sh kids_django')

def static():
    with cd(ROOT):
        run('rm -rf static/*')
        run('env/bin/python ./manage.py collectstatic --settings=django_kids.settings.production --noinput --link')

def deploy():
    execute(update)
    execute(env)
    execute(backupdb)
    execute(schema)
    execute(static)
    execute(restart)

def env():
    with cd(ROOT):
        run('./createVirtualEnv.sh')
