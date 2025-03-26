import streamlit as st
import requests
import json

# Get your free API key from https://openrouter.ai/
OPENROUTER_API_KEY = "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"

st.title("Marina's Recipe Generator")

ingredients = st.text_input("Enter ingredients (separated by commas):")
recipe_notes = st.text_area("Add any specific recipe notes or preferences (e.g., dietary restrictions, cuisine type, cooking time):")

if st.button("Generate Recipe"):
    if ingredients.strip():  # Ensure input is not empty or just spaces
        with st.spinner("Generating recipe..."):
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }
            prompt = f"Generate a detailed recipe using the following ingredients: {ingredients.strip()}."
            if recipe_notes.strip():
                prompt += f" Consider these notes: {recipe_notes.strip()}."

            payload = {
                "model": "google/gemini-2.5-pro-exp-03-25:free",  # Free model (You can also try deepseek-chat, gemma, etc.)
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }
            api_url = "https://openrouter.ai/api/v1/chat/completions"

            try:
                response = requests.post(api_url, headers=headers, json=payload)
                response.raise_for_status()

                data = response.json()
                if "choices" in data and len(data["choices"]) > 0:
                    recipe = data["choices"][0]["message"]["content"].strip()
                    st.subheader("Generated Recipe:")
                    st.write(recipe)
                else:
                    st.error("Unexpected response format from OpenRouter API.")

            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to OpenRouter API: {e}")
            except json.JSONDecodeError:
                st.error("Error decoding JSON response from OpenRouter API.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

    else:
        st.warning("Please enter some ingredients.")
