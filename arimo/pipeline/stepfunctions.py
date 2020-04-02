import boto3
import click
import json

from arimo.pipeline.main import cli
from arimo.pipeline.utils import load_yaml

client = boto3.client('stepfunctions')


@cli.group()
def sfn():
    pass


@sfn.command()
@click.option('--file', prompt='File')
def create(file):
    o = load_yaml(file)
    response = client.create_state_machine(
        name=o.get('name'),
        definition=json.dumps(o['definition']),
        roleArn='arn:aws:iam::394497726199:role/pipeline-sdk',
    )
    print(response)


@sfn.command()
@click.option('--file', prompt='File')
def update(file):
    o = load_yaml(file)
    state_machine_arn = "arn:aws:states:ap-northeast-1:394497726199:stateMachine:" + o['name']
    response = client.update_state_machine(
        stateMachineArn=state_machine_arn,
        definition=json.dumps(o['definition']),
    )
    print(response)
