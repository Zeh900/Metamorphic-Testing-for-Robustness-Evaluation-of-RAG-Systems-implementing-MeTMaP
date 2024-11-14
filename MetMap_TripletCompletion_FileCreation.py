import random
import pandas as pd
import re
import json
import ast

tagged_sentences = []
quantSub_sentences = []
LLM_sentences = []


def add_tagged_entry(sentence1, sentence2,label):
  tagged_sentences.append({"sentence1": sentence1, "sentence2": sentence2,"label": label, "tag": MRIdentification(sentence1, sentence2,label)})

def add_final_entry(sentence1, sentence2, sentence3,sentences):
  sentences.append({"sentence1": sentence1, "sentence2": sentence2, "sentence3": sentence3})



file_name = '/content/dev_modificato.tsv'
dataset_full = pd.read_csv(file_name, sep = '\t', engine='python', names = ['id', 'sentence1', 'sentence2', 'label'])

for index in range(1,100):
  add_tagged_entry(dataset_full.loc[index].sentence1, dataset_full.loc[index].sentence2, dataset_full.loc[index].label)

QuantFile = 'QuantSub.jsonl'
LLMFile = 'LLM.jsonl'


##If the tag in an entry is simply 'Other', it means that the two sentences have the same meaning, so a negative sentence is created using random number generation.
##Otherwise, if the MR was actually identified, a placeholder sentence is assigned, to be actually added later by a LLM.
for entry in tagged_sentences:
  if entry["tag"] == "Other":
    quant = RegexFindQuant(entry["sentence1"])
    if quant != 'null':
      rand_mult = 1
      while rand_mult == 1:
        rand_mult = random.uniform(0,2)
      new_quant = int(quant) * rand_mult
      add_final_entry(entry["sentence1"],re.sub(quant,str(int(new_quant)),entry["sentence1"]),entry["sentence2"],quantSub_sentences)
  elif "Other" not in entry["tag"]:
    add_final_entry(entry["sentence1"], entry["sentence2"],' ',LLM_sentences)


with open(QuantFile, 'w') as file:
  for d in quantSub_sentences:
    json.dump(d,file)
    file.write('\n')

with open(LLMFile, 'w') as file:
  for d in LLM_sentences:
    json.dump(d,file)
    file.write('\n')







