from elevenlabs.conversational_ai.conversation import ClientTools
from langchain_community.tools import DuckDuckGoSearchRun
import os
import requests
from PIL import Image
from io import BytesIO
import openai
from dotenv import load_dotenv
def search_web(parameters):
    "Searches the web using DuckDuckGo and returns the results."
    query = parameters.get("query")
    results = DuckDuckGoSearchRun(query=query)
    return results

def save_to_txt(parameters):
    "Saves the provided data to a text file."
    filename = parameters.get("filename")
    data = parameters.get("data")
    formatted_data = f"{data}"
    with open(filename, "a", encoding="utf-8") as file:
        file.write(formatted_data + "\n")
def generate_image(parameters):
    "Generates an image based on the provided prompt and saves it to a file."
    prompt = parameters.get("prompt")
    filename = parameters.get("filename")
    size = parameters.get("size", "1024x1024")
    save_dir = parameters.get("save_dir", "image_outputs")
    os.makedirs(save_dir, exist_ok=True)
    filepath = os.path.join(save_dir, filename)
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    client = openai.OpenAI()
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        n=1,
        quality="standard")
    image_url = response.data[0].url
    image_response = requests.get(image_url)
    image = Image.open(BytesIO(image_response.content))
    image.save(filepath)
    return f"Image saved to {filepath}"

client_tools = ClientTools()
client_tools.register("searchWeb", search_web)
client_tools.register("saveToTxt", save_to_txt)
client_tools.register("generateImage", generate_image)