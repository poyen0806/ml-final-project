import google.generativeai as genai
from configparser import ConfigParser

# Config Parser
config = ConfigParser()
config.read("config.ini")
genai.configure(api_key=config["Gemini"]["API_KEY"])


system_prompt = '''
You are a coding expert that specializes in rendering code for front-end interfaces. 
When I describe a component of a website I want to build, please return the HTML and CSS needed to do so. 
Do not give an explanation for this code. Also offer some UI design suggestions.
'''
user_prompt = '''
Create a box in the middle of the page that contains a rotating selection of images each with a caption. 
The image in the center of the page should have shadowing behind it to make it stand out. 
It should also link to another page of the site. Leave the URL blank so that I can fill it in.
'''
model = genai.GenerativeModel(
    model_name = 'gemini-1.5-pro',
    system_instruction=system_prompt,
    generation_config=genai.GenerationConfig(
        max_output_tokens=2000,     # Limit the length of the output
        temperature=0.9,            # Higher temperature means more randomness
        #top_k=1,                     
        #top_p=0.9,
        #stop_sequences=['\n']       # Stop generation at the first newline character
    )
)
response = model.generate_content(
    user_prompt,
    generation_config = genai.GenerationConfig(stop_sequences=['\n6'])
)

print(response.text)