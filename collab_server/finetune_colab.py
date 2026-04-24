# Google Colab Fine-tuning Script (4-bit) - Upload on Top
# ========================================================

# Step 1: Upload Dataset (Run this in Colab first)
# from google.colab import files
# uploaded = files.upload()
# DATA_FILE = list(uploaded.keys())[0] 
# print(f"Using file: {DATA_FILE}")

# Step 2: Install Dependencies
# !pip install unsloth
# !pip install --no-deps "xformers<0.0.29" "trl<0.13.0" peft accelerate bitsandbytes

# Step 3: Mount Google Drive
# from google.colab import drive
# drive.mount('/content/drive')

import os
import torch
import shutil
from unsloth import FastLanguageModel
from unsloth.chat_templates import get_chat_template
from datasets import load_dataset
from transformers import TrainingArguments, DataCollatorForSeq2Seq
from trl import SFTTrainer

# Step 4: Config
MODEL_ID     = "unsloth/Qwen3-1.7B-unsloth-bnb-4bit"
MAX_SEQ_LEN  = 512

# Step 5: Load Model
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name     = MODEL_ID,
    max_seq_length = MAX_SEQ_LEN,
    dtype          = None,
    load_in_4bit   = True,
)

# Step 6: Attach LoRA
model = FastLanguageModel.get_peft_model(
    model,
    r              = 16,
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj"],
    lora_alpha     = 16,
    lora_dropout   = 0,
    bias           = "none",
    use_gradient_checkpointing = "unsloth",
    random_state   = 42,
)

# Step 7: Load & Format Dataset
tokenizer = get_chat_template(tokenizer, chat_template="qwen-2.5")

def format_chat(example):
    return {
        "text": tokenizer.apply_chat_template(
            example["messages"],
            tokenize=False,
            add_generation_prompt=False,
        )
    }

dataset = load_dataset("json", data_files=DATA_FILE, split="train")
dataset = dataset.map(format_chat, remove_columns=["messages"])

# Step 8: Train
trainer = SFTTrainer(
    model              = model,
    tokenizer          = tokenizer,
    train_dataset      = dataset,
    dataset_text_field = "text",
    max_seq_length     = MAX_SEQ_LEN,
    data_collator      = DataCollatorForSeq2Seq(tokenizer=tokenizer),
    args = TrainingArguments(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        warmup_steps                = 10,
        num_train_epochs            = 3,
        learning_rate               = 2e-4,
        fp16                        = not torch.cuda.is_bf16_supported(),
        bf16                        = torch.cuda.is_bf16_supported(),
        logging_steps               = 1,
        output_dir                  = "outputs",
        save_strategy               = "epoch",
        report_to                   = "none",
    ),
)

trainer.train()

# Step 9: Save and Upload to Google Drive
model.save_pretrained("qwen3_activity_lora")
tokenizer.save_pretrained("qwen3_activity_lora")

# Zip and move to Drive
# !zip -r qwen3_activity_lora.zip qwen3_activity_lora
# shutil.copy("qwen3_activity_lora.zip", "/content/drive/MyDrive/qwen3_activity_lora.zip")
# print("✅ Saved to Google Drive!")
