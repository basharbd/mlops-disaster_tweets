import sys
from pathlib import Path

# 1. Path Injection (The Fix)
# This finds the 'src' folder relative to this test file
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import pytest
import torch
from disaster_tweets.model import DisasterTweetModel

# 2. Fixture to initialize the model once for these tests
@pytest.fixture(scope="module")
def model():
    return DisasterTweetModel()

def test_model_initialization(model):
    """Check that the model initializes with the correct architecture."""
    assert hasattr(model, "bert"), "Model should have a 'bert' attribute"
    assert hasattr(model, "classifier"), "Model should have a 'classifier' attribute"

def test_forward_pass_shape(model):
    """Check that the forward pass returns the correct shape (batch_size, 2)."""
    batch_size = 4
    seq_length = 128

    input_ids = torch.randint(0, 1000, (batch_size, seq_length))
    attention_mask = torch.ones((batch_size, seq_length))

    logits = model(input_ids, attention_mask)

    # Check output shape: Should be [4, 2]
    assert logits.shape == (batch_size, 2), f"Expected shape ({batch_size}, 2), got {logits.shape}"

def test_prediction_output_range(model):
    """Check that model runs and outputs raw logits (not probabilities)."""
    input_ids = torch.randint(0, 1000, (1, 128))
    attention_mask = torch.ones((1, 128))

    logits = model(input_ids, attention_mask)

    assert isinstance(logits, torch.Tensor)
    assert logits.ndim == 2
