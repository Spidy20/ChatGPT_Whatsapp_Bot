from flask import Flask, request
import openai
from twilio.twiml.messaging_response import MessagingResponse
import os

# Init the Flask App
app = Flask(__name__)

# Initialize the OpenAI API key
# export OPENAI_API_KEY=YOUR API KEY
openai.api_key = os.environ.get("OPENAI_API_KEY")


# Define a function to generate answers using GPT-3
def generate_answer(question):
    model_engine = "text-davinci-002"
    prompt = (f"Q: {question}\n"
              "A:")

    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    answer = response.choices[0].text.strip()
    return answer


# Define a route to handle incoming requests
@app.route('/chatgpt', methods=['POST'])
def chatgpt():
    incoming_que = request.values.get('Body', '').lower()
    print("Question: ", incoming_que)
    # Generate the answer using GPT-3
    answer = generate_answer(incoming_que)
    print("BOT Answer: ", answer)
    bot_resp = MessagingResponse()
    msg = bot_resp.message()
    msg.body(answer)
    return str(bot_resp)


# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
