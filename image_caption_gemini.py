import base64
import json
from time import time, sleep
from copy import deepcopy

import google.generativeai as genai

# Set your Gemini API key
genai.configure(api_key="api-key")

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def read_image(id):
  # scenario path
  scenario_path = f"scenario_images/s{id}.png"

  # Getting the base64 string
  scenario_image = encode_image(scenario_path)

  # create json for reading image file
  image_json = {
    "mime_type": "image/png", 
    "data": scenario_image
    }
  return image_json

def image_to_text():
  # Use Gemini model
  model = genai.GenerativeModel("gemini-1.5-pro",
    system_instruction="You are an automotive UI design expert having an extensive knowledge of autonomous vehicles (AVs),\
    external human-machine interface (eHMI), and smart pole interaction units (SPIUs). \
    Respond to the user query with coherent and detailed paragraphs."
    )
  
  with open("prompts.json", "r") as f:
    prompts = json.load(f)

  # image_to_text for 8 scenarios
  for idx, prompt in enumerate(prompts):
    # add image to the prompt
    image_json = read_image(idx+1)

    payload = {
        "parts": [
            {"text": prompt["content"][0]["text"]},  # Text part
            {"inline_data": image_json}  # Image part
        ]
    }

    # record starting time
    starttime = time()

    # send request to server
    response = model.generate_content(
        contents=[payload],  # Pass the prompt content here
        generation_config=genai.GenerationConfig(max_output_tokens=2048)
    )

    # record request return time
    endtime = time()

    # save the generated response
    with open(f"gemini/s{idx+1}.txt", "+a") as f:
      f.write(response.text +'\n'*3+'-'*40)

    print(f"Scenario{idx+1}")
    print("Latency: ", endtime - starttime)
    print("Input Tokens: ", response.usage_metadata.prompt_token_count)
    print("Output Tokens: ", response.usage_metadata.candidates_token_count)
    sleep(60)

if __name__ == '__main__':
  print('Performing Analysis')
  for i in range(4):
    print('Round number: ', i)
    image_to_text()
    print(f'Round number: {i} Complete\n')
