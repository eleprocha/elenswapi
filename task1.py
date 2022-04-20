import requests
import json
import click

@click.group()
def task1():
    pass

@task1.command()
@click.argument('char')
def search(**kwargs):
    response = requests.get("https://www.swapi.tech/api/people").json()
    name_uid_dict = {i['name']:i['uid'] for i in response['results']}
    if any({i:j for i,j in name_uid_dict.items() if kwargs['char'].upper() in i.upper()}):
        dict = {}
        dict['name'] = [i for i in name_uid_dict.keys() if kwargs['char'].upper() in i.upper()][0]
        dict['uid'] = int(name_uid_dict[dict['name']])
        result = requests.get('https://www.swapi.tech/api/people/{0}'.format(dict['uid'])).json()['result']['properties']
        height = result['height']
        mass = result['mass']
        birth_year = result['birth_year']
        print('Name: {0}\nHeight: {1}\nMass: {2}\nBirth Year: {3}'.format(dict['name'],height,mass,birth_year))
    else:
            print('The force is not strong within you')



if __name__ == '__main__':
    task1()
