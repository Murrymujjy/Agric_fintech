# Agric_fintech
Project Title: Farm Ledger – AI-Powered Credit Inclusion
Tagline: Bridging the gap between rural farmers and formal lending through Hybrid AI.

Overview
Farm Ledger is a comprehensive platform designed to evaluate the creditworthiness of farmers in Nigeria. Unlike traditional scoring systems that are "black boxes," Farm Ledger uses Logistic Regression and Decision Trees for precise risk assessment, paired with Featherless.ai (LLMs) to provide transparent, natural-language explanations for every decision.

The Problem
Many farmers in rural sectors lack formal credit history, leading to high "risk" labels and loan denials without explanation.

The Solution: Our Hybrid AI Stack
Predictive Layer: Uses Scikit-learn models (Logistic Regression/Decision Trees) to process features like education level, sector (urban/rural), and community tenure.

Generative Layer: Integrates Featherless.ai via an OpenAI-compatible API to translate model outputs (like confidence scores) into actionable financial advice for the farmer.

Production-Ready UI: A multi-page Streamlit dashboard featuring batch processing for lenders and an interactive chatbot for farmers.
