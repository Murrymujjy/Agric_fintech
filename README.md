# Agric_fintech
Project Title: Farm Ledger – AI-Powered Credit Inclusion
Tagline: Bridging the gap between rural farmers and formal lending through Hybrid AI.

Overview
Farm Ledger is a comprehensive platform designed to evaluate the creditworthiness of farmers in Nigeria. Unlike traditional scoring systems that are "black boxes," Farm Ledger uses Logistic Regression and Decision Trees for precise risk assessment, paired with Featherless.ai (LLMs) to provide transparent, natural-language explanations for every decision.
Farm Ledger Africa is a specialized FinTech platform designed to bridge the $330$ billion financing gap for smallholder farmers across the continent. 
By leveraging Hybrid AI, we provide a credit scoring tool that speaks 10 African languages, converting natural speech and text into structured financial data for immediate loan eligibility assessment.

The Problem
Many farmers in rural sectors lack formal credit history, leading to high "risk" labels and loan denials without explanation.


✨ Key Features
🌍 Pan-African Linguistic Support: Full UI and AI integration for 10 languages, including English, Luganda, Yoruba, Hausa, Igbo, Swahili, Zulu, Amharic, Wolof, and Afrikaans.
🎙️ Voice-Activated Profiling: A resilient voice-to-text pipeline that allows farmers to apply for credit using their native tongue.
🤖 Context-Aware AI Chatbot: An LLM-powered assistant that synchronizes with the user's Farmer Profile to explain credit decisions in plain, localized language.
📊 Lender Dashboard: A centralized hub for financial institutions to process bulk applications and analyze regional credit trends.
🍏 Green-Agri Branding: A professional, Forest Green interface designed to build trust and reflect the growth of the agricultural sector.
🛠️ Technical StackFrontend: Streamlit (Python) with custom CSS and interactive navigation.

Predictive Model: Scikit-Learn (Logistic Regression)—a deterministic engine for fair and mathematically sound credit scoring.
Reasoning Engine: Meta-Llama 3.1-8B (hosted via Featherless.ai) for zero-shot intent extraction and multi-lingual generative explanations.
Transcription: Google Speech API for cost-effective, multi-lingual audio processing.
State Management: Streamlit Session State for real-time synchronization between the profiling form and the chatbot.

📂 File Structure
appp.py: The main multi-lingual controller and interactive dashboard.
HomeChatbotPage.py: The context-aware AI assistant.
voice_assistant.py: The multi-modal voice processing module.
farm_profile.py: The data entry and initial scoring engine.
models_logistic_regression_model.pkl: The trained ML predictive core.
