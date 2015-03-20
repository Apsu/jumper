#!/usr/bin/env python

import click
import requests
import yaml
import json

@click.group()
def jumper():
    pass

@jumper.command()
@click.option('--cred_file', default='creds.yml')
def login(cred_file):
    if not cred_file:
        return False

    with open(cred_file) as fd:
        creds = yaml.load(fd)

    params = {
        'username': creds['username'],
        'password': creds['password'],
        'api-key': creds['api-key']
    }

    r = requests.post('http://localhost:5000/login', params=params)
    if r.status_code == 200 and r.json()['Response'] == 'Success':
        logged_in = True
        return True
    else:
        print r.text
        return False

@jumper.command()
def user():
    r = requests.get('http://localhost:5000/user')
    print r.text

@jumper.command()
def find():
    r = requests.get('http://localhost:5000/find')
    print r.text

@jumper.command()
def characters():
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
    for character in r.json()['Response']['data']['characters']:
        print 'Class: %s, Gender: %s, Level: %d' % (
            _get_class(character['characterBase']['classType']),
            _get_gender(character['characterBase']['genderType']),
            character['characterLevel']
        )

    #print r.text

@jumper.command()
def manifest():
    r = requests.get('http://localhost:5000/manifest')
    print r.text

if __name__ == '__main__':
    jumper()
