# Disaster Tweet Classification

## Overall Goal of the Project
The primary objective of this project is to develop a robust, production-ready MLOps pipeline for Natural Language Processing (NLP). In the context of emergency response, social media is a critical source of real-time information. However, manually monitoring Twitter for actionable data is impossible due to the high volume of noise. We aim to build a system that automatically classifies Twitter messages to determine if they refer to real-world disasters (e.g., fires, earthquakes, floods) or if they are metaphorical/irrelevant.

Beyond simple accuracy, our focus is on the **Machine Learning Operations (MLOps)** lifecycle. We aim to solve common challenges in deploying NLP models, such as environment inconsistency, lack of reproducibility, and opaque experiment tracking. Our pipeline emphasizes:
1.  **Reproducibility:** A fully containerized environment using **Docker** to ensure the code runs identically on local machines and cloud instances.
2.  **Automation:** Continuous Integration (CI) pipelines via **GitHub Actions** to automatically lint code, run unit tests, and verify model builds on every commit.
3.  **Scalability:** Efficient training loops and hardware acceleration using **PyTorch Lightning**, allowing for easy transition between CPU and GPU resources.
4.  **Experiment Tracking:** Using **Weights & Biases (W&B)** to log hyperparameters, loss curves, and model artifacts, ensuring that every result can be traced back to a specific configuration.

## Data Description
We utilize the **Kaggle "Natural Language Processing with Disaster Tweets"** dataset, which consists of approximately 10,000 hand-labeled tweets.
-   **Input Data:** Each sample contains the raw text of the tweet, a  (e.g., "ablaze", "accident"), and a  (though this field is often blank or noisy).
-   **Target Variable:** A binary label where `1` indicates a real disaster and `0` indicates a non-disaster.
-   **Data Challenges:** The dataset is "noisy" and reflects real-world social media text. It contains URL links, HTML tags, emojis, slang, and misspellings. A significant part of our data pipeline (in `src/data`) focuses on cleaning these artifacts and tokenizing the text efficiently for Transformer models.

## Model Architecture & Approach
We intend to leverage **Transfer Learning** rather than training a model from scratch.
-   **Architecture:** We will fine-tune **DistilBERT**, a distilled version of the BERT transformer. This model provides a strong balance, retaining 97% of BERT's performance while being 40% lighter and 60% faster, making it ideal for a potential real-time API.
-   **Training:** The model training is implemented in **PyTorch** and wrapped in **PyTorch Lightning** to handle engineering boilerplate (checkpointing, logging, device management).
-   **Evaluation:** We will use **F1-score** and **Accuracy** as our primary metrics. Since disaster detection often suffers from class imbalance, F1-score will be critical to ensure we are not just predicting the majority class. We will also monitor training loss to detect overfitting early.


---

## Project structure

The directory structure of the project looks like this:

```txt
├── .github/                  # Github actions and dependabot
│   ├── dependabot.yaml
│   └── workflows/
│       └── tests.yaml
├── configs/                  # Configuration files
├── data/                     # Data directory
│   ├── processed
│   └── raw
├── dockerfiles/              # Dockerfiles
│   ├── api.Dockerfile
│   └── train.Dockerfile
├── docs/                     # Documentation
│   ├── mkdocs.yml
│   └── source/
│       └── index.md
├── models/                   # Trained models
├── notebooks/                # Jupyter notebooks
├── reports/                  # Reports
│   └── figures/
├── src/                      # Source code
│   ├── project_name/
│   │   ├── __init__.py
│   │   ├── api.py
│   │   ├── data.py
│   │   ├── evaluate.py
│   │   ├── models.py
│   │   ├── train.py
│   │   └── visualize.py
└── tests/                    # Tests
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_data.py
│   └── test_model.py
├── .gitignore
├── .pre-commit-config.yaml
├── LICENSE
├── pyproject.toml            # Python project file
├── README.md                 # Project README
├── requirements.txt          # Project requirements
├── requirements_dev.txt      # Development requirements
└── tasks.py                  # Project tasks
```

Created using [mlops_template](https://github.com/SkafteNicki/mlops_template),
a [cookiecutter template](https://github.com/cookiecutter/cookiecutter) for getting
started with Machine Learning Operations (MLOps).


## Quickstart

```bash
# 1) clone + enter
git clone https://github.com/basharbd/mlops-disaster_tweets.git
cd mlops-disaster_tweets

# 2) create env (conda) + install
conda create -n mlops-disaster python=3.11 -y
conda activate mlops-disaster
pip install -r requirements.txt
pip install -r requirements_dev.txt

# 3) prepare data + train + test
python -m disaster_tweets.data
python -m disaster_tweets.train
pytest -q

----

# MLOps Disaster Tweets Project

## 🚀 Deployment Status
**Status:** Successfully Deployed on Google Cloud Run ✅
**Live URL:** https://disaster-api-284562251239.us-central1.run.app/docs
**Bucket Storage:** Verified (gs://dt-bucket-bashar-2026/predictions/)

## 🛠️ Project Components
- **Containerization:** Docker & Google Artifact Registry.
- **CI/CD:** Google Cloud Build.
- **Monitoring:** Google Cloud Monitoring (Alerting configured for CPU > 80%).
- **Data Collection:** Predictions are automatically saved to GCS Bucket.
