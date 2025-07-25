# backend/handler.py

from intent_model import extract_intent
from web_automation import (
    play_video_on_youtube,
    order_product,
    order_food_on_platform,
    search_google  # Optional if you implement SearchTopic intent
)


def handle_command(command):
    intent, entities = extract_intent(command)
    print("Intent:", intent)
    print("Entities:", entities)

    if not intent or not entities:
        
        return "Intent not recognized."

    platform = (entities.get("platform") or "").lower()

    if intent == "PlayVideo" and platform == "youtube":
        product = entities.get("product")
        return play_video_on_youtube(product)

    elif intent == "OrderProduct" and platform in ["amazon", "flipkart"]:
        product = entities.get("product")
        return order_product(product, platform)

    elif intent == "OrderFood":
        return order_food_on_platform(
            food_item=entities.get("food_item", ""),
            restaurant=entities.get("restaurant", ""),
            location=entities.get("location", ""),
            platform=platform
        )

    elif intent == "SearchTopic":
        product = entities.get("product")
        if product:
            return search_google(product)
        else:
            
            return "No search term provided."
        
    elif intent == "GeneralTopic":
        print(f"Searching Google for {command}")
        return search_google(command)


    else:
        print("This platform or action is not supported.")
        return "Unsupported intent or platform."
