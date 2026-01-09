import torch
import pytorch_lightning as pl
from transformers import DistilBertModel

class DisasterTweetModel(pl.LightningModule):
    def __init__(self, lr=1e-4):
        super().__init__()
        self.save_hyperparameters()
        
        # 1. Load the pre-trained DistilBERT
        self.bert = DistilBertModel.from_pretrained('distilbert-base-uncased')
        
        # 2. Add a simple classifier layer on top (768 -> 2 classes)
        # Class 0: Not Disaster, Class 1: Disaster
        self.classifier = torch.nn.Linear(768, 2)
        
        self.loss_fn = torch.nn.CrossEntropyLoss()

    def forward(self, input_ids, attention_mask):
        # Pass input through BERT
        output = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        
        # Get the state of the [CLS] token (the first token) representing the whole sentence
        cls_token_state = output.last_hidden_state[:, 0, :]
        
        # Pass through classifier
        return self.classifier(cls_token_state)

    def training_step(self, batch, batch_idx):
        input_ids = batch['input_ids']
        attention_mask = batch['attention_mask']
        labels = batch['label']
        
        logits = self(input_ids, attention_mask)
        loss = self.loss_fn(logits, labels)
        
        # Log training loss
        self.log('train_loss', loss)
        return loss
    
    def validation_step(self, batch, batch_idx):
        input_ids = batch['input_ids']
        attention_mask = batch['attention_mask']
        labels = batch['label']
        
        logits = self(input_ids, attention_mask)
        loss = self.loss_fn(logits, labels)
        
        # Calculate accuracy
        preds = torch.argmax(logits, dim=1)
        acc = (preds == labels).float().mean()
        
        self.log('val_loss', loss)
        self.log('val_acc', acc)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.hparams.lr)