import os
from openrouter import OpenRouter
import dotenv
import json
import eel

dotenv.load_dotenv()
eel.init('web')

apiKey = os.getenv("API_KEY")
client = OpenRouter(api_key=apiKey)

rules = ""
skill = open("Agents.md", "r")
rules = skill.read()
skill.close()

@eel.expose
def agenticAI(prompt):
    print('Received a prompt')
    response = client.chat.send(
        model="nvidia/nemotron-3-ultra-550b-a55b:free",
        messages=[{ "role": "user", "content": f"{rules} {prompt}" }],
    )

    response = response.choices[0].message.content
    response = json.loads(response)

    for x in response:
        dirname = os.path.dirname(x['filePath'])
        if dirname:
            os.makedirs(dirname, exist_ok=True)

        with open(x['filePath'], "w") as f:
            f.write(x['code'])
    
    msg = client.chat.send(
        model="nvidia/nemotron-3-ultra-550b-a55b:free",
        messages=[{ "role": "user", "content": "Summarize your actions till now in 1-20 words maximum." }],
    )
    return msg.choices[0].message.content

eel.start('index.html', size=(1600, 900))