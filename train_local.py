import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import SFTTrainer, SFTConfig
from peft import LoraConfig, get_peft_model

# 1. Tải Mô hình siêu nhỏ (Qwen 0.5B) và Tokenizer
model_name = "Qwen/Qwen2.5-0.5B-Instruct"
print(f"Đang tải mô hình {model_name} (khoảng 1-2GB)...")

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

# Tải model (Ép chạy trên CPU)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="cpu", 
    torch_dtype=torch.float32 
)

# 2. Áp dụng kỹ thuật LoRA 
print("⚙️ Đang cấu hình kỹ thuật LoRA...")
peft_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)
model = get_peft_model(model, peft_config)

# 3. Chuẩn bị Dữ liệu
print(" Đang nạp dữ liệu TKB từ file TrainTKB.jsonl...")
dataset = load_dataset("json", data_files="TrainTKB.jsonl", split="train")

def format_prompt(examples):
    texts = []
    for messages in examples["messages"]:
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
        texts.append(text)
    return {"text": texts}

dataset = dataset.map(format_prompt, batched=True)

# 4. Cấu hình Tham số Huấn luyện (ĐÃ CẬP NHẬT THEO CHUẨN MỚI NHẤT)
print("Khởi tạo cấu hình SFTConfig...")
training_args = SFTConfig(
    output_dir="./tkb_model_local",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    logging_steps=5,
    max_steps=50, 
    save_strategy="no", 
    use_cpu=True, 
    report_to="none",
    dataset_text_field="text", 
    max_length=512,        
)

# 5. Khởi tạo Trainer và Bắt đầu
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    processing_class=tokenizer,
    args=training_args,
)

print("BẮT ĐẦU QUÁ TRÌNH HUẤN LUYỆN BẰNG CPU...")
trainer.train()

# 6. Lưu Mô hình thành quả
print("Huấn luyện xong! Đang lưu mô hình...")
trainer.model.save_pretrained("./tkb_model_final")
tokenizer.save_pretrained("./tkb_model_final")
print("THÀNH CÔNG! Mô hình của em đã nằm trong thư mục 'tkb_model_final'")