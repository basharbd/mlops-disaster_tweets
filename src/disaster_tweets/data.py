import torch
import pandas as pd
from torch.utils.data import Dataset, DataLoader
from transformers import DistilBertTokenizer

class DisasterTweetsDataset(Dataset):
    def __init__(self, data_path, tokenizer, max_len=128):
        self.data = pd.read_csv(data_path)
        self.tokenizer = tokenizer
        self.max_len = max_len
        
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        text = str(self.data.loc[index, 'text'])
        label = self.data.loc[index, 'target']
        
        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_len,
            return_token_type_ids=False,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )
        
        return {
            'text': text,
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'label': torch.tensor(label, dtype=torch.long)
        }

def process_data(raw_path, processed_path):
    """
    Loads raw data, tokenizes it, and saves the processed tensors.
    """
    print(f"Processing data from {raw_path}...")
    
    # 1. Load Data
    df = pd.read_csv(raw_path)
    
    # 2. Split into Train/Validation (80/20)
    train_size = int(0.8 * len(df))
    train_df = df.sample(frac=1, random_state=42) # Shuffle
    val_df = df.drop(train_df.index)
    
    train_df = train_df[:train_size]
    val_df = train_df[train_size:]
    
    # 3. Save Processed Splits
    train_df.to_csv(f"{processed_path}/train_processed.csv", index=False)
    val_df.to_csv(f"{processed_path}/val_processed.csv", index=False)
    
    print(f"Data saved to {processed_path}")

if __name__ == '__main__':
    # This runs when you execute 'python src/disaster_tweets/data.py'
    process_data('data/raw/train.csv', 'data/processed')