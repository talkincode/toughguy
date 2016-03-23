#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, click
from toughcli import __version__
from toughcli.service import mysql as mysql_serv
from toughcli.service import docker as docker_serv
from toughcli.service import redis as redis_serv
from toughcli.service import radius as radius_serv
from toughcli.service import wlan as wlan_serv
from toughcli.settings import *

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(click.style("toughcli {0}".format(__version__),fg='cyan'))
    ctx.exit()

def print_info(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(click.style("toughcli {0}".format(__version__),fg='cyan'))
    ctx.exit()
    


@click.group()
@click.option('--version', is_flag=True, callback=print_version,expose_value=False, is_eager=True)
@click.option('--server-info', is_flag=True, callback=print_info,expose_value=False, is_eager=True)
def cli():
    pass

@click.command()
@click.option('--pypi', is_flag=True,help="from pypi")
@click.option('--github', is_flag=True,help="from github")
def upgrade(pypi,github):
    if github:
        os.system("sudo pip install --upgrade https://github.com/talkincode/toughcli/archive/master.zip")
    elif pypi:
        os.system("sudo pip install --upgrade toughcli")


@click.command()
@click.option('--install', is_flag=True,help="install docker & docker-compose")
@click.option('--from-daocloud', is_flag=True)
def docker(install,from_daocloud):
    if install and from_daocloud:
        docker_serv.daocloud_install()
    elif from_daocloud:
        docker_serv.auto_install()


@click.command()
@click.option('--install', is_flag=True,help="install mysql docker instance")
@click.option('-e','--edit-config', is_flag=True,help="edit mysql docker-compose.yml config")
@click.option('-o','--docker-operate', default='',type=click.Choice(MYSQL_OPS),help="docker instance operate")
@click.option('-d','--rundir', default=RUNDIR,help="default:%s"%RUNDIR)
@click.option('-i','--instance', default='mydb',help="mysql instance, default:mydb")
def mysql(install,edit_config,docker_operate,rundir,instance):
    if install:
        mysql_serv.docker_install(rundir,instance)
    elif docker_operate:
        mysql_serv.docker_op(rundir,instance,docker_operate)
    elif edit_config:
        click.edit(filename="{0}/{1}/docker-compose.yml".format(rundir,instance))


@click.command()
@click.option('--install', is_flag=True,help="install redis docker instance")
@click.option('-e','--edit-config', is_flag=True,help="edit redis docker-compose.yml config")
@click.option('-o','--docker-operate', default='', type=click.Choice(REDIS_OPS),help="docker instance operate")
@click.option('-d','--rundir', default=RUNDIR, help="default:%s"%RUNDIR)
@click.option('-i','--instance', default='myredis',help="redis instance, default:myredis")
def redis(install,edit_config,docker_operate,rundir,instance):
    if install:
        redis_serv.docker_install(rundir,instance)
    elif docker_operate:
        redis_serv.docker_op(rundir,instance,docker_operate)
    elif edit_config:
        click.edit(filename="{0}/{1}/docker-compose.yml".format(rundir,instance))



@click.command()
@click.option('--install', is_flag=True)
@click.option('-e','--edit-config', is_flag=True,help="edit radius docker-compose.yml config")
@click.option('-o','--docker-operate', default='', type=click.Choice(RADIUS_OPS),help="docker instance operate")
@click.option('-d','--rundir', default=RUNDIR, help="default:%s"%RUNDIR)
@click.option('-i','--instance', default='myradius')
@click.option('-n','--worker-num', default=2,type=click.INT)
@click.option('-r','--release', default='stable',type=click.Choice(['dev','stable','commcial']),)
def radius(install,edit_config, docker_operate,rundir,instance,worker_num,release):
    if install and release == 'commcial':
        licence = click.prompt('Please enter your commcial licence:', default='')
    elif install and release in ('dev','stable'):
        radius_serv.docker_install(rundir,instance,worker_num,release)
    elif docker_operate:
        radius_serv.docker_op(rundir,instance,docker_operate)
    elif edit_config:
        click.edit(filename="{0}/{1}/docker-compose.yml".format(rundir,instance))

@click.command()
@click.option('--install', is_flag=True)
@click.option('--scale', is_flag=True)
@click.option('-e','--edit-config', is_flag=True,help="edit toughwlan docker-compose.yml config")
@click.option('-o','--docker-operate', default='', type=click.Choice(WLAN_OPS),help="docker instance operate")
@click.option('-d','--rundir', default=RUNDIR, help="default:%s"%RUNDIR)
@click.option('-i','--instance', default='myradius')
@click.option('-n','--worker-num', default=2,type=click.INT)
def wlan(install,scale,edit_config, docker_operate,rundir,instance,worker_num):
    if install:
        wlan_serv.docker_install(rundir,instance,worker_num)
    elif docker_operate:
        wlan_serv.docker_op(rundir,instance,docker_operate)
    elif edit_config:
        click.edit(filename="{0}/{1}/docker-compose.yml".format(rundir,instance))
    elif scale:
        wlan_serv.docker_scale(rundir,instance,worker_num)


cli.add_command(upgrade)
cli.add_command(docker)
cli.add_command(mysql)
cli.add_command(redis)
cli.add_command(radius)
cli.add_command(wlan)

if __name__ == '__main__':
    cli()














