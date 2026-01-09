# Disaster Tweet Classification

## Overall Goal
The primary objective of this project is to develop a robust, production-ready MLOps pipeline for Natural Language Processing (NLP). We aim to build a system that classifies Twitter messages to determine if they refer to real-world disasters. Our focus is on reproducibility (Docker), automation (CI/CD), and scalability (PyTorch Lightning).

## Data
We utilize the Kaggle 'Natural Language Processing with Disaster Tweets' dataset:
- **Input:** Tweets containing text, keywords, and location.
- **Target:** Binary classification (1 = Real Disaster, 0 = Not Disaster).
- **Challenges:** Noisy data requiring significant cleaning.

## Models
We will use Transfer Learning with **DistilBERT**:
- **Architecture:** DistilBERT (via Hugging Face) wrapped in PyTorch Lightning.
- **Why:** Balances performance and inference speed.
- **Experiments:** We will track performance using Weights & Biases.

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
