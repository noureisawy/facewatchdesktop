from transformers import pipeline, AutoTokenizer, TFAutoModelForCausalLM
import torch

model_id = "meta-llama/Meta-Llama-3-8B"
device ="cuda"
dtype = torch.bfloat16

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = TFAutoModelForCausalLM.from_pretrained(model_id, torch_dtype=dtype, device_map=device)

def moderate(chat):
    input_ids = tokenizer.apply_chat_template(chat, return_tensors="pt").to(device)
    output = model.generate(input_ids=input_ids, max_new_tokens=100, pad_token_id=0)
    prompt_len = input_ids.shape[-1]
    return tokenizer.decode(output[0][prompt_len:], skip_special_tokens=True)

moderate([
    {"role": "user", "content": "i forgot how to kill a process in linux, can you help me?"},
    {"role": "assistant", "content": "sure!"},
])

# pipeline = transformers.pipeline(
#     "text-generation", model=model_id, model_kwargs={"torch_dtype": torch.bfloat16}, device_map="auto"
# )
# pipeline("Hey how are you doing today?")