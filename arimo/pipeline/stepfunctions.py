import boto3
import click
import json

from arimo.pipeline.main import cli
from arimo.pipeline.utils import load_yaml

client = boto3.client('stepfunctions')
sts = boto3.client('sts')

STATE_MACHINE_ARN_PREFIX = "arn:aws:states:ap-northeast-1:905988898753:stateMachine:"

aws_account = sts.get_caller_identity().get('Account')
aws_role_arn = "arn:aws:iam::%s:role/pipeline-states-role" % aws_account


def write_json(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(json.loads(data), outfile, indent=2)
    print("JSON file:", filename)


@cli.group()
def sfn():
    pass


@sfn.command()
@click.option('--file', prompt='File')
@click.option('--out-json/--no-out-json', default=False)
def create(file, out_json):
    o = load_yaml(file)
    role_arn = aws_role_arn
    definition = json.dumps(o['definition'], indent=2)
    tags = [{'key': k, 'value': o['tags'][k]} for k in o['tags']]
    response = client.create_state_machine(
        name=o.get('name'),
        definition=definition,
        tags=tags,
        roleArn=role_arn,
    )
    print(response)
    if out_json:
        write_json(file.replace('.yaml', '.json'), definition)


@sfn.command()
@click.option('--file', prompt='File')
@click.option('--out-json/--no-out-json', default=False)
def update(file, out_json):
    o = load_yaml(file)
    role_arn = aws_role_arn
    state_machine_arn = STATE_MACHINE_ARN_PREFIX + o['name']
    definition = json.dumps(o['definition'], indent=2)
    response = client.update_state_machine(
        stateMachineArn=state_machine_arn,
        definition=definition,
        roleArn=role_arn,
    )
    print(response)
    if out_json:
        write_json(file.replace('.yaml', '.json'), definition)


@sfn.command()
@click.option('--name', prompt='Name')
def delete(name):
    state_machine_arn = STATE_MACHINE_ARN_PREFIX + name
    response = client.delete_state_machine(
        stateMachineArn=state_machine_arn
    )
    print(response)


@sfn.command()
@click.option('--name', prompt='Name')
@click.option('--input-file')
def start(name, input_file):
    state_machine_arn = STATE_MACHINE_ARN_PREFIX + name
    input_json = {}
    if input_file:
        with open(input_file) as f:
            input_json = json.load(f)
    input_str = json.dumps(input_json, indent=2)

    response = client.start_execution(
        stateMachineArn=state_machine_arn,
        input=input_str
    )
    print(response)
