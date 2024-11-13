from scipy.spatial import distance
from sentence_transformers import SentenceTransformer


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
  for sentence in sentences:
    sentence_vector_base = model.encode(sentence["sentence1"])
    sentence_vector_neg = model.encode(sentence["sentence2"])
    sentence_vector_pos = model.encode(sentence["sentence3"])

    distance_base_pos = distance.euclidean(sentence_vector_base,sentence_vector_pos)
    print(distance_base_pos)
    distance_base_neg = distance.euclidean(sentence_vector_base,sentence_vector_neg)
    print(distance_base_neg)

    if distance_base_pos < distance_base_neg:
      print('positive distance is lower:' + ' ' + str(distance_base_pos) + ' ' + 'the matching was correct')
    else:
      print('negative distance is lower:' + ' ' + str(distance_base_neg) + ' ' + 'the matching was incorrect')
    print('\n')


print('Information retrieval for sentences with the tag QuantSub')
informationRetrieval(quant_sentences)

print('Information retrieval for sentences with the tags different from Other and QuantSub')
informationRetrieval(LLM_sentences)