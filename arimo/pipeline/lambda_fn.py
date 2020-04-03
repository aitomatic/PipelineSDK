from io import BytesIO

import boto3
import click
import glob
import json
import zipfile

from arimo.pipeline.main import cli
from arimo.pipeline.utils import load_yaml

client = boto3.client('lambda')
s3_resource = boto3.resource('s3')

ARN_ROLE = "arn:aws:iam::394497726199:role/pipeline-sdk-lambda-role"


def generate_zip(files):
    mem_zip = BytesIO()

    with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file in files:
            with open(file, 'rb') as f:
                data = BytesIO(f.read())
            zf.writestr(file, data.getvalue())

    return mem_zip.getvalue()


@cli.group(name="lambda")
def lambda_fn():
    pass


@lambda_fn.command()
@click.option('--file', prompt='File')
def create(file):
    o = load_yaml(file)
    name = o['FunctionName']
    code_dir = o.get('Code')['FunctionCodeFiles']
    response = client.create_function(
        FunctionName=name,
        Runtime=o.get('Runtime', 'python3.8'),
        Role=ARN_ROLE,
        Handler=o['Handler'],
        Code={
            "ZipFile": generate_zip(glob.glob(code_dir))
        },
        Description=o.get('Description', ''),
        Timeout=o.get('Timeout', 3),
        MemorySize=o.get('MemorySize', 128),
        Environment={
            'Variables': o.get('EnvironmentVariables', {})
        },
        Tags=o.get('Tags', {}),
    )
    print(response)


@lambda_fn.command()
@click.option('--file', prompt='File')
def update(file):
    o = load_yaml(file)
    name = o['FunctionName']

    code = o.get('Code')
    if code:
        code_dir = code['FunctionCodeFiles']
        response = client.update_function_code(
            FunctionName=name,
            ZipFile=generate_zip(glob.glob(code_dir))
        )
        print(response)

    handler = o.get('Handler')
    if handler:
        response = client.update_function_configuration(
            FunctionName=name,
            Handler=o['Handler']
        )
        print(response)


@lambda_fn.command()
@click.option('--name', prompt='Name')
def delete(name):
    response = client.delete_function(
        FunctionName=name,
    )
    print(response)
