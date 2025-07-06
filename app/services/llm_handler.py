import json
from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv
load_dotenv()

# Find the store_layout file
STORE_LAYOUT_PATH = Path(__file__).parent.parent / "data" / "store_layout.json"
store_layout = json.loads(STORE_LAYOUT_PATH.read_text())["layout"]
# Initialize model correctly
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-lite",
    temperature=0.7,
    google_api_key=os.getenv("GEMINI_API_KEY")
)


def locate_product(query: str) -> dict:
    # Flatten store layout
    all_items = []
    for dept, aisles in store_layout.items():
        for aisle, products in aisles.items():
            for item in products:
                line = f"{item['name']} is in {aisle}, Shelf {item['shelf']} under {dept}."
                all_items.append(line)

    layout_context = "\n".join(all_items)

    prompt = f"""
You are a helpful assistant inside a Walmart store.
Here is the store layout (include aisle, shelf, and department):

{layout_context}

Now, based on the customer's question:
"{query}"

Return a **friendly and specific response** like:
- “Sure! You’ll find milk in Aisle 3, Shelf D1 under the Dairy section.”
- OR if not found: “Sorry, I couldn't find that item in our store layout.”

Be concise and avoid repeating the query. Give a clear answer.
"""

    response = llm.invoke([HumanMessage(content=prompt)])
    return {"response": response.content}
