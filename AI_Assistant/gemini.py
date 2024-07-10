import google.generativeai as genai
import os

class Model:
    def __init__(self):
        api_key = os.getenv('GEMINI_TOKEN')
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        self.chat = None
    
    def set_chat(self):
        self.chat=self.model.start_chat(history=[])

    def get_response(self,user_input):
        response =self.chat.send_message(user_input)
        return response.text