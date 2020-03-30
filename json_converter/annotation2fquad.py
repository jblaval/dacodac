# -*- coding: utf8 -*-

import json
import os
import random as rd


PATH = "/content/drive/My Drive/dataset_giec/temp_annotation"


def import_data(path, title):
    with open(f"{path}/json/{title}.json") as f:
        data = json.load(f)
    return data


def import_context(path, title):
    with open(f"{path}/context/{title}.txt", "r") as f:
        context = f.read()
    return context


def get_output_dict(data, context, title, output_dict, curr_id):
    current_entry = {
        "title": title,
        "paragraphs": [{"context": context, "qas": []}],  # will be completed
    }
    id = curr_id
    questions = {}  # stores the questions that have already appeared
    for q in data["annotations"][0]["value"]:
        if (
            q["question"] in questions.keys()
        ):  # if the question has already appeared, we just complete with the new answer
            current_entry["paragraphs"][0]["qas"][questions[q["question"]] - curr_id][
                "answer"
            ].append(
                {
                    "answer_start": q["answer_start"],
                    "text": q["answer"]  # ,
                    #'answer_type' : q['answer-type'],
                    #'qa_type' : q['qa_type']
                }
            )
        else:  # if the question appears for the first time, we add it both to the ouput dict and to the questions dict
            current_entry["paragraphs"][0]["qas"].append(
                {
                    "answer": [
                        {
                            "answer_start": q["answer_start"],
                            "text": q["answer"]  # ,
                            #'answer_type' : q['answer-type'],
                            #'qa_type' : q['qa_type']
                        }
                    ],
                    "question": q["question"],
                    #'question_type' : q['question_type'],
                    "id": str(id).zfill(
                        5
                    ),  # the id are string corresponding to int starting from 0 and made of 5 digits
                }
            )
            questions[q["question"]] = id
            id += 1
    output_dict["data"].append(current_entry)
    return (output_dict, id)


def save_output_json(path, output_dict, title):
    with open(f"{path}/output/{title}.json", "w+", encoding="utf-8") as f:
        f.write(json.dumps(output_dict, ensure_ascii=False))

# main code

TRAIN_PROPORTION = 0.85

all_files = os.listdir(f"{PATH}/context")
rd.shuffle(all_files)
switch_idx = int(TRAIN_PROPORTION * len(all_files))
train_files, valid_files = all_files[:int(switch_idx)], all_files[switch_idx:]

output_dict = {
    'data' : []
}
curr_id = 0
for f in train_files:
  title = f.split('.txt')[0]
  data = import_data(PATH, title)
  context = import_context(PATH, title)
  output_dict, curr_id = get_output_dict(data, context, title, output_dict, curr_id)
save_output_json(PATH, output_dict, 'train')

output_dict = {
    'data' : []
}
curr_id = 0
for f in valid_files:
  title = f.split('.txt')[0]
  data = import_data(PATH, title)
  context = import_context(PATH, title)
  output_dict, curr_id = get_output_dict(data, context, title, output_dict, curr_id)
save_output_json(PATH, output_dict, 'valid')
