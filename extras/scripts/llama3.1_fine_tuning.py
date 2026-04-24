alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{}

### Input:
{}

### Response:
{}"""

EOS_TOKEN = tokenizer.eos_token # Must add EOS_TOKEN

def formatting_prompts_func(examples):
    instructions = examples["instruction"]
    inputs       = examples["input"]
    outputs      = examples["output"]
    texts = []
    for instruction, input, output in zip(instructions, inputs, outputs):
        # Must add EOS_TOKEN, otherwise your generation will go on forever!
        text = alpaca_prompt.format(instruction, input, output) + EOS_TOKEN
        texts.append(text)
    return { "text" : texts, }

# Convert the loaded data to the format expected by your script
instructions = [item['instruction'] for item in data]
inputs = [item['input'] for item in data]
outputs = [item['output'] for item in data]

# Create a dataset dictionary
dataset_dict = {
    'instruction': instructions,
    'input': inputs,
    'output': outputs
}

# Apply the formatting function to your dataset
formatted_dataset = formatting_prompts_func(dataset_dict)


from datasets import load_dataset
# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Load your dataset from Google Drive
import json

# Replace 'path_to_your_dataset.json' with the actual path to your dataset in Google Drive
dataset_path = '/content/drive/My Drive/real_data_set.json'
# Load the custom dataset from data.json
dataset = load_dataset('json', data_files=dataset_path,split='train')
print(dataset)