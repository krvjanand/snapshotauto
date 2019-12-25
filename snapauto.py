import boto3
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
def instances():
            "Commands for instances"

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
        i.stop()


    return

@instances.command('start')
@click.option('--project',default=None,
        help="Only Instances for project (tag Project:<name>)")

def start_instances(project):

    "Start EC2 instances"

    instances=filter_instances(project)

    for i in instances:
        print("Starting {0}...".format(i.id))
        i.start()


    return

if __name__ == '__main__':
    instances()
