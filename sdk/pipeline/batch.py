import boto3
import click

from sdk.pipeline.main import cli
from sdk.pipeline.utils import load_yaml

client = boto3.client('batch')


@cli.group()
def batch():
    pass


@batch.command()
@click.option('--file', prompt='File')
def submit(file):
    o = load_yaml(file)
    response = client.submit_job(
        jobName=o['jobName'],
        jobQueue=o['jobQueue'],
        arrayProperties=o.get('arrayProperties', {}),
        jobDefinition=o['jobDefinition'],
        containerOverrides=o.get('containerOverrides', {}),
        timeout=o.get('timeout', {})
    )
    print(response)
