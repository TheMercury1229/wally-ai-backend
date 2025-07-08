import os
import json
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

load_dotenv()
LAYOUT_PATH = Path(__file__).parent.parent / "data" / "store_layout.json"
layout = json.loads(LAYOUT_PATH.read_text())["layout"]


llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-lite",
    temperature=0.8,
    google_api_key=os.getenv("GEMINI_API_KEY")
)


def flatten_catalog(layout_dict: dict) -> str:
    """Flattens the layout into a string the LLM can use to reason properly."""
    catalog_lines = []
    for dept, aisles in layout_dict.items():
        for aisle, items in aisles.items():
            for item in items:
                catalog_lines.append(
                    f"Product: {item['name']}, Price: ₹{item['price']}, "
                    f"Stock: {'Yes' if item['stock'] else 'No'}, "
                    f"Dept: {dept}, Aisle: {aisle}, Shelf: {item['shelf']}"
                )
    return "\n".join(catalog_lines)


def generate_surprise_product(user_id: str, history: list[dict]) -> dict:
    history_text = "\n".join([
        f"- {item['product_name']} ({item['category']}, ₹{item['price']}) on {item['timestamp']}"
        for item in history
    ])
    catalog = flatten_catalog(layout)

    prompt = f"""
You are an AI assistant at Walmart. A user with ID {user_id} has this shopping history:
{history_text}

Suggest one fun, unexpected, but relevant product they might like today from the catalog.
{catalog}
Respond in this format:
Suggestion: product name (e.g., "Protein Bar")
Message: <funny/witty/helpful message (1 line)>
"""

    response = llm.invoke([HumanMessage(content=prompt)])

    suggestion, message = "", ""
    for line in response.content.strip().split("\n"):
        if line.lower().startswith("suggestion:"):
            suggestion = line.split(":", 1)[1].strip()
        elif line.lower().startswith("message:"):
            message = line.split(":", 1)[1].strip()

    return {
        "suggestion": suggestion,
        "message": message
    }
