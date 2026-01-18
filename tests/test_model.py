import torch

from disaster_tweets.models import DisasterTweetModel


def test_model_output_shape():
    # 1. Setup: Create the model
    model = DisasterTweetModel()

    # Define a fake batch size
    batch_size = 4
    seq_length = 20

    # Create random inputs (simulating token IDs)
    # We need input_ids and attention_mask as expected by BERT
    input_ids = torch.randint(0, 1000, (batch_size, seq_length))
    attention_mask = torch.ones((batch_size, seq_length))

    # 2. Action: Forward pass
    # Using the model like a function calls its forward() method
    output = model(input_ids, attention_mask)

    # 3. Assertion: Check output shape
    # We expect [batch_size, 2] because we have 2 classes (Disaster vs Not Disaster)
    assert output.shape == (batch_size, 2), (
        f"Expected output shape {(batch_size, 2)}, but got {output.shape}"
    )
