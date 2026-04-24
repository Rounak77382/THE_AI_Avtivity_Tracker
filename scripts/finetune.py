"""
scripts/finetune.py
===================
Runs LoRA fine-tuning on the Qwen3-1.7B-Instruct 4-bit model using Unsloth.
This script is optimized for 4GB VRAM (e.g., GTX 1650).

Run from the project root:
    python scripts/finetune.py

Input  : dataset/merged_train.jsonl
Output : models/qwen3_activity_lora/ (PEFT adapter weights)
"""

# Unsloth/Triton Windows Compatibility Hack
import sys
import os
import importlib.machinery
from types import ModuleType

def mock_triton():
    from dataclasses import dataclass
    from typing import Any

    class Mock(ModuleType):
        def __init__(self, name):
            super().__init__(name)
            self.__file__ = os.path.abspath(__file__)
            self.__path__ = []
            self.__spec__ = importlib.machinery.ModuleSpec(name, None)
            self.__version__ = "3.0.0"
        def __getattr__(self, name):
            if name == "AttrsDescriptor":
                @dataclass
                class AttrsDescriptor:
                    divisible_by_16: Any = None
                    equal_to_1: Any = None
                    ids_of_folded_args: Any = None
                return AttrsDescriptor
            if name == "__all__": return []
            return Mock(f"{self.__name__}.{name}")
        def __call__(self, *args, **kwargs): return Mock("call")
        def __mro_entries__(self, bases):
            return (type(self.__name__, (), {}),)

    class TritonLoader:
        def create_module(self, spec):
            return Mock(spec.name)
        def exec_module(self, module):
            module.Config = type("Config", (), {"__init__": lambda *args, **kwargs: None})

    class TritonImportFinder:
        def find_spec(self, fullname, path, target=None):
            if fullname == "triton" or fullname.startswith("triton."):
                return importlib.machinery.ModuleSpec(fullname, TritonLoader())
            return None

    sys.meta_path.insert(0, TritonImportFinder())
    print("DEBUG: Global Triton import interceptor applied")

mock_triton()

# Unsloth MUST be imported before transformers/trl/peft
from unsloth import FastLanguageModel
from unsloth.chat_templates import get_chat_template

import torch
from datasets import load_dataset
from transformers import TrainingArguments, DataCollatorForSeq2Seq
from trl import SFTTrainer

# ── Config ────────────────────────────────────────────────────────────────────
_HERE        = os.path.dirname(os.path.abspath(__file__))
_PROJ_ROOT   = os.path.dirname(_HERE)
DATA_FILE    = os.path.join(_PROJ_ROOT, "dataset", "merged_train.jsonl")
OUT_CHECKPTS = os.path.join(_PROJ_ROOT, "models", "checkpoints")
OUT_LORA     = os.path.join(_PROJ_ROOT, "models", "qwen3_activity_lora")

MODEL_ID     = "unsloth/Qwen3-1.7B-unsloth-bnb-4bit"
MAX_SEQ_LEN  = 512

if not os.path.exists(DATA_FILE):
    raise FileNotFoundError(f"Training data not found at: {DATA_FILE}")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Loading {MODEL_ID} in 4-bit mode (GTX 1650 safe)...")

    # 1. Load base model
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name     = MODEL_ID,
        max_seq_length = MAX_SEQ_LEN,
        dtype          = None,  # auto-detect (fp16 / bf16)
        load_in_4bit   = True,
    )

    # 2. Apply chat template
    tokenizer = get_chat_template(tokenizer, chat_template="qwen-2.5")

    # 3. Attach LoRA adapters
    print("Attaching LoRA adapters...")
    model = FastLanguageModel.get_peft_model(
        model,
        r              = 16,
        lora_alpha     = 16,
        lora_dropout   = 0,
        target_modules = [
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj"
        ],
        bias           = "none",
        use_gradient_checkpointing = "unsloth",  # Critical for 4GB VRAM
        random_state   = 42,
    )

    # 4. Load & format dataset
    print(f"Loading dataset from {DATA_FILE}...")
    dataset = load_dataset("json", data_files=DATA_FILE, split="train")

    def format_chat(example):
        return {
            "text": tokenizer.apply_chat_template(
                example["messages"],
                tokenize=False,
                add_generation_prompt=False,
            )
        }

    dataset = dataset.map(format_chat, remove_columns=["messages"])
    num_samples = len(dataset)
    print(f"Dataset mapped. Total samples: {num_samples}")

    # 5. Train
    # Adjust epochs based on dataset size
    epochs = 3
    if num_samples < 500:
        epochs = 4
    if num_samples > 2000:
        epochs = 2

    print(f"Starting training for {epochs} epochs...")
    trainer = SFTTrainer(
        model              = model,
        tokenizer          = tokenizer,
        train_dataset      = dataset,
        dataset_text_field = "text",
        max_seq_length     = MAX_SEQ_LEN,
        data_collator      = DataCollatorForSeq2Seq(tokenizer=tokenizer),
        args = TrainingArguments(
            per_device_train_batch_size = 2,
            gradient_accumulation_steps = 4,  # Effective batch size = 8
            warmup_steps                = 10,
            num_train_epochs            = epochs,
            learning_rate               = 2e-4,
            fp16                        = not torch.cuda.is_bf16_supported(),
            bf16                        = torch.cuda.is_bf16_supported(),
            logging_steps               = 1,
            output_dir                  = OUT_CHECKPTS,
            save_strategy               = "epoch",
            report_to                   = "none",
        ),
    )

    trainer.train()
    print("Fine-tuning complete!")

    # 6. Save LoRA adapter
    os.makedirs(OUT_LORA, exist_ok=True)
    model.save_pretrained(OUT_LORA)
    tokenizer.save_pretrained(OUT_LORA)
    print(f"✅ LoRA adapter saved to: {OUT_LORA}")
    print("\nNext step: run  python scripts/export_gguf.py")
