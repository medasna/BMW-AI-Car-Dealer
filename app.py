import os
import json
import streamlit as st
import sqlite3
import pandas as pd
from huggingface_hub import InferenceClient
from search_cars import search_cars


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="BMW Assistant",
    page_icon="🚗",
    layout="centered"
)


# ============================================================
# HUGGING FACE
# ============================================================

try:
    HF_TOKEN = st.secrets["HF_TOKEN"]
except (FileNotFoundError, KeyError):
    HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    st.error("Hugging Face API token is not configured.")
    st.stop()

client = InferenceClient(api_key=HF_TOKEN)

MODEL = "Qwen/Qwen3-32B"

# ============================================================
# MANAGER SETTINGS
# ============================================================

MANAGER_CODE = "5229"

manager_page = "manager" in st.query_params

if "manager_authenticated" not in st.session_state:
    st.session_state.manager_authenticated = False


# ============================================================
# MANAGER LOGIN
# ============================================================

if manager_page and not st.session_state.manager_authenticated:

    st.title("🔐 Manager Access")

    st.write("Enter the manager code to continue.")

    manager_code = st.text_input(
        "Manager Code",
        type="password"
    )

    if st.button("Unlock"):

        if manager_code == MANAGER_CODE:

            st.session_state.manager_authenticated = True
            st.rerun()

        else:

            st.error("Incorrect manager code.")

    st.stop()


# ============================================================
# MANAGER DASHBOARD
# ============================================================

if manager_page and st.session_state.manager_authenticated:

    st.title("🔧 Manager Dashboard")

    st.success("Manager access granted.")

    # --------------------------------------------------------
    # LOCK MANAGER PANEL
    # --------------------------------------------------------

    if st.button("🔒 Lock Manager Panel"):

        st.session_state.manager_authenticated = False

        st.query_params.clear()

        st.rerun()

    st.divider()

    st.header("📋 Inventory")


    # ========================================================
    # ADD CAR
    # ========================================================

    with st.expander("➕ Add a New BMW"):

        with st.form("add_car_form"):

            col1, col2 = st.columns(2)

            # ------------------------------------------------
            # LEFT COLUMN
            # ------------------------------------------------

            with col1:

                model = st.text_input(
                    "Model",
                    placeholder="Example: X3"
                )

                year = st.number_input(
                    "Year",
                    min_value=1900,
                    max_value=2100,
                    value=2026
                )

                price = st.number_input(
                    "Price (€)",
                    min_value=0,
                    value=40000,
                    step=500
                )

                fuel = st.selectbox(
                    "Fuel",
                    [
                        "Petrol",
                        "Diesel",
                        "Hybrid",
                        "Electric"
                    ]
                )

                transmission = st.selectbox(
                    "Transmission",
                    [
                        "Automatic",
                        "Manual"
                    ]
                )


            # ------------------------------------------------
            # RIGHT COLUMN
            # ------------------------------------------------

            with col2:

                body_type = st.selectbox(
                    "Body Type",
                    [
                        "SUV",
                        "Sedan",
                        "Hatchback",
                        "Coupe",
                        "Wagon",
                        "Convertible"
                    ]
                )

                horsepower = st.number_input(
                    "Horsepower",
                    min_value=0,
                    value=150,
                    step=10
                )

                mileage = st.number_input(
                    "Mileage (km)",
                    min_value=0,
                    value=0,
                    step=1000
                )

                seats = st.number_input(
                    "Seats",
                    min_value=1,
                    max_value=20,
                    value=5
                )

                available = st.checkbox(
                    "Available",
                    value=True
                )


            submitted = st.form_submit_button(
                "➕ Add Car"
            )


            # =================================================
            # SAVE CAR
            # =================================================

            if submitted:

                if not model.strip():

                    st.error(
                        "Please enter a car model."
                    )

                else:

                    connection = sqlite3.connect(
                        "cars.db"
                    )

                    cursor = connection.cursor()

                    cursor.execute(
                        """
                        INSERT INTO cars (
                            brand,
                            model,
                            year,
                            price,
                            fuel,
                            transmission,
                            body_type,
                            horsepower,
                            mileage,
                            seats,
                            available
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            "BMW",
                            model.strip(),
                            year,
                            price,
                            fuel,
                            transmission,
                            body_type,
                            horsepower,
                            mileage,
                            seats,
                            int(available)
                        )
                    )

                    connection.commit()
                    connection.close()

                    st.success(
                        f"BMW {model} was added successfully!"
                    )

                    st.rerun()


    # ============================================================
    # CURRENT INVENTORY
    # ============================================================

    connection = sqlite3.connect("cars.db")

    cars = pd.read_sql_query(
        "SELECT * FROM cars ORDER BY id",
        connection
    )

    connection.close()

    st.dataframe(
        cars,
        use_container_width=True,
        hide_index=True
    )

    st.stop()


# ============================================================
# AI TOOL
# ============================================================

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


# ============================================================
# AI TOOLS
# ============================================================

tools = [

    {
        "type": "function",

        "function": {

            "name": "find_cars",

            "description":
                "Search the BMW dealership inventory for cars "
                "matching the customer's requirements.",

            "parameters": {

                "type": "object",

                "properties": {

                    "max_price": {

                        "type": "integer",

                        "description":
                            "Maximum budget in euros."

                    },

                    "fuel": {

                        "type": "string",

                        "description":
                            "Fuel type, such as Petrol, Diesel, Hybrid, or Electric."

                    },

                    "transmission": {

                        "type": "string",

                        "description":
                            "Transmission type, such as Automatic or Manual."

                    },

                    "body_type": {

                        "type": "string",

                        "description":
                            "Body type, such as SUV, Sedan, Coupe, Hatchback, Wagon, or Convertible."

                    }
                }
            }
        }
    }
]


# ============================================================
# AI SYSTEM
# ============================================================

SYSTEM_PROMPT = """

You are a professional BMW dealership customer-support assistant.

LANGUAGE:

Always answer in the same language as the customer.

French customer → ONLY French.
English customer → ONLY English.

If the customer changes language,
immediately change to that language.

Never repeat or paraphrase the customer's message.

INVENTORY:

- The dealership sells BMW vehicles.
- Never invent cars, prices, specifications, or availability.
- When the customer asks about cars, use the find_cars tool.
- Only recommend vehicles returned by the find_cars tool.
- Never make up inventory information.

TOOL USAGE:

Use max_price when the customer gives a maximum budget.

Use fuel when the customer specifies a fuel type.

Use transmission when the customer specifies automatic or manual.

Use body_type when the customer specifies a vehicle type.

If a requirement was not specified by the customer,
do not invent one.

STYLE:

- Friendly and professional.
- Keep responses concise and natural.
- Do not mention tools, databases, APIs, programming,
  or internal processes.
- Do not expose internal reasoning.
"""


# ============================================================
# CHAT MEMORY
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = [

        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }

    ]


# ============================================================
# CUSTOMER CHAT
# ============================================================

st.title("🚗 BMW Assistant")

st.caption(
    "Tell me what kind of BMW you're looking for."
)


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        with st.chat_message("user"):

            st.write(
                message["content"]
            )


    elif message["role"] == "assistant":

        with st.chat_message("assistant"):

            st.write(
                message["content"]
            )


# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input(
    "What kind of BMW are you looking for?"
)


if user_input:

    # --------------------------------------------------------
    # SHOW USER MESSAGE
    # --------------------------------------------------------

    with st.chat_message("user"):

        st.write(user_input)


    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )


    # ========================================================
    # FIRST AI CALL
    # ========================================================

    response = client.chat.completions.create(

        model=MODEL,

        messages=st.session_state.messages,

        tools=tools
    )


    assistant_message = response.choices[0].message


    # ========================================================
    # TOOL CALL
    # ========================================================

    if assistant_message.tool_calls:

        # Convert the Hugging Face message into a normal
        # dictionary that can be sent back to the API.

        assistant_dict = {
            "role": "assistant",
            "content": assistant_message.content or "",
            "tool_calls": []
        }


        for tool_call in assistant_message.tool_calls:

            assistant_dict["tool_calls"].append(
                {
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments
                    }
                }
            )


        st.session_state.messages.append(
            assistant_dict
        )


        # ----------------------------------------------------
        # EXECUTE TOOLS
        # ----------------------------------------------------

        for tool_call in assistant_message.tool_calls:

            if tool_call.function.name == "find_cars":

                arguments = tool_call.function.arguments


                # Hugging Face returns arguments as JSON text
                if isinstance(arguments, str):

                    arguments = json.loads(arguments)


                result = find_cars(
                    **arguments
                )


                st.session_state.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": "find_cars",
                        "content": result
                    }
                )


        # ====================================================
        # SECOND AI CALL
        # ====================================================

        final_response = client.chat.completions.create(

            model=MODEL,

            messages=st.session_state.messages,

            tools=tools
        )


        answer = final_response.choices[0].message.content


        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )


    # ========================================================
    # NORMAL AI RESPONSE
    # ========================================================

    else:

        answer = assistant_message.content

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )


    # ========================================================
    # SHOW AI RESPONSE
    # ========================================================

    with st.chat_message("assistant"):

        st.write(answer)