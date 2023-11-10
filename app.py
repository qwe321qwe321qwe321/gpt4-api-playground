from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
# You should create a .env file and add a line: OPENAI_API_KEY=<your_openai_key>
load_dotenv()

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    imageUrl = request.form['image_url'].strip()
    promptText = request.form['prompt'].strip()

    if imageUrl and promptText:
        print(promptText + " -> " + imageUrl)
        try:
            response = client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": promptText},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": imageUrl,
                                    "detail": "high"
                                },
                            },
                        ],
                    }
                ],
                max_tokens=1500,
            )
            print(response)
            answer = response.choices[0].message.content.strip()
            return jsonify({'status': 'OK', 'answer': answer})
        except Exception as e:
            print(e)
            return jsonify({'status': 'ERROR', 'answer': e.message})
    else:
        return jsonify({'status': 'ERROR', 'answer': 'Input Error: Please provide an image and the prompt to ask for GPT4.'})

@app.route('/imagine', methods=['POST'])
def imagine():
    promptText = request.form['prompt'].strip()

    if promptText:
        print(promptText)
        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=promptText,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            print(response)
            answer = response.data[0].revised_prompt
            url = response.data[0].url
            return jsonify({'status': 'OK', 'image_url': url, "answer": answer})
        except Exception as e:
            print(e)
            return jsonify({'status': 'ERROR', 'answer': e.message})
    else:
        return jsonify({'status': 'ERROR', 'answer': 'Please provide an image description.'})

if __name__ == '__main__':
    app.run(debug=True)