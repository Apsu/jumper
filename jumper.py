#!/usr/bin/env python

import click
import requests
import yaml
import json

@click.group()
def jumper():
    pass

@jumper.command()
@click.option(
    '--creds_file',
    default='creds.yml',
    type=click.Path(
        exists=True,
        file_okay=True,
        readable=True,
        resolve_path=True
    ),
    help='Path to credentials file'
)
def login(creds_file):
    with open(creds_file) as fd:
        creds = yaml.load(fd)

    params = {
        'username': creds['username'],
        'password': creds['password'],
        'api-key': creds['api-key']
    }

    r = requests.post('http://localhost:5000/login', params=params)
    if r.status_code == 200 and r.json()['Response'] == 'Success':
        print 'Success'
    else:
        print 'Login failure:'
        print r.text

@jumper.command()
@click.option('--verbose/--brief', default=False, help='Show full JSON output or summary')
def user(verbose):
    r = requests.get('http://localhost:5000/user')

    if not verbose:
        print r.json()['Response']['user']['displayName']
    else:
        print r.text


@jumper.command()
@click.option('--verbose/--brief', default=False, help='Show full JSON output or summary')
def characters(verbose):
    def _get_class(classType):
        if classType == 0:
            return 'Titan'
        elif classType == 1:
            return 'Hunter'
        elif classType == 2:
            return 'Warlock'

    def _get_gender(genderType):
        if genderType == 0:
            return 'Male'
        elif genderType == 1:
            return 'Female'

    r = requests.get('http://localhost:5000/user/characters')
    if not verbose:
        for character in r.json()['Response']['data']['characters']:
            print 'Class: %s, Gender: %s, Level: %d' % (
                _get_class(character['characterBase']['classType']),
                _get_gender(character['characterBase']['genderType']),
                character['characterLevel']
            )
    else:
        print r.text

@jumper.command()
def manifest():
    r = requests.get('http://localhost:5000/manifest')
    print r.text

if __name__ == '__main__':
    jumper()
