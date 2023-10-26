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

english_sentences = dataset['English']
akuapem_twi_sentences = dataset['Akuapem Twi']



# Tokenize and prepare the dataset for translation
def tokenize_function(examples):
    inputs = tokenizer(examples["English"], padding="max_length", truncation=True, return_tensors="pt")
    targets = tokenizer(examples["Akuapem Twi"], padding="max_length", truncation=True, return_tensors="pt")
    return {
        "input_ids": inputs["input_ids"],
        "attention_mask": inputs["attention_mask"],
        "labels": targets["input_ids"],
    }

flattened_dataset = {"English": english_sentences, "Akuapem Twi": akuapem_twi_sentences}
tokenized_datasets = flattened_dataset.map(tokenize_function, batched=True)

# Initialize tokenizer and collator
tokenizer = AutoTokenizer.from_pretrained(model_name)
data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

# Initialize training arguments
training_args = Seq2SeqTrainingArguments(
    output_dir="fine_tuned_model",
    per_device_train_batch_size=8,  # You can adjust this batch size
    evaluation_strategy="steps",
    save_total_limit=5,
    save_steps=500,
    remove_unused_columns=False,
    num_train_epochs=3,  # Adjust the number of training epochs
    load_best_model_at_end=True,
)

# Initialize Trainer
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    data_collator=data_collator,  # Use the data collator
    train_dataset=tokenized_datasets["train"],
    tokenizer=tokenizer,
)

# Fine-tune the model
trainer.train()

# Save the fine-tuned model
model.save_pretrained("fine_tuned_model")

# Optionally, save the tokenizer
tokenizer.save_pretrained("fine_tuned_model")
