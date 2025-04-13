# Multi-Agent LLM Pipeline for Customer Support Ticket Handling

import json
import re
import os
from openai import AzureOpenAI
# from config import endpoint, deployment, subscription_key, api_version
from vector_store.vector_store import PineconeVectorStore
# Constants
AUTO_ESCALATE_CATEGORIES = {"legal", "data privacy", "security"}

# Azure OpenAI client from ENV
client = AzureOpenAI(
    api_version=os.getenv("AZURE_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_SUBSCRIPTION_KEY"),
)

DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME")


def call_llm(system_prompt, user_prompt, temperature=0):
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=4096,
        model=DEPLOYMENT_NAME,
        temperature=temperature
    )
    return response.choices[0].message.content.strip()


# --- AGENTS ---

def extract_json(text):
    """Extract and parse JSON from model output."""
    try:
        json_str = re.search(r'\{.*\}', text, re.DOTALL).group()
        return json.loads(json_str)
    except (json.JSONDecodeError, AttributeError) as e:
        print(f"❌ Failed to parse JSON: {e}")
        print(f"🪵 Raw LLM output:\n{text}")
        raise






def classifier_agent(ticket_text):
    system_prompt = "You are a support ticket classifier. Output JSON with category and priority."
    user_prompt = (
        f"Classify this ticket:\n\"{ticket_text}\"\n"
        f"Return valid JSON like: {{\"category\": \"legal | data privacy | security | billing \", \"priority\": \"high\"|\"medium\"|\"low\"}}"
    )
    result = call_llm(system_prompt, user_prompt)
    print(f"🔍 Classification Raw Result:\n{result}\n")
    return extract_json(result)

################ADD RAG FOR RESPONDER AGENT TO RESOND BASED ON DOC##############################
def responder_agent(ticket_text, category):
    # Initialize vector store (no upsert needed here)
    store = PineconeVectorStore(namespace="policy-knowledge")

    # Use ticket content for richer query context
    query = f"{category} policy: {ticket_text}" if category else ticket_text
    results = store.search(query=query, top_k=3)

    # Build context from retrieved policies
    relevant_documents = "\n".join([doc[0] for doc in results]) or "No relevant policies found."

    # Prepare prompts for LLM
    system_prompt = (
        f"You are a customer support assistant specialized in '{category}' tickets. "
        f"Use the following policy context to help answer the question:\n{relevant_documents}"
    )
    user_prompt = f"Write a helpful and professional reply to this ticket:\n\"{ticket_text}\""

    return call_llm(system_prompt, user_prompt)



def evaluator_agent(ticket_text, response):
    system_prompt = (
        "You are a QA evaluator for support responses. Determine if this response is good to send directly to a customer. "
        "Return valid JSON like: {\"approve\": true|false, \"reason\": \"...\"}"
    )
    user_prompt = (
        f"Customer message:\n\"{ticket_text}\"\n\n"
        f"Proposed response:\n\"{response}\"\n\n"
        "Evaluate clarity, accuracy, and coverage of the issue."
    )
    return extract_json(call_llm(system_prompt, user_prompt))


def escalator_agent(ticket_text, reason):
    system_prompt = "You are an internal assistant writing escalation notes."
    user_prompt = (
        f"Escalate this ticket:\n\"{ticket_text}\"\n\n"
        f"Reason: {reason}\n\n"
        "Write a concise, clear summary for a human support agent."
    )
    return call_llm(system_prompt, user_prompt)


# --- PIPELINE ---

def handle_ticket(ticket_text):
    print(f"\n📝 Ticket: {ticket_text}\n")

    classification = classifier_agent(ticket_text)
    category = classification.get("category", "unknown")
    priority = classification.get("priority", "normal")
    print(f"📌 Category: {category.upper()} | Priority: {priority.upper()}\n")

    response = responder_agent(ticket_text, category)
    print(f"🧾 Proposed Response:\n{response}\n")

    if category in AUTO_ESCALATE_CATEGORIES or category == "unknown":
        reason = f"Category '{category}' requires manual review."
        escalation = escalator_agent(ticket_text, reason)
        print(f"⚠️ Escalated:\n{escalation}\n")
        return

    eval_result = evaluator_agent(ticket_text, response)
    if not eval_result.get("approve", False):
        reason = eval_result.get("reason", "Response rejected by evaluator.")
        escalation = escalator_agent(ticket_text, reason)
        print(f"⚠️ Escalated:\n{escalation}\n")
    else:
        print(f"✅ Final Response Approved:\n{response}\n")


# --- TESTING EXAMPLES ---

if __name__ == "__main__":
    tickets = [
    "Can I get a refund if I change my mind?",
    "Why did I get charged an extra 5% fee?",
    "Will my subscription renew automatically?",
    "What are your password rules?",

            ]

    for t in tickets:
        handle_ticket(t)
        print("=" * 70)
