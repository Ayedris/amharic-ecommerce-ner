# Amharic E-commerce Data Extractor for FinTech Insights

This project is part of the 10Academy Week 4 AI Mastery Challenge (June 18–24, 2025). The goal is to develop a system for extracting structured insights from Telegram-based e-commerce channels in Amharic, enabling EthioMart to centralize listings and evaluate vendors for micro-lending opportunities.

## Project Objectives

- Scrape and preprocess Amharic messages from Telegram e-commerce channels.
- Label data using CoNLL format for NER.
- Fine-tune transformer-based NER models (XLM-R, Amharic-BERT, etc.).
- Compare models using metrics like F1-score and interpretability tools (SHAP, LIME).
- Score vendors using extracted data and Telegram metadata for loan eligibility.

### Project Structure

```
amharic-ecommerce-ner/
│
├── data/
│   ├── raw/
│   └── labeled/
│
├── notebooks/
│   ├── data_ingestion.ipynb
│   ├── labeling_sample.ipynb
│   ├── ner_training.ipynb
│   └── model_comparison.ipynb
│
├── scripts/
│   ├── telegram_scraper.py
│   ├── preprocess.py
│   ├── label_converter.py
│   ├── train_ner.py
│   ├── interpretability.py
│   └── vendor_scorecard.py
│
├── models/
│
├── outputs/
│   ├── interim_summary.pdf
│   └── final_report.pdf
│
├── README.md
├── .gitignore
├── requirements.txt
├── dvc.yaml
└── LICENSE
```
