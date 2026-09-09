import os
import json
from huggingface_hub import InferenceClient
from search_cars import search_cars


# ==========================================
# HUGGING FACE CONNECTION
# ==========================================

client = InferenceClient(
    api_key=os.getenv("HF_TOKEN")
)

MODEL = "Qwen/Qwen3-4B-Thinking-2507"


# ==========================================
# CAR SEARCH FUNCTION
# ==========================================

def find_cars(
    max_price=None,
    fuel=None,
    transmission=None,
    body_type=None
):
    cars = search_cars(
        max_price=max_price,
        fuel=fuel,
        transmission=transmission,
        body_type=body_type
    )

    if not cars:
        return "No matching cars were found in our inventory."

    results = []

    for car in cars:
        results.append(
            f"{car['brand']} {car['model']} "
            f"({car['year']}) - €{car['price']} - "
            f"{car['fuel']} - {car['transmission']} - "
            f"{car['body_type']} - {car['horsepower']} HP"
        )

    return "\n".join(results)


# ==========================================
# AI TOOL
# ==========================================

tools = [
    {
        "type": "function",
        "function": {
            "name": "find_cars",
            "description": (
                "Search the BMW dealership inventory for cars "
                "matching the customer's requirements."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "max_price": {
                        "type": "integer",
                        "description": "Maximum budget in euros."
                    },
                    "fuel": {
                        "type": "string",
                        "description": (
                            "Fuel type, such as Petrol, Diesel, "
                            "Hybrid, or Electric."
                        )
                    },
                    "transmission": {
                        "type": "string",
                        "description": (
                            "Transmission type, such as Automatic "
                            "or Manual."
                        )
                    },
                    "body_type": {
                        "type": "string",
                        "description": (
                            "Body type, such as SUV, Sedan, "
                            "Hatchback, Coupe, Wagon, or Convertible."
                        )
                    }
                }
            }
        }
    }
]


# ==========================================
# SYSTEM PROMPT
# ==========================================

messages = [
    {
        "role": "system",
        "content": """
You are a professional BMW dealership customer-support assistant.

LANGUAGE:
- Detect the language of the customer's message.
- Always respond in the same language as the customer.
- French customer → French response.
- English customer → English response.
- If the customer switches language, switch with them.

CONVERSATION:
- Respond directly to what the customer says.
- NEVER repeat, copy, or paraphrase the customer's message.
- NEVER pretend that you are the customer.
- Do not start your response by repeating the customer's request.
- If the customer says "Bonjour", simply greet them naturally.
- If the customer is looking for a car, help them find one.
- Ask for missing information when necessary.

INVENTORY:
- The dealership sells BMW vehicles.
- Never invent cars, prices, specifications, or availability.
- When the customer asks for available cars matching requirements,
  use the find_cars tool.
- Only recommend vehicles returned by the find_cars tool.
- Do not recommend vehicles that were not returned by the tool.

TOOL USAGE:
- Use max_price when the customer gives a maximum budget.
- Use fuel when the customer specifies a fuel type.
- Use transmission when the customer specifies automatic or manual.
- Use body_type when the customer specifies a vehicle type.
- If the customer does not specify a requirement, leave that parameter empty.
- Do not ask for information that is not necessary to perform a useful search.

STYLE:
- Be friendly and professional.
- Keep responses concise and natural.
- Do not explain your internal reasoning.
- Do not mention tools, databases, APIs, or programming to the customer.
"""
    }
]


# ==========================================
# START CHAT
# ==========================================

print("===================================")
print("      BMW Car Dealership Assistant")
print("===================================")
print("Type 'exit' to quit.")
print()


while True:

    # Get customer message
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Assistant: Goodbye!")
        break

    # Add customer message
    messages.append({
        "role": "user",
        "content": user_input
    })


    # ==========================================
    # FIRST AI CALL
    # ==========================================

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools
    )

    assistant_message = response.choices[0].message

    # Add AI response to conversation
    messages.append(assistant_message)


    # ==========================================
    # CHECK IF AI WANTS TO SEARCH CARS
    # ==========================================

    if assistant_message.tool_calls:

        for tool_call in assistant_message.tool_calls:

            if tool_call.function.name == "find_cars":

                arguments = tool_call.function.arguments


                # Hugging Face returns tool arguments as JSON text
                if isinstance(arguments, str):
                   arguments = json.loads(arguments)

                # Execute the actual database search
                result = find_cars(**arguments)

                # Give results back to AI
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": "find_cars",
                    "content": result
                })


        # ==========================================
        # SECOND AI CALL
        # ==========================================

        final_response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools
        )

        final_message = final_response.choices[0].message

        messages.append(final_message)

        print(f"Assistant: {final_message.content}")


    # ==========================================
    # NORMAL RESPONSE
    # ==========================================

    else:

        print(f"Assistant: {assistant_message.content}")
