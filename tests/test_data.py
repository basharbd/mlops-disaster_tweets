import os
import pytest
import torch
from disaster_tweets.data import DisasterTweetsDataset

class MockTokenizer:
    def encode_plus(self, text, add_special_tokens=True, max_length=128,
                    return_token_type_ids=False, padding='max_length',
                    truncation=True, return_attention_mask=True, return_tensors='pt'):
        return {
            "input_ids": torch.ones((1, max_length), dtype=torch.long),
            "attention_mask": torch.ones((1, max_length), dtype=torch.long)
        }

@pytest.mark.skipif(not os.path.exists("data/processed/train_processed.csv"), reason="Data files not found")
def test_data_loading():
    tokenizer = MockTokenizer()
    train_path = "data/processed/train_processed.csv"

    dataset = DisasterTweetsDataset(train_path, tokenizer)

    assert len(dataset) > 0, "Dataset should not be empty"

    sample = dataset[0]

    # Check for the keys that actually exist in your data
    assert "input_ids" in sample
    assert "attention_mask" in sample
    assert "label" in sample  # <--- CHANGED from "labels" to "label"

    assert torch.is_tensor(sample["input_ids"])
    assert torch.is_tensor(sample["label"])
