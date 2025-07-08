import os
import json
import base64
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

load_dotenv()

# Load store layout
LAYOUT_PATH = Path(__file__).parent.parent / "data" / "store_layout.json"
layout = json.loads(LAYOUT_PATH.read_text())["layout"]

# Gemini Vision LLM setup
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
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


def image_to_product_location(image_path: str):
    with open(image_path, "rb") as img_file:
        content = img_file.read()

    encoded_image = base64.b64encode(content).decode()
    catalog = flatten_catalog(layout)

    vision_prompt = HumanMessage(
        content=[
            {
                "type": "text",
                "text": f"""
You are a friendly in-store Walmart AI assistant.

A customer has uploaded a photo of a product. Below is the catalog of all available products in the store:
{catalog}

Your job:
1. Identify the closest matching product from the image.
2. Respond in a friendly, helpful tone.
3. Include the product name, department, aisle, shelf, and price in your response.
4. If no match found, say something like: "Sorry! I couldn't find that in our store today."

Example:
"That looks like 'chips'! You’ll find them in Snacks → Aisle 4, Shelf S1 for just ₹1.6."
"""
            },
            {"type": "image_url", "image_url": {
                "url": f"data:image/jpeg;base64,{encoded_image}"}
             }
        ]
    )

    try:
        vision_response = llm.invoke([vision_prompt])
        message = vision_response.content.strip()

        return {
            "found": not message.lower().startswith("sorry"),
            "message": message
        }

    except Exception as e:
        return {
            "found": False,
            "message": f"Something went wrong while processing the image: {str(e)}"
        }
