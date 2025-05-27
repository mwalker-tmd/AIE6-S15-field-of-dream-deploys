---
title: TMD Open Source RAG
emoji: 🧠
colorFrom: yellow
colorTo: green
sdk: docker
sdk_version: '1.0'
app_file: app.py
pinned: false
license: mit
short_description: TMD Open Source RAG implementation
---

# TMD Open Source RAG

A Retrieval-Augmented Generation (RAG) app using open-source models, FastAPI, and Vite/React.# 🌽 Field of Dream Deploys

### **_“If you deploy it, they can use it.”_**  
Welcome to `field-of-dream-deploys`, a full-stack Retrieval-Augmented Generation (RAG) application powered by open-source models deployed via Hugging Face Inference Endpoints.

This project showcases how to:
- Load and embed real-world documents (like essays and engineering philosophies)
- Persist them in a vector database
- Ask questions through a conversational React frontend
- Route responses through your own LLM and embedding endpoints — no OpenAI required

Inspired by *Field of Dreams*, this app turns deployed endpoints into usable interfaces for real-time insight and discovery.

Built with:
- **LangChain**
- **FastAPI**
- **React**
- **Qdrant**
- **Hugging Face Inference Endpoints**

Step onto the field. Deploy the dream. Let the questions come.

## Backend Template ([/backend](./backend))

This backend provides a reusable scaffold for building LLM-powered applications with FastAPI.

### Features
- Modular routing with `/api`
- Prompt manager and role-based prompt composition
- Plug-and-play vector DB with FAISS
- Easily swappable embedding model