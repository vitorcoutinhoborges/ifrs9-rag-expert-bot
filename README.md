# ifrs9-rag-expert-bot
RAG para consultas às normas da IFRS9
# ⚖️ IFRS 9 Specialist - RAG Bot

Este projeto utiliza **IA Generativa** e **Busca Semântica** para responder dúvidas técnicas sobre a norma contábil IFRS 9.

### 🚀 Tecnologias Utilizadas
* **Databricks**: Ingestão e processamento do PDF oficial da norma.
* **LangChain**: Orquestração do pipeline de RAG (Retrieval-Augmented Generation).
* **FAISS**: Banco de dados vetorial para busca semântica ultra-rápida.
* **HuggingFace**: Embeddings locais (`all-MiniLM-L6-v2`) para maior resiliência.
* **Google Gemini 1.5 Flash**: LLM para geração de respostas técnicas fundamentadas.
* **Streamlit**: Interface de usuário intuitiva.

### 🏗️ Arquitetura
O sistema processa a norma em chunks, gera vetores de significado e os armazena localmente. Ao receber uma pergunta, o bot identifica os trechos mais relevantes e utiliza o Gemini para sintetizar uma resposta precisa, evitando alucinações.

---
*Desenvolvido como projeto de portfólio para demonstração de habilidades em Engenharia de Dados e GenAI.*
