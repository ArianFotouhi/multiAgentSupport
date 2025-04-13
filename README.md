# 🤖 Multi-Agent LLM Pipeline for Customer Support Ticket Handling

This project implements an intelligent, multi-agent system to automate customer support ticket handling using Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG). It classifies, responds, evaluates, and escalates tickets using a coordinated team of AI agents.

---

## 🚦 How It Works

This system simulates a real customer support flow, handled end-to-end by multiple LLM agents:

1. **🧠 Classifier Agent**
   - Categorizes incoming support tickets (e.g., `legal`, `billing`, `security`) and assigns priority (`high`, `medium`, `low`).

2. **📚 Responder Agent (with RAG)**
   - Uses semantic search (via Pinecone) to retrieve relevant internal policies and crafts a context-aware, professional response.

3. **🧪 Evaluator Agent**
   - Evaluates the response's quality, clarity, and coverage before approval.

4. **🚨 Escalator Agent**
   - Escalates tickets requiring human attention (e.g., sensitive categories or failed evaluation) with a summarized internal note.

---

🚀 Running the Pipeline
Run with example tickets:

```bash
PINECONE_API_KEY=xxx 
AZURE_SUBSCRIPTION_KEY=xxx \
AZURE_OPENAI_ENDPOINT=xxx \
AZURE_API_VERSION=xxx \
AZURE_DEPLOYMENT_NAME=xxx \
python3 multiAgent.py
```


You’ll see classification, generated response, evaluation, and escalation (if needed) for each ticket.

🧠 Example Agents in Action
Input Ticket:

"Why did I get charged an extra 5% fee?"

Classifier Output:

```
{
  "category": "billing",
  "priority": "medium"
}
```
Responder Output:
```
"Thank you for reaching out. The additional 5% charge is due to..."
```
Evaluator Output:

```
{
  "approve": true,
  "reason": "Response is accurate and clearly explains the charge."
}
```
🧩 Customization
🔍 Add more categories in AUTO_ESCALATE_CATEGORIES

🧠 Tweak prompts in each agent for tone, verbosity, etc.

📚 Change vector store namespace or connect to another backend (like FAISS or Qdrant)

📦 Tech Stack
OpenAI / Azure OpenAI

Pinecone Vector Store

Python re, json, and LLM-powered prompts

🙌 Acknowledgments
This project draws inspiration from emerging multi-agent orchestration patterns and LLM applications in enterprise support.

📄 License
MIT License — see LICENSE file for details.

vbnet
Copy
Edit

Let me know if you'd like a version with a badge section, architecture diagram, or deployment g