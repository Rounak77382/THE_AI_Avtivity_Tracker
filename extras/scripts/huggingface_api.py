#pip install huggingface_hub
from huggingface_hub import InferenceClient
import json
import os

# Ensure the HF_TOKEN environment variable is set
hf_token = os.getenv("HF_TOKEN")
if not hf_token:
    raise ValueError("HF_TOKEN environment variable not set")

repo_id = "RSted/productivity-assessment-gemma-2-9b"
llm_client = InferenceClient(
    model=repo_id,
    token=hf_token,
    timeout=120,
)

alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{}

### Input:
{}

### Response:
"""

def call_llm(inference_client: InferenceClient, instruction: str, input_text: str):
    prompt = alpaca_prompt.format(instruction, input_text, "")
    response = inference_client.post(
        json={
            "inputs": prompt,
            "parameters": {"max_new_tokens": 200},
            "task": "text-generation",
        },
    )
    return json.loads(response.decode())[0]["generated_text"]

instruction = "I will provide a process title representing currently running processes on a computer. Your task is to analyze the process and determine if it is directly productive for a SOFTWARE DEVELOPER.  \nReturn your output as boolean, where each element corresponds to the productivity status of the respective process in the input array. Ensure that the length of the output array matches the input array. Do not include any additional text or explanation in your response."
input_text = "test_removebrackets.py - THEAPP - Cursor"
response = call_llm(llm_client, instruction, input_text)
print(response)