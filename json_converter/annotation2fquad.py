# -*- coding: utf8 -*-

# The path (sys.argv[0]) must point to a folder with 3 subfolders inside :
#     -> json : contains .json files from the annotation process
#     -> contex : contains the context .txt files 
#     -> json : initially empty, it will contain the output .json files
#
# For a given context, the context should be TITLE.txt, the annotation file should be TITLE.json with the same TITLE. The corresponding result will be TITLE.json.
#
# e.g. for Google Drive : sys.argv[0] = '/content/drive/My Drive/DAC'

import json
import sys
import os


def import_data(path, title):
    with open(f'{path}/json/{title}.json') as f:
        data = json.load(f)
    return data


def import_context(path, title):
    with open(f'{path}/context/{title}.txt', 'r') as f:
        context = f.read()
    return context


def get_output_dict(data, context, title):
    output_dict = {
        'data' : [{
            'title' : title,
            'paragraphs' : [{
                'context' : context,
                'qas' : [] # will be completed
                }]
            }]
        }
    id = 0
    questions = {} # stores the questions that have already appeared
    for q in data['annotations'][0]['value']:
        if q['question'] in questions.keys(): # if the question has already appeared, we just complete with the new answer
            output_dict['data'][0]['paragraphs'][0]['qas'][questions['questions']]['answer'].append({
                        'answer_start' : q['answer_start'],
                        'text' : q['answer'],
                        'answer_type' : q['answer_type'],
                        'qa_type' : q['qa_type']
                    })
        else: # if the question appears for the first time, we add it both to the ouput dict and to the questions dict
            output_dict['data'][0]['paragraphs'][0]['qas'].append({
                'answer' : [
                      {
                          'answer_start' : q['answer_start'],
                          'text' : q['answer'],
                          'answer_type' : q['answer_type'],
                          'qa_type' : q['qa_type']
                      }
                ],
                'question' : q['question'],
                'question_type' : q['question_type'],
                'id': str(id).zfill(5) # the id are string corresponding to int starting from 0 and made of 5 digits
            })
            questions[q['question']] = id
            id += 1
    return output_dict


def save_output_json(output_dict, title):
    with open(f'/content/drive/My Drive/DAC/output/{title}.json', 'w+') as f:
        f.write(json.dumps(output_dict))


if __name__ == '__main__':
    """
    sys.argv[0] stands for the path of the root directory (without the final slash)
    """

    path = sys.argv[0]
    for f in os.listdir(f"{path}/context"):
        title = f.split('.txt')[0]
        data = import_data(path, title)
        context = import_context(path, title)
        output_dict = get_output_dict(data, context, title)
        save_output_json(output_dict, title)