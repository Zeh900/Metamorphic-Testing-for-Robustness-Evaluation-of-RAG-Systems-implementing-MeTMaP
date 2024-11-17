from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch
import json

LLMFile = 'LLM.jsonl'
new_contents = []
model = "tiiuae/falcon-7b-instruct"

def add_final_entry(sentence1, sentence2, sentence3,sentences):
  sentences.append({"sentence1": sentence1, "sentence2": sentence2, "sentence3": sentence3})

tokenizer = AutoTokenizer.from_pretrained(model)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    )

##Generating the third sentence and adding it to its sentence pair
with open(LLMFile,'r') as file:
    for line in file:
        base = json.loads(line)['sentence1']
        sequences = pipeline(
            "Paraphrase the following sentence while not changing its meaning at all: " +  base,
            max_length=200,
            do_sample=True,
            top_k=10,
            num_return_sequences=1,
            eos_token_id=tokenizer.eos_token_id,
        )
        
        for seq in sequences:
            response = str(seq['generated_text']).split('\n')[1]
            print(f"Result: {seq['generated_text']}")
            print('\n')
            add_final_entry(base,json.loads(line)['sentence2'],response,new_contents)


with open(LLMFile, 'w') as file:
  for d in new_contents:
    json.dump(d,file,ensure_ascii=False)
    file.write('\n')

            
