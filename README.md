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

--------------------

🧪 Example Ticket Walkthroughs

Ticket 1: Refund Inquiry

📝 Ticket: Can I get a refund if I change my mind?

🔍 Classification Raw Result:
```
{"category": "billing", "priority": "medium"}
```
📌 Category: BILLING | Priority: MEDIUM

ℹ️ Using existing Pinecone index 'index-policies'
🔍 Performing search for: 'billing policy: Can I get a refund if I change my mind?'

🧾 Proposed Response:
```
Hello,

Thank you for reaching out regarding your refund inquiry.

According to our refund policy, refunds can be issued if requested within 30 days of the original transaction date. If your purchase falls within this period, we would be happy to assist you with processing your refund.

Could you please confirm the date of your transaction or provide your account details so we can verify your eligibility?

If you have any further questions or concerns, please let me know—I’m here to help.

Best regards,  
[Your Name]  
Billing Support Team
```

Final Response Approved: ✅



Ticket 2: Password Rules
📝 Ticket: What are your password rules?

🔍 Classification Raw Result:
```
{"category": "security", "priority": "medium"}
```
📌 Category: SECURITY | Priority: MEDIUM

ℹ️ Using existing Pinecone index 'index-policies'
🔍 Performing search for: 'security policy: What are your password rules?'

🧾 Proposed Response:
```
Hello,

Thank you for reaching out regarding our password requirements. Our current password policy includes the following guidelines:

- Passwords must be at least 12 characters in length.
- We strongly recommend using a combination of uppercase and lowercase letters, numbers, and special characters to enhance security.
- Additionally, multi-factor authentication (MFA) is required for all admin accounts to further protect sensitive access.
- Please note that all system access is logged and audited regularly to ensure security compliance.

If you have any further questions or need assistance, please let me know.

Best regards,  
[Your Name]  
Customer Support
```
⚠️ Escalated:
```
User is asking about our password requirements. Escalating because inquiries related to security policies require manual review.
```
--------------------
🧩 Customization
🔍 Add more categories in AUTO_ESCALATE_CATEGORIES

🧠 Tweak prompts in each agent for tone, verbosity, etc.

📚 Change vector store namespace or connect to another backend (like FAISS or Qdrant)

Pinecone Vector Store

Python re, json, and LLM-powered prompts

🙌 Acknowledgments
This project draws inspiration from emerging multi-agent orchestration patterns and LLM applications in enterprise support.

📄 License
MIT License — see LICENSE file for details.
