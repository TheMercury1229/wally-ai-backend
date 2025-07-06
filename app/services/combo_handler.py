import json
from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv
load_dotenv()

STORE_PATH = Path(__file__).parent.parent / "data" / "store_layout.json"
layout = json.loads(STORE_PATH.read_text())["layout"]

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-lite",
    temperature=0.7,
    google_api_key=os.getenv("GEMINI_API_KEY")
)


def extract_available_products():
    products = []
    for dept, aisles in layout.items():
        for aisle, items in aisles.items():
            for item in items:
                products.append({
                    "name": item["name"],
                    "price": item["price"],
                    "aisle": aisle,
                    "dept": dept
                })
    return products


def suggest_combos(purpose: str) -> list[str]:
    all_products = extract_available_products()

    catalog = "\n".join([
        f"{p['name']} (₹{p['price']}) in {p['dept']}, {p['aisle']}"
        for p in all_products
    ])

    prompt = f"""
You are a Walmart in-store assistant AI.

The customer is shopping for: "{purpose}".

You have access to this product list:
{catalog}

Suggest 3–5 best items for their purpose.

For each item, give:
- Product Name
- Price
- Department
- Aisle

Return a clear, clean bullet list like:
• Milk – ₹1.5 – Dairy, Aisle 3

If no relevant items, say: \"Sorry, I couldn’t find anything good for that purpose right now.\"
"""

    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip().split("\n")
