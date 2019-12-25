# snapshotauto
Python framework to list, start, stop EC2 instances, volumes and take snapshots of EBS volumes

## About

This project uses boto3 package to manage EC2 instances running in Linux Academy's Cloud sandbox environment and list the instances

## Configure

snapauto uses config file created by AWS CLI e.g.

'aws configure --profile snapauto'

## running
py snapauto.py <command> --project=Anand

commands = list, start, stop instances
