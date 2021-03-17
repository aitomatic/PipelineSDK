import boto3
import click

from sdk.pipeline.main import cli
from sdk.pipeline.utils import load_yaml

client = boto3.client('emr')


@cli.group()
def emr():
    pass


@emr.command()
@click.option('--file', prompt='File')
def create(file):
    o = load_yaml(file)
    instances = o['Instances']
    log_uri = o['LogUri']
    response = client.run_job_flow(
        Name=o['Name'],
        LogUri=log_uri,
        ReleaseLabel=o['ReleaseLabel'],
        Instances={
            'InstanceGroups': instances['InstanceGroups'],
            'KeepJobFlowAliveWhenNoSteps': False,
            'TerminationProtected': True
        },
        Steps=o.get('Steps', []),
        BootstrapActions=o.get('BootstrapActions', []),
        Applications=o.get('Applications', []),
        Configurations=o.get('Configurations', []),
        VisibleToAllUsers=True,
        ServiceRole='EMR_DefaultRole',
        Tags=o.get('Tags', []),
        StepConcurrencyLevel=1
    )
    print(response)


@emr.command()
@click.option('--name', prompt='Name')
def terminate(name):
    pass
