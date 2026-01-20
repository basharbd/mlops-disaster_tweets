import pytest
import torch
import pandas as pd
from transformers import AutoTokenizer
from disaster_tweets.data import DisasterTweetsDataset

# 1. Create a dummy CSV file
@pytest.fixture
def mock_csv(tmp_path):
    data = {
        "text": ["Disaster happened", "Just chilling", "Fire everywhere", "Sunny day", "Help me"],
        "target": [1, 0, 1, 0, 1]
    }
    df = pd.DataFrame(data)
    file_path = tmp_path / "dummy_train.csv"
    df.to_csv(file_path, index=False)
    return str(file_path)

# 2. Load the Tokenizer (New!)
@pytest.fixture(scope="module")
def tokenizer():
    return AutoTokenizer.from_pretrained("google/bert_uncased_L-2_H-128_A-2")

# 3. Update Tests to use the Tokenizer
def test_dataset_loading(mock_csv, tokenizer):
    """Test that the dataset loads correctly from a CSV file."""
    # PASS THE TOKENIZER HERE 👇
    dataset = DisasterTweetsDataset(mock_csv, tokenizer)

    assert len(dataset) == 5, "Dataset length should match the number of rows in the CSV"

def test_dataset_item_structure(mock_csv, tokenizer):
    """Test that the dataset returns the correct keys and shapes."""
    dataset = DisasterTweetsDataset(mock_csv, tokenizer)
    sample = dataset[0]

    # UPDATED: Match exactly what your dataset returns
    expected_keys = {"text", "input_ids", "attention_mask", "label"}

    # Verify keys exist (using set comparison to ignore order)
    assert set(sample.keys()) == expected_keys, f"Key mismatch! Found: {sample.keys()}"

    # Check tensor shapes
    assert sample["input_ids"].shape == (128,), f"Expected (128,), got {sample['input_ids'].shape}"
    assert sample["attention_mask"].shape == (128,)

    # UPDATED: Key is 'label' (singular), not 'labels'
    assert isinstance(sample["label"], torch.Tensor)
    assert sample["label"].ndim == 0

def test_dataset_tokenization(mock_csv, tokenizer):
    """Test that tokenization is actually working."""
    dataset = DisasterTweetsDataset(mock_csv, tokenizer)
    sample = dataset[0] # "Disaster happened"

    # 101 is the [CLS] token that starts every BERT sentence
    assert sample["input_ids"][0] == 101, "Tokenization should start with [CLS] token id 101"
