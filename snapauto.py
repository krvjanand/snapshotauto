import boto3
import botocore
import click

session = boto3.Session(profile_name='snapauto')
ec2 = session.resource('ec2')

def filter_instances(project):
    instances = []
    # print('Project:',project)
    if project:
        filters=[{'Name':'tag:Project','Values': [project]}]
        instances = ec2.instances.filter(Filters=filters)

    else:
        instances = ec2.instances.all()

    return instances

@click.group()
def cli():
    "Snapauto manages automatic snapshots"

@cli.group('snapshots')
def snapshots():
    "Commands for Snapshots"

@snapshots.command('list')
@click.option('--project',default=None,
        help="Only Snapshots for project (tag Project:<name>)")

    # @click.option('--state', default=None,
    #     help="Only Instances with state (tag state:<name>)")

@click.option('--all','list_all',default=False, is_flag=True,
        help="Lists all snapshots for each volume, not just most recent for project (tag Project:<name>)")


def list_snapshots(project, list_all):
    "List EC2 Volume snapshots"
    instances=filter_instances(project)

    cnt = 1
    for i in instances:
        tags = {t['Key']: t['Value'] for t in i.tags or []}
        for v in i.volumes.all():
            for s in v.snapshots.all():
                if cnt == 1:
                    print('| '.join((
                        "Snapshot id",
                        "Volume",
                        "Instance",
                        "Instance State",
                        "Volume State",
                        "Snapshot State",
                        "Progress",
                        "Start Time",
                        "Tag")))
                    print("|".join((
                        s.id,
                        v.id,
                        i.id,
                        i.state['Name'],
                        v.state,
                        s.state,
                        s.progress,
                        s.start_time.strftime("%c"),
                        tags.get('Project','<No Project>'))))

                    cnt = cnt + 1
                    if s.state == 'completed' and not list_all: break


                else:
                    cnt = cnt + 1
                    print("|".join((
                        s.id,
                        v.id,
                        i.id,
                        i.state['Name'],
                        v.state,
                        s.state,
                        s.progress,
                        s.start_time.strftime("%c"),
                        tags.get('Project','<No Project>'))))

                    if s.state == 'completed' and not list_all: break

    return s

@cli.group('volumes')
def volumes():
    "Commands for volumes"

@volumes.command('list')
@click.option('--project',default=None,
        help="Only Volumes for project (tag Project:<name>)")

    # @click.option('--state', default=None,
    #     help="Only Instances with state (tag state:<name>)")

def list_volumes(project):
    "List EC2 Volumes"
    instances=filter_instances(project)

    cnt = 1
    for i in instances:
        tags = {t['Key']: t['Value'] for t in i.tags or []}
        for v in i.volumes.all():
            if cnt == 1:
                print('| '.join((
                    "Volume",
                    "Instance",
                    "State",
                    "Size",
                    "Encrypted",
                    "Tag")))
                print("|".join((
                       v.id,
                       i.id,
                       v.state,
                       str(v.size) + "GiB",
                       v.encrypted and "Encrypted" or "Not Encrypted",
                       tags.get('Project','<No Project>'))))

                cnt = cnt + 1

            else:
                cnt = cnt + 1
                print("|".join((
                       v.id,
                       i.id,
                       v.state,
                       str(v.size) + "GiB",
                       v.encrypted and "Encrypted" or "Not Encrypted",
                       tags.get('Project','<No Project>'))))
    return v


@cli.group('instances')
def instances():
    "Commands for instances"

@instances.command('snapshot',
    help="Create Snapshots of all volumes")

@click.option('--project',default=None,
        help="Only Instances for project (tag Project:<name>)")

def create_snapshots(project):
    "Create snapshots for EC2 instances"

    instances=filter_instances(project)
    for i in instances:
        print("Stopping Instance: {0}...".format(i.id))

        i.stop()
        i.wait_until_stopped()

        for v in i.volumes.all():
            print("Creating snapshot of {0}".format(v.id))
            v.create_snapshot(Description="Created by Snapshot Auto Program")

        print("Starting Instance: {0}...".format(i.id))

        i.start()
        i.wait_until_running()
    print("Snapshots complete!!")
    return

@instances.command('list')
@click.option('--project',default=None,
        help="Only Instances for project (tag Project:<name>)")

    # @click.option('--state', default=None,
    #     help="Only Instances with state (tag state:<name>)")


    # def list_instances(project, state):
def list_instances(project):

    "List EC2 instances"
    instances=filter_instances(project)

    # if state:
    #     stfilters=[{'Name':'instance-state-name','Values': [state]}]
    #     instances = ec2.instances.filter(Filters=stfilters)
    #
    # else:
    #     instances = ec2.instances.all()

    cnt = 1
    for i in instances:
        tags = {t['Key']: t['Value'] for t in i.tags or []}
        if cnt == 1:
            print('| '.join((
                "Instance Id",
                "Instance Type",
                "AZ",
                "State",
                "Public DNS Name",
                "Public IP",
                "Public IP from NI",
                "Tag")))
            print('| '.join((
                i.id,
                i.instance_type,
                i.placement['AvailabilityZone'],
                i.state['Name'],
                i.public_dns_name,
                str(i.public_ip_address),
                tags.get('Project','<No Project>'))))

                 # ''.join(list(map(lambda x: x['Association']['PublicIp'], i.network_interfaces_attribute))))))
            cnt = cnt + 1

        else:
            cnt = cnt + 1
            print('| '.join((
                i.id,
                i.instance_type,
                i.placement['AvailabilityZone'],
                i.state['Name'],
                i.public_dns_name,
                str(i.public_ip_address),
                tags.get('Project','<No Project>'))))
                # ''.join(list(map(lambda x: x['Association']['PublicIp'], i.network_interfaces_attribute))))))
    return

@instances.command('stop')
@click.option('--project',default=None,
        help="Only Instances for project (tag Project:<name>)")

def stop_instances(project):

    "Stop EC2 instances"

    instances=filter_instances(project)

    for i in instances:
        print("Stopping {0}...".format(i.id))
        try:
            i.stop()
        except botocore.exceptions.ClientError as e:
            print("Could not stop {0}.".format(i.id) + str(e))
            continue
    return

@instances.command('start')
@click.option('--project',default=None,
        help="Only Instances for project (tag Project:<name>)")

def start_instances(project):

    "Start EC2 instances"

    instances=filter_instances(project)

    for i in instances:
        print("Starting {0}...".format(i.id))
        try:
            i.start()
        except botocore.exceptions.ClientError as e:
            print("Could not start {0}.".format(i.id) + str(e))
            continue
    return

if __name__ == '__main__':
    cli()
