import numpy as np
import torch

from torch import nn
from torch.utils.data import DataLoader
from transformers import BertTokenizer, BertModel
from few_shot_priming.few_shot_stance import *

class Dataset(torch.utils.data.Dataset):
    def __init__(self,df, labels, path=None):
        if path:
            tokenizer = BertTokenizer.from_pretrained(path)
        else:
            tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
        self.labels = [labels[label] for label in df["claims.stance"]]
        self.texts = []
        for i, record in df.iterrows():
            self.texts.append(tokenizer(record['claims.claimCorrectedText'], record["topicText"], max_length=512,
                                        truncation=True, return_tensors="pt"))

    def classes(self):
        return self.labels

    def __len__(self):
        return len(self.labels)

    def get_batch_labels(self, idx):
        return np.array(self.labels[idx])

    def get_batch_texts(self, idx):
        return self.texts[idx]
    def __getitem__(self, idx):
        batch_texts = self.get_batch_texts(idx)
        batch_y = self.get_batch_labels(idx)
        return batch_texts, batch_y

class BertClassifier(nn.Module):
    def __init__(self, hyperparameters, path=None):
        super(BertClassifier, self).__init__()
        self.lr = hyperparameters["learning-rate"]
        self.head_size = hyperparameters["head-size"]
        self.batch_size = hyperparameters["batch-size"]
        self.linear = nn.Linear(768, self.head_size)
        self.classifier_head = nn.Linear(self.head_size, 1)
        if path:
            self.bert = BertModel.from_pretrained(path)
        else:
            self.bert = BertModel.from_pretrained('bert-base-cased')
        self.labels = {"CON": 0, "PRO":1}


    def forward(self, input_ids, mask):
        _, pooled_output = self.bert(input_ids=input_ids, attention_mask=mask, return_dict=False)
        linear_output = self.linear(pooled_output)
        head_output = self.classifier_head(linear_output)
        return head_output


def get_baseline_params():
    config = load_config()
    print(config)
    return config["baseline-params"]


def parse_args():
    """
    Parse the arguments of the scripts
    :return:
    """
    parser = ArgumentParser()
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--offline", action="store_true")
    return parser.parse_args()

def run_experiment_baseline(splits, offline=True, validate=False, params=None):
    use_cuda = torch.cuda.is_available()
    if offline:
        save_pre_trained_model()
        path = params["model-path"]

    if not params:
        params = get_baseline_params()

    train_dataset = Dataset(splits["training"], {"PRO": 1, "CON": 0}, path=path)
    if validate:
        experiment_type = "validate"
        test_dataset = Dataset(splits["validation"], {"PRO": 1, "CON": 0}, path=path)
    else:
        experiment_type = "test"
        test_dataset = Dataset(splits["test"], {"PRO": 1, "CON": 0}, path=path)

    train_dataloader = DataLoader(train_dataset, batch_size=params["batch-size"], shuffle=True)
    test_dataloader = DataLoader(test_dataset, batch_size=params["batch-size"], shuffle=True)

    device = torch.device("cuda" if use_cuda else "cpu")

    optimizer = AdamW(params, lr=params["learning-rate"])
    bert = BertClassifier(params, path=path)
    epochs = params["epochs"]
    criterion = nn.BCEWithLogitsLoss().cuda()

    train_loss = 0
    test_loss = 0
    sigmoid = nn.Sigmoid()
    bert.train()
    metrics = {}
    for epoch in range(epochs):
        for step, (train_input, train_label) in enumerate(train_dataloader):
            train_label = train_label.to(device)
            mask = train_input["attention_mask"].to(device)
            input_ids = train_input["input_ids"].sequeeze(1).to(device)
            output = bert(input_ids, mask)
            batch_loss = criterion(output, train_label.float())
            train_loss += batch_loss.item()
            batch_loss.backward()
            optimizer.step()
            metrics["train/loss"] = train_loss / (step +1)
            wandb.log(metrics)
            bert.eval()
            all_test_labels = []
            all_test_preds = []
            for step, (test_input, test_labels) in enumerate(test_dataloader):
                test_labels = test_labels.to(device)
                mask = test_labels.to(device)
                input_ids = test_input["input_ids"].sequeeze(1).to(device)
                output = bert(input_ids, mask)
                predictions = sigmoid(output)
                predictions = [score > 0.5 for score in predictions]
                all_test_preds.extend(predictions)
                all_test_labels.extend(test_labels)
                batch_loss = criterion(output, test_labels.float())
                test_loss += batch_loss.item()
                metrics[f"{experiment_type}/loss"] = test_loss / (step+1)
                wandb.log(metrics)
            test_accuracy = accuracy_score(all_test_labels, all_test_preds)
            metrics[f"{experiment_type}/accuracy"] = test_accuracy
            wandb.log(metrics)


if __name__ == "__main__":
    args = parse_args()
    splits = load_splits()
    params = get_baseline_params()
    init_wandb(args.offline, params)
    run_experiment_baseline(splits, args.offline, args.validate)
