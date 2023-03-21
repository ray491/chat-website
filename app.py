from flask import Flask, render_template, request
import spacy
import openai
import concurrent.futures



app = Flask(__name__)

# Initialize OpenAI API key
openai.api_key = "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"

# Initialize spaCy model
nlp = spacy.load("en_core_web_sm")

def generate_response(prompt, entities, sentiment):
    """
    Generate a response from OpenAI given the user's prompt, detected entities,
    and sentiment analysis results.
    """
    try:
        if len(entities) == 0:
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=f"Chatbot: I'm not sure what you're asking about. Can you provide more context?\n{prompt}",
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            ).choices[0].text
        else:
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=(
                    f"Chatbot: You asked about the following entities: {', '.join(entities)}. How can I help you with that? (Sentiment: {sentiment})\n"
                    f"{prompt}"
                ),
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            ).choices[0].text
        return response
    except Exception as e:
        print(f"Error: {e}")
        response = "Sorry, I encountered an error. Can you try asking your question again?"
        return response

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chatbot", methods=["POST"])
def chatbot():
    nlp = spacy.load("en_core_web_sm")
    openai.api_key = "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"

    # get user input from the form
    user_input = request.form["user_input"]

    if user_input.lower() == "hello":
        response = "Bot: Hello there."
    elif user_input.lower() == "how are you":
        response = "Bot: I'm doing well, thank you. How about you?"
    elif user_input.lower() == "who is your creator?":
        response = "Bot: Ray Achakzai"
    elif user_input.lower() == "what's your name":
        response = "Bot: My name is Chatbot. Nice to meet you!"
    elif user_input.lower() == "bye":
        response = "Bot: Bye! Have a great day."
    else:
        doc = nlp(user_input)
        entities = []
        for ent in doc.ents:
            entities.append(ent.text)
        sentiment = doc.sentiment
        if sentiment >= 0.5:
            sentiment = "positive"
        elif sentiment <= -0.5:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_response = executor.submit(generate_response, user_input, entities, sentiment)
            response = "Bot: " + future_response.result()

    return response

