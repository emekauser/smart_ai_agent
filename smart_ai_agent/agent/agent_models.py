
from langchain_google_genai import ChatGoogleGenerativeAI

all_models = {
    "google_germini": "gemini-2.0-flash",
    "google_germini_embed": "models/gemini-embedding-exp-03-07"
}


def get_model(name: str):
    model_name = all_models.get(name)
    print(model_name)
    if model_name:
        return ChatGoogleGenerativeAI(model=model_name),
    return None
