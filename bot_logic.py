import json
import difflib
import openai
import os

class SimpleChatBot:
    def __init__(self, intents_file="intents.json"):
        with open("intents.json", encoding="utf-8") as f:
         self.intents = json.load(f)

        self.threshold = 0.6

    def get_response(self, user_input):
        user_input = user_input.lower()
        best_match = None
        best_ratio = 0

        for intent in self.intents["intents"]:
            for pattern in intent["patterns"]:
                ratio = difflib.SequenceMatcher(None, user_input, pattern.lower()).ratio()
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_match = intent

        if best_ratio > self.threshold:
            return best_match["responses"][0]

        return self.ask_gpt(user_input)

    def ask_gpt(self, prompt):
        openai.api_key = os.getenv("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")
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful customer support assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message["content"]
        except Exception as e:
            return "⚠️ Sorry, I'm having trouble connecting to the AI service right now."
