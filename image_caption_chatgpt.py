import base64
import requests
import json
from time import time, sleep
from copy import deepcopy

# OpenAI API Key
api_key = "api-key"

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

def read_image(id):
  # scenario path
  scenario_path = f"scenario_images/s{id}.png"

  # Getting the base64 string
  scenario_image = encode_image(scenario_path)

  # create json for reading image file
  image_json = {
    "type": "image_url",
    "image_url": {
        "url": f"data:image/png;base64,{scenario_image}"
    }
  }
  return image_json

def image_to_text():
  # payload template
  payload = {
    "model": "gpt-4o",
    "messages": [
        {
        "role": "system",
        "content": [
            {
            "type": "text",
            "text": "You are an automotive UI design expert having an extensive knowledge of autonomous vehicles (AVs),\
                external human-machine interface (eHMI), and smart pole interaction units (SPIUs). \
                Respond to the user query with coherent and detailed paragraphs."
            }
        ]
        },
    ],
    "max_tokens": 2048
    }
  
  with open("prompts.json", "r") as f:
    prompts = json.load(f)

  # image_to_text for 8 scenarios
  for idx, prompt in enumerate(prompts):
    # add image to the prompt
    image_json = read_image(idx+1)
    prompt["content"].append(image_json)

    # add prompt to the system message from template
    final_payload = deepcopy(payload)
    final_payload["messages"].append(prompt)

    # record stating time
    starttime = time()

    # send request to server
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=final_payload).json()

    # record request return time
    endtime = time()

    # save the generated response
    with open(f"gpt/s{idx+1}.txt", "+a") as f:
      f.write(response['choices'][0]['message']['content']+'\n'*3+'-'*40)

    print(f"Scenario{idx+1}")
    print("Latency: ", endtime - starttime)
    print("Input Tokens: ", response["usage"]["prompt_tokens"])
    print("Output Tokens: ", response["usage"]["completion_tokens"])
    sleep(60)

if __name__ == '__main__':
  print('Performing Analysis')
  for i in range(5):
    print('Round number: ', i)
    image_to_text()
    print(f'Round number: {i} Complete\n')

  
