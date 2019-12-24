import boto3
import click

session = boto3.Session(profile_name='snapauto')
ec2 = session.resource('ec2')

@click.command("list")
def list_instances():
    "List EC2 instances"
    cnt = 1
    for i in ec2.instances.all():
        if cnt == 1:
            print('| '.join((
                "Instance Id",
                "Instance Type",
                "AZ",
                "State",
                "Public DNS Name",
                "Public IP",
                "Public IP from NI")))
            print('| '.join((
                i.id,
                i.instance_type,
                i.placement['AvailabilityZone'],
                i.state['Name'],
                i.public_dns_name,
                i.public_ip_address,
                ''.join(list(map(lambda x : x['Association']['PublicIp'], i.network_interfaces_attribute))))))
            cnt = cnt + 1
        else:
            cnt = cnt + 1
            print('| '.join((
                i.id,
                i.instance_type,
                i.placement['AvailabilityZone'],
                i.state['Name'],
                i.public_dns_name,
                i.public_ip_address,
                ''.join(list(map(lambda x : x['Association']['PublicIp'], i.network_interfaces_attribute))))))
    return

if __name__ == '__main__':
    list_instances()
