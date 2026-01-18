from pytorch_lightning import Trainer
from torch.utils.data import DataLoader
from transformers import DistilBertTokenizer

from disaster_tweets.data import DisasterTweetsDataset
from disaster_tweets.models import DisasterTweetModel


def train():
    print("Preparing data...")
    tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

    # Load the processed CSVs we created earlier
    train_dataset = DisasterTweetsDataset(
        "data/processed/train_processed.csv", tokenizer
    )
    val_dataset = DisasterTweetsDataset("data/processed/val_processed.csv", tokenizer)

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=32, num_workers=0)

    print("Initializing model...")
    model = DisasterTweetModel(lr=1e-4)

    print("Starting training...")
    # Train for just 1 epoch to test if it works
    trainer = Trainer(max_epochs=1, limit_train_batches=0.1)
    trainer.fit(model, train_loader, val_loader)


if __name__ == "__main__":
    train()
