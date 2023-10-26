import torch
from transformers import MarianMTModel, MarianTokenizer
from transformers import AutoTokenizer, DataCollatorForSeq2Seq, Seq2SeqTrainer, Seq2SeqTrainingArguments 
from datasets import load_dataset

# Define your dataset file or directory
dataset_path = "verified_data.csv"  # Replace with the actual path

# Load your dataset using Hugging Face's datasets library
dataset = load_dataset('csv', data_files=dataset_path)

# Define the source and target languages
source_language = "en"  # English
target_language = "tw"  # Twi

# Initialize the Marian tokenizer and model
model_name = f'Helsinki-NLP/opus-mt-{source_language}-{target_language}'
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

# Tokenize and prepare the dataset for translation
def tokenize_function(examples):
    return tokenizer(examples["English"], examples["Akuapem Twi"], padding="max_length", truncation=True)

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Initialize tokenizer and collator
tokenizer = AutoTokenizer.from_pretrained(model_name)
data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

# Initialize training arguments
output_dir = "fine_tuned_model"  # Replace with your desired output directory
batch_size = 4  # Adjust as needed
num_epochs = 1  # Adjust as needed

training_args = Seq2SeqTrainingArguments(
    output_dir=output_dir,
    per_device_train_batch_size=batch_size,
    evaluation_strategy="steps",
    save_total_limit=5,
    save_steps=500,
    remove_unused_columns=False,
    num_train_epochs=num_epochs,
    load_best_model_at_end=True,
    # Enable padding and truncation
    logging_steps=10,
    push_to_hub=False,  # Set to True if you want to upload to the Hugging Face Model Hub
)

# Initialize Trainer
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["train"],  # Use the same dataset for evaluation for simplicity
    tokenizer=tokenizer,
)

# Fine-tune the model
trainer.train()

# Save the fine-tuned model
model.save_pretrained(output_dir)

# Optionally, save the tokenizer
tokenizer.save_pretrained(output_dir)
