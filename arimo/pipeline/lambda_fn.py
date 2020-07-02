from urllib.parse import urlparse

import boto3
import click

from arimo.pipeline.main import cli
from arimo.pipeline.utils import load_yaml

client = boto3.client('lambda')
s3_resource = boto3.resource('s3')


@cli.group(name="lambda")
def lambda_fn():
    pass


@lambda_fn.command()
@click.option('--file', prompt='File')
def create(file):
    o = load_yaml(file)
    name = o['FunctionName']
    role = o['Role']

    zip_file = o['Code']['ZipFile']
    assert 's3://' in zip_file
    prs = urlparse(zip_file)
    s3_bucket, s3_key = prs.netloc, prs.path[1:]

    response = client.create_function(
        FunctionName=name,
        Runtime=o.get('Runtime', 'python3.8'),
        Role=role,
        Handler=o['Handler'],
        Code={
            "S3Bucket": s3_bucket,
            "S3Key": s3_key
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
    role = o['Role']

    code = o.get('Code')
    if code:
        zip_file = code['ZipFile']
        assert 's3://' in zip_file
        prs = urlparse(zip_file)
        s3_bucket, s3_key = prs.netloc, prs.path[1:]

        response = client.update_function_code(
            FunctionName=name,
            S3Bucket=s3_bucket,
            S3Key=s3_key
        )
        print(response)

    handler = o.get('Handler')
    if handler:
        response = client.update_function_configuration(
            FunctionName=name,
            Role=role,
            Handler=o['Handler']
        )
        print(response)

    tags = o.get('Tags')
    if tags:
        region = o['AWS_REGION']
        response = client.tag_resource(
            Resource="arn:aws:lambda:%s:905988898753:function:%s" % (region, name),
            Tags=tags
        )
        print(response)


@lambda_fn.command()
@click.option('--name', prompt='Name')
def delete(name):
    response = client.delete_function(
        FunctionName=name,
    )
    print(response)
