import base64
from anthropic import Anthropic
import json
from time import time, sleep
from copy import deepcopy

# Claude API Key
api_key = "api-key"

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

client = Anthropic(api_key=api_key)

def read_image(id):
    # scenario path
    scenario_path = f"scenario_images/s{id}.png"
    
    # Getting the base64 string
    scenario_image = encode_image(scenario_path)
    
    # create json for reading image file
    image_json = {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": "image/png",
            "data": scenario_image
        }
    }
    return image_json

def image_to_text():
    # payload template
    payload = []
    
    with open("prompts.json", "r") as f:
        prompts = json.load(f)
    
    # image_to_text for 8 scenarios
    for idx, prompt in enumerate(prompts):
        # add image to the prompt
        image_json = read_image(idx+1)
        prompt["content"].append(image_json)
        
        # add prompt to the messages from template
        final_payload = deepcopy(payload)
        final_payload.append(prompt)
        
        # record starting time
        starttime = time()
        
        # send request to server
        response = client.messages.create(model="claude-3-5-sonnet-20240620", max_tokens=2048, 
                                          system="You are an automotive UI design expert having an extensive knowledge of autonomous vehicles (AVs), external human-machine interface (eHMI), and smart pole interaction units (SPIUs). Respond to the user query with coherent and detailed paragraphs.",
                                          messages=final_payload)
        
        # record request return time
        endtime = time()
        
        # save the generated response
        with open(f"claude/s{idx+1}.txt", "+a") as f:
            f.write(response.content[0].text+'\n'*3+'-'*40)
        
        print(f"Scenario{idx+1}")
        print("Latency: ", endtime - starttime)
        print("Input Tokens: ", response.usage.input_tokens)
        print("Output Tokens: ", response.usage.output_tokens)
        sleep(60)

if __name__ == '__main__':
    print('Performing Analysis')
    for i in range(5):
        print('Round number: ', i)
        image_to_text()
        print(f'Round number: {i} Complete\n')
