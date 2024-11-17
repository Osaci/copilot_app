import base64
import re
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting, Part

class VertexClient():
    def multiturn_generate_content(self, prompt_queue):
        print(prompt_queue)
        vertexai.init(project="ultra-function-439306-r4", location="us-central1")
        model = GenerativeModel(
            "gemini-experimental",
            system_instruction=[textsi_1]
        )
        chat = model.start_chat()
        response = chat.send_message(
            [prompt_queue],
            generation_config=generation_config,
            safety_settings=safety_settings          
        )
        print(response)
        #text = re.search(r'|text: "|/*?', response)
        text = response.candidates[0].content.parts[0].text
        print(text)
        return text
textsi_1 = """ """

generation_config = {
    "max_output_tokens": 1024,
    "temperature": 0.2,
    "top_p": 0.8,
}

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
]
