from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch
import json

LLMFile = 'LLM.jsonl'

model = "tiiuae/falcon-7b-instruct"

tokenizer = AutoTokenizer.from_pretrained(model)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    device_map="auto",
    )

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
            ##provvisorio
            print(f"Result: {seq['generated_text']}")
            print('\n')
