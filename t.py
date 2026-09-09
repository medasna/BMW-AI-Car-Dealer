import os
import json
from huggingface_hub import InferenceClient

MODEL = "Qwen/Qwen3-32B"

client = InferenceClient(
    api_key=os.getenv("HF_TOKEN")
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "find_cars",
            "description": "Find BMW cars matching the customer's requirements.",
            "parameters": {
                "type": "object",
                "properties": {
                    "max_price": {
                        "type": "number",
                        "description": "Maximum price in euros"
                    },
                    "fuel": {
                        "type": "string",
                        "enum": ["Petrol", "Diesel"]
                    },
                    "transmission": {
                        "type": "string",
                        "enum": ["Manual", "Auto"]
                    },
                    "body_type": {
                        "type": "string",
                        "enum": [
                            "SUV",
                            "Sedan",
                            "Coupe",
                            "Hatchback",
                            "Wagon",
                            "Convertible"
                        ]
                    }
                }
            }
        }
    }
]

messages = [
    {
        "role": "system",
        "content": "You are a BMW dealership assistant. Use the find_cars tool when the customer asks for cars. Keep your final response short and do not reveal your reasoning."
    },
    {
        "role": "user",
        "content": "Show me SUVs under €50,000."
    }
]

print("Testing model:", MODEL)
print()

try:
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools
    )

    message = response.choices[0].message

    print("Model response:")
    print(message.content)

    print("\nTool calls:")

    if message.tool_calls:
        for tool_call in message.tool_calls:
            print("Function:", tool_call.function.name)
            print("Arguments:", tool_call.function.arguments)

            # Verify arguments are valid JSON
            arguments = tool_call.function.arguments

            if isinstance(arguments, str):
                arguments = json.loads(arguments)

            print("Parsed:", arguments)

        print("\n✅ TOOL CALLING WORKS")
    else:
        print("❌ No tool call was generated.")

except Exception as e:
    print("\n❌ ERROR:")
    print(type(e).__name__, e)