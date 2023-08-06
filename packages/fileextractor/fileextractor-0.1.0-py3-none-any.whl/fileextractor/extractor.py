import pandas as pd
import json
import yaml
import ruamel.yaml
import sys
from collections import OrderedDict
import numpy as np

def nlu_dict_to_yaml(dict_file:dict, file_name:str):
    """
    Written dict data into yaml file.

    Args:
        dict_file (dict): dictionary containting data to be written

    Returns:
        nlu_data_from_sheets_eng.yml:  nlu data file containing all the english intents and examples 
        nlu_data_from_sheets_swh.yml:  nlu data file containing all the swahili intents and examples       
     
    """

    yaml_data = yaml.dump(dict_file, Dumper=yaml.CDumper, sort_keys=False, default_flow_style=False)
    # print(yaml_data)
    yaml_data = yaml_data.replace("examples:\n", "examples: |\n")
    yaml_data = yaml_data.replace("  - ", "    - ")
    # yaml_data = yaml_data.replace("    ", "    - ")
    # yaml_data = yaml_data.replace("\n- ", "\n    - ")
    # yaml_data = yaml_data.replace("- ", "  - ", -1)

    with open(f"bot\data\{file_name}.yml", "w") as file:
        file.write(yaml_data)
    
    
def response_dict_to_yaml(dict_file:dict, file_name:str):
    """
    Written dict data into yaml file.

    Args:
        dict_file (dict): dictionary containting data to be written

    Returns:
        responses_eng.yml:  file containing all the english responses
        responses_swh.yml:  file containing all the swahili responses
        
    """

    yaml_data = yaml.dump(dict_file, Dumper=yaml.CDumper, sort_keys=False, default_flow_style=False)
    # print(yaml_data)
    # yaml_data = yaml_data.replace("examples:\n", "examples: |\n")
    yaml_data = yaml_data.replace("- ", "  ")
    yaml_data = yaml_data.replace("    text:", "  - text:")
    # yaml_data = yaml_data.replace("\n- ", "\n    - ")
    # yaml_data = yaml_data.replace("- ", "  - ", -1)

    with open(f"bot\data\{file_name}.yml", "w") as file:
        file.write(yaml_data)

def stories_dict_to_yaml(dict_file:dict, file_name:str):
    """
    Written dict data into yaml file.

    Args:
        dict_file (dict): dictionary containting data to be written

    Returns:
       
        stories.yml:    stories file containing all the story paths
      
    """

    yaml_data = yaml.dump(dict_file, Dumper=yaml.CDumper, sort_keys=False, default_flow_style=False)
    # print(yaml_data)
    yaml_data = yaml_data.replace("examples:\n", "examples: |\n")
    yaml_data = yaml_data.replace("  - ", "    - ")
    yaml_data = yaml_data.replace("    - utter", "  - action: utter")
    yaml_data = yaml_data.replace("    - ", "  - intent: ")
    # yaml_data = yaml_data.replace("- ", "  - ", -1)

    with open(f"bot\data\{file_name}.yml", "w") as file:
        file.write(yaml_data)


def excel_to_yaml(excel_file: str, ):
    """
    Extract data for every intent from  all sheets in an excel file and write it into a json file .

    Args:
        excel_file (str): path to excel file 

    Returns:
        nlu_data_from_sheets_eng.yml:  nlu data file containing all the english intents and examples 
        nlu_data_from_sheets_swh.yml:  nlu data file containing all the swahili intents and examples  
        stories.yml:    stories file containing all the story paths
        responses_eng.yml:  file containing all the english responses
        responses_swh.yml:  file containing all the swahili responses
    """

    # read excel sheet
    df = pd.read_excel(excel_file, sheet_name=None)
  
    df_list = list(df)
    nlu_data_from_sheets_eng = []
    nlu_data_from_sheets_swh = []
    responses_eng = []
    responses_swh = []

    for sheet in df_list[:-1]:
        # dropping all rows with nothing but nan values
        intent_sheet = df[sheet]
        intent_sheet.dropna(how='all', inplace=True)
        # print(intent_sheet)

        # print(df.head(30))
        # print(intent_sheet.columns)

        intent_sheet = intent_sheet.rename(columns={col: col.strip()
                             for col in intent_sheet.columns})
        # list of all intents
        intents = intent_sheet[intent_sheet.columns[0]].unique()
        # print(intents)

        data_records = intent_sheet.to_dict(orient='records')
        # print(data_records)

        

        # loop through dict and pick anything with same intent_name
        
        for intent in intents:
            nlu_eng = dict()
            nlu_swh = dict()

            res_eng = {}
            res_eng_dict = dict()

            res_swh = {}
            res_swh_dict = dict()

            english = []
            swahili = []
            # images = []

            for record in data_records:
                if 'intent_name' in record.keys() and intent == record['intent_name']:
                    intent_name = record['intent_name']
                    # english =record['english examples/questions']
                    english.append(
                        record['english examples/questions'])
                    response_name = record['response name']
                    eng_response = record['english responses/answers']
                    swahili.append(record['swahili example/questions'])
                    swh_response = record['swahili responses/answers']
                    image = record['images']

            # nlu_eng['intent'] = intent_name
            # nlu_eng['examples'] = english
            nlu_eng.update({'intent':intent_name, 'examples':english})
            
            nlu_swh.update({'intent':intent_name, 'examples':swahili})
            # nlu_swh['intent'] = intent_name
            # nlu_swh['examples'] = swahili
            # print(eng_response)
            res_eng['text'] = eng_response
            

            # if np.isnan(eng_response):
            #     res_eng['text'] = ''
            # else:
            #     res_eng['text'] = eng_response

            if np.isnan(swh_response):
                res_swh['text'] = ''
            else:
                res_swh['text'] = swh_response
            
            # print(images)
            if np.isnan(image):
                res_eng['image'] = ''
                res_swh['image'] = ''
            else:
                res_eng['image'] = image
                res_swh['image'] = image


            res_eng_dict.update({response_name:res_eng})
        
            res_swh_dict.update({response_name:res_swh})


            # record_results['response_name'] = response_name
            # record_results['eng_response'] = eng_response
            # record_results['swahili'] = swahili
            # record_results['swh_response'] = swh_response
            # record_results['images'] = images
            # sheet_results.append(record_results)
            # nlu_data_from_sheets_eng['version'] = '3.1'
            nlu_data_from_sheets_eng.append(nlu_eng)
            nlu_data_from_sheets_swh.append(nlu_swh)
            responses_eng.append(res_eng_dict)
            responses_swh.append(res_swh_dict)

    #final nlu data file
    final_nlu_eng = dict(version='3.1', nlu=nlu_data_from_sheets_eng)
    final_nlu_swh = dict(version='3.1', nlu=nlu_data_from_sheets_swh)
    # final_nlu_eng['version'] = '3.1'
    # final_nlu_eng['nlu'] = nlu_data_from_sheets_eng

    #final resposes file
    final_res_eng = dict(responses=responses_eng)
    final_res_swh = dict(responses=responses_swh)

    #change to ordered dict
    # nlu_eng_ordered = OrderedDict(nlu_eng.items())

    story_sheet_name = df_list[-1]
    story_sheet = df[story_sheet_name] 
    # print(story_sheet)
    
    story_sheet.dropna(how='all', inplace=True)
    story_sheet = story_sheet.rename(columns={col: col.strip()
                             for col in story_sheet.columns})
    story_records = story_sheet.to_dict(orient='records')
    story_paths = story_sheet[story_sheet.columns[0]].unique()
    

    all_stories = []
    
    
    for path in story_paths:
        stories = {}
        steps = []
        for record in story_records:
            # print(record)
            if path == record['stories']:
                story = record['stories']
                steps.append(record['steps'])
            stories['story']  =story
            stories['steps']  =steps
        all_stories.append(stories)

    # print(final_nlu_swh)  
    nlu_dict_to_yaml(final_nlu_eng, 'nlu_eng')
    nlu_dict_to_yaml(final_nlu_swh, 'nlu_swh')

    # print(final_res_eng)

    response_dict_to_yaml(final_res_eng, 'response_eng')
    response_dict_to_yaml(final_res_swh, 'response_swh')

    # print(all_stories)

    all_stories_dict = dict(version='3.1', stories=all_stories)
    stories_dict_to_yaml(all_stories_dict, 'stories')

    # return  final_nlu_eng, final_nlu_swh
# , nlu_data_from_sheets_swh, responses_eng, responses_swh, all_stories

# print(excel_to_yaml('bot\odpcdata.xlsx'))
# excel_to_yaml('bot\odpcdata.xlsx')
# print(nlu_eng)

    
    
# Open YAML file
# with open(r'bot\data\nlu.yml', 'r') as file:
#     # Load YAML data into dictionary
#     data = yaml.safe_load(file)

# Print dictionary
# print(data)

# import yaml

# # Define the data as a dictionary
# data = {
    
#     'vegetables': ['carrot', 'cucumber', 'lettuce'],
#     'animals': {
#         'mammals': ['dog', 'cat', 'horse'],
#         'birds': ['parrot', 'canary', 'owl'],
#     },
#     'fruits': ['apple', 'banana', 'cherry']
# }

# # Use the PyYAML library to dump the data to a YAML file
# with open('data.yaml', 'w') as file:
#     yaml.dump(data, file)

# import yaml

# data = {
#     "version": "3.1",
#     "nlu": [
#         {
#             "intent": "greet",
#             "examples": "|-\n  - hey\n  - hello\n  - hi\n  - hello there\n  - good morning\n  - good evening\n  - moin\n  - hey there\n  - let's go\n  - hey dude\n  - goodmorning\n  - goodevening\n  - good afternoon"
#         }
#     ]
# }

# with open('file.yml', 'w') as f:
#     yaml.dump(data, f, sort_keys=False)

# import yaml

# data = {
#     'version': '3.1',
#     'nlu': [
#         {
#             'intent': 'raise_complaint',
#             'examples': [
#                 'how do i raise a complaint?',
#                 'I have been denied access to my data',
#                 'what should i do when my data has been shared?',
#                 'where do i raise a complaint?',
#                 'how do I file a complaint?',
#                 'i have a complaint?',
#                 'i have been hacked?'
#             ]
#         }
#     ]
# }

# yaml_data = yaml.dump(data, default_flow_style=False)
# yaml_data = yaml_data.replace("- ", "    - ")

# # create list of indented examples
# examples_list = ["    - {}".format(example) for example in data['nlu'][0]['examples']]
# examples_string = "\n".join(examples_list)

# # replace examples with indented list
# yaml_data = yaml_data.replace("examples:\n", "examples: |\n{}\n".format(examples_string))

# with open('data.yaml', 'w') as f:
#     f.write(yaml_data)

