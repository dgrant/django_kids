from fabric.api import run, env, cd, shell_env, execute

env.hosts = ['slice:55555']
ROOT='/home/david/public_html/django/django_kids/public'

def restart():
    with cd(ROOT):
        run('touch ../../django_kids.ini')

def update():
    with cd(ROOT):
        run('git pull')

def schema():
    with cd(ROOT), shell_env(DJANGO_SETTINGS_MODULE='django_kids.settings.production'):
        run('env/bin/python ./manage.py migrate links')

def backupdb():
    with cd(ROOT):
        run('./backupLocalDB.sh django_kids')

def static():
    with cd(ROOT):
        run('env/bin/python ./manage.py collectstatic --settings=django_kids.settings.production --noinput --link --clear')

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
