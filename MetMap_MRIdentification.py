import re
import nltk


##These downloads are necessary for the excecutions
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('punkt_tab')
#nltk.download('averaged_perceptron_tagger_eng')

##Finds the words that are different between two sentences.
def FindDiff(words1, words2):
  for w1, w2 in zip(words1,words2):
    if w1 != w2:
      return w1,w2

##Turns the sentences into natural language tokens.
def NLTK(sentence1, sentence2):
  tokens1 = nltk.word_tokenize(sentence1.lower())
  tokens2 = nltk.word_tokenize(sentence2.lower())
  return tokens1, tokens2

##Uses the regular expression package to find the first quantifier in a sentence.
def RegexFindQuant(sentence):
  if len(re.findall("-?\d+(?:\.\d+)?",sentence)):
    return re.findall("-?\d+(?:\.\d+)?",sentence)[0]
  else:
    return 'null'

##Determines the word level metamorphosis that was applied to the sentence pair, if it doesn't match any of the ones described in the paper, it's indicated as 'Other'.
def MRIdentification(sentence1, sentence2,label):
  #In the PAWS dataset, 0 indicates that two sentences have the same meaning. We are only interested in sentences that have different meaning.
  if label == '0':
    words_sentence1 = sentence1.lower().split()
    words_sentence2 = sentence2.lower().split()
    if ''.join(sorted(words_sentence1)) == ''.join(sorted(words_sentence2)):
      return "WordSwap"
    else:
      all_words = set(words_sentence1).union(set(words_sentence2))
      if len(words_sentence1) == len(words_sentence2) and ((len(all_words) - len(words_sentence1) <= 1) or (len(all_words) - len(words_sentence2) <= 1)):
        diff1, diff2 = FindDiff(words_sentence1, words_sentence2)
        if diff1 == RegexFindQuant(sentence1) and diff2 == RegexFindQuant(sentence2):
          return "QuantSub"
        else:
          tokens1, tokens2 = NLTK(sentence1, sentence2)
          tag1 = nltk.pos_tag(tokens1.pop(tokens1.index(diff1)).split())
          tag2 = nltk.pos_tag(tokens2.pop(tokens2.index(diff2)).split())
          if ('NN' in tag1[0][1] or 'PRP' in tag1[0][1] or 'JJ' in tag1[0][1] or 'RB' in tag1[0][1] or 'VB' in tag1[0][1]) and ('NN' in tag2[0][1] or 'PRP' in tag2[0][1] or 'JJ' in tag2[0][1] or 'RB' in tag2[0][1] or 'VB' in tag2[0][1]):
            if('NN' in tag1[0][1] or 'PRP' in tag1[0][1]) and ('NN' in tag2[0][1] or 'PRP' in tag2[0][1]):
              return "ObjSub"
            elif('JJ' in tag1[0][1] or 'RB' in tag1[0][1]) and ('JJ' in tag2[0][1] or 'RB' in tag2[0][1]):
              return "NegaExp"
            elif 'VB' in tag1[0][1] and 'VB' in tag2[0][1]:
              return "ActSub"
            else:
              return "Other1"
          else:
            return "Other2"
      else:
        if all(x in words_sentence2 for x in words_sentence1):
          if (len(words_sentence2) - len(words_sentence1) <= 2) and ('not' in set(words_sentence2) - set(words_sentence1)):
            return "NegaExp"
          else:
            return "WordDel"
        else:
          return "Other3"
  return "Other"



