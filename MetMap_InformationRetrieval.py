from scipy.spatial import distance
from sentence_transformers import SentenceTransformer
import json

QuantFile = 'QuantSub.jsonl'
LLMFile = 'LLM.jsonl'

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

quant_sentences = []
with open(QuantFile,'r') as file:
  for line in file:
    quant_sentences.append(json.loads(line))

LLM_sentences = []
with open(LLMFile,'r') as file:
  for line in file:
    LLM_sentences.append(json.loads(line))


def informationRetrieval(sentences):
  for triplet in sentences:
    sentence_vector_base = model.encode(triplet["sentence1"])
    sentence_vector_neg = model.encode(triplet["sentence2"])
    sentence_vector_pos = model.encode(triplet["sentence3"])

    print('Base sentence: ' + triplet["sentence1"])
    print('Positive sentence: ' + triplet["sentence3"])
    print('Negative sentence: ' + triplet["sentence2"])
    distance_base_pos = distance.euclidean(sentence_vector_base,sentence_vector_pos)
    print('The distance between the base and positive vectors is: ' + str(distance_base_pos))
    distance_base_neg = distance.euclidean(sentence_vector_base,sentence_vector_neg)
    print('The distance between the base and negative vectors is: ' + str(distance_base_neg))


    if distance_base_pos < distance_base_neg:
      print('positive distance is lower:' + ' ' + str(distance_base_pos) + ' ' + 'the matching was correct')
    else:
      print('negative distance is lower:' + ' ' + str(distance_base_neg) + ' ' + 'the matching was incorrect')
    print('\n')


print('Information retrieval for sentences with that had a negative sentence generated (QuantSub)')
informationRetrieval(quant_sentences)

print('Information retrieval for sentences that had a positive sentence generated')
informationRetrieval(LLM_sentences)
