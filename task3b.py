import requests
import json
import click
from datetime import datetime
from requests_cache import CachedSession



@click.group()
def task3():
    pass

session = CachedSession('example_cache', backend='sqlite')

@task3.command()
@click.option("--world", is_flag=True, show_default=True, default=False)
@click.option("--clean", is_flag=True, show_default=True, default=False)
@click.argument('char')
def search(clean,world,**kwargs):
    response = session.get("https://www.swapi.tech/api/people").json()
    name_uid_dict = {i['name']:i['uid'] for i in response['results']}
    if any({i:j for i,j in name_uid_dict.items() if kwargs['char'].upper() in i.upper()}):
        dict = {}
        dict['name'] = [i for i in name_uid_dict.keys() if kwargs['char'].upper() in i.upper()][0]
        dict['uid'] = int(name_uid_dict[dict['name']])
        result = session.get('https://www.swapi.tech/api/people/{0}'.format(dict['uid'])).json()['result']['properties']
        response_c = session.get('https://www.swapi.tech/api/people/{0}'.format(dict['uid']))
        height = result['height']
        mass = result['mass']
        birth_year = result['birth_year']
        print('Name: {0}\nHeight: {1}\nMass: {2}\nBirth Year: {3}'.format(dict['name'],height,mass,birth_year))
        
        if world:
            result_planet = requests.get('https://www.swapi.tech/api/planets/{0}'.format(dict['uid'])).json()['result']['properties']
            thename = result_planet['name']
            population = result_planet['population']
            planet_year = int(result_planet['orbital_period'])
            planet_day = int(result_planet['rotation_period'])
            print('Name: {0}\nHeight: {1}\nMass: {2}\nBirth Year: {3}\n'.format(dict['name'],height,mass,birth_year))
            print('Homeworld\n'+ len('Homeworld')*'-',f'\nName:{thename}',f'\nPopulation:{population}')
            print('\nOn {0}, 1 year on earth is {1} years and 1 day {2} days'.format(thename,round(planet_year/365,2),round(planet_day/24,2)))
        print("\n\ncache:"+ datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f"))

        if clean:
            session.cache.clear()
            print("removed cache")

    else: 
            print('The force is not strong within you')

@task3.command()
@click.option("--clean", is_flag=True, show_default=True, default=False)
def cache(clean):
        session.cache.clear()
        print("removed cache")





if __name__ == '__main__':
    task3()

