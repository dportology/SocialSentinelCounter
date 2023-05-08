import configparser
import os
import argparse
import time
from random import randint
from yaspin import yaspin
import csv

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.agents import load_tools
from langchain.agents import initialize_agent

from prompts import *
from util_objects.IndividualDetails import *
from utils import *

api_config = configparser.ConfigParser()
api_config.read_file(open('apidata.config'))

os.environ['OPENAI_API_KEY'] = api_config['OPENAI']['KEY']
os.environ['SERPAPI_API_KEY'] = api_config['OPENAI']['SERPAPI_KEY']
os.environ['SERPER_API_KEY'] = api_config['OPENAI']['SERPER_KEY']

factModel = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')  # Default model is text-davinci-003, seems to be 10x cost of gpt-3.5-turbo

def isPositiveResult(string):
    negativePhrases = ['is not', "isn't", 'ethnicity is unknown', 'unclear', 'is not Jewish',
                       'is not jewish', 'is not jewish', 'he is Christian', 'she is Christian']

    if any(phrase in string for phrase in negativePhrases):
        return False
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action="count", 
                        help="increase output verbosity (e.g., -vv is more than -v)")

    args = parser.parse_args()

    print("=====================================================")

    files = os.listdir('./guest_data')
    name_list = []
    while True:
        for index, file in enumerate(files):
            print('{num} - {dir}'.format(num=index+1, dir=file))
        try:
            x = input('choose a file: ')
            name_list = getListFromFile('guest_data/' + files[int(x)-1])
            break
        except ValueError:
            print('please enter a valid number')

    print("=====================================================")

    logic_chain = load_tools(['serpapi', 'llm-math'], llm=factModel)
    # travel_chain = load_tools(['google-serper', 'open-meteo-api'], llm=factModel)

    agent_decider = initialize_agent(logic_chain,
                                    factModel,
                                    agent='zero-shot-react-description',
                                    verbose=args.verbose)
    
    # Sometimes pops up. If consistent, could identify it with this text
    stopped_text = 'Agent stopped due to iteration limit or time limit'
    
    individuals_dict = {}
    for guest in name_list:
        if not args.verbose:
            try:
                with yaspin(text='Examining {name}'.format(name=guest), color="yellow") as spinner:
                    # If the name we're examining has already been examined, skip it, and add another
                    if guest in individuals_dict:
                        spinner.ok('💥 DUPLICATE ')
                        individuals_dict[guest].num_appearances += 1
                    else: 
                        output = agent_decider.run(get_ethnicity.format(name=guest))
                        deets = IndividualDetails(output, 1)
                        individuals_dict[guest] = deets
                        spinner.ok('✅ ')
            except Exception as e:
                print(e)
                continue
        else:
            try:
                if guest in individuals_dict:
                    print(guest + ' is a duplicate, skipping')
                    individuals_dict[guest].num_appearances += 1
                else: 
                    output = agent_decider.run(get_ethnicity.format(name=guest))
                    deets = IndividualDetails(output, 1)
                    individuals_dict[guest] = deets
            except Exception as e:
                print(e)
                continue


    csv_columns = ['NAME', 'ETHNICITY', 'NATIONALITY', 'APPEARANCES']

    try:
        with open('output.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            # Loop through individuals_dict and write each row to the csv
            for data in individuals_dict:
                # print('guest was : ' + individuals_dict[data].ethnicity)
                writer.writerow({'NAME': data, 'ETHNICITY': individuals_dict[data].ethnicity, 'APPEARANCES': individuals_dict[data].num_appearances})
    except IOError:
        print("I/O error")

    for key in individuals_dict:
        print('RESULT: {key} is {ethnicity} and has been on the show {appearances} times'.format(key=key, ethnicity=individuals_dict[key].ethnicity, appearances=individuals_dict[key].num_appearances))