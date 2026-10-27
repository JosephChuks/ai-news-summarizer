import requests
import smtplib
from email.mime.text import MIMEText
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os

load_dotenv()


def send_email(subject, body, to_email):
    user = "admin@localhost"
    # Email sent locally using mailpit local SMTP server on port 1025
    with smtplib.SMTP("localhost", 1025) as server:
        html_body = body.decode("utf-8") if isinstance(body, bytes) else body
        message = MIMEText(html_body, "html", "utf-8")
        message["Subject"] = subject
        message["From"] = user
        message["To"] = to_email
        server.send_message(message)


url = (
    "https://newsapi.org/v2/top-headlines?"
    "category=business&"
    "language=en&"
    "pageSize=8&"
    "sortBy=publishedAt&apiKey=" + os.getenv("NEWS_API_KEY")
)

# Make request
request = requests.get(url)
# Get a dictionary with data
content = request.json()
articles = content["articles"]

model = init_chat_model(
    model=os.getenv("AI_MODEL"),
    model_provider=os.getenv("AI_MODEL_PROVIDER"),
    api_key=os.getenv("AI_API_KEY"),
)

prompt = f"""
You are a news summarizer. 
write a short paragraph for all the articles.
Add a second paragraph on how they affect the stock market.
Use html formatting for the output. (<p>)
Summarize the following articles:
{articles}
"""

response = model.invoke(prompt)
response_text = response.content[0]["text"]


# AI summarizing the news
body = f"<h1>Summary of Top News</h1><div>{response_text}</div>"
body = body.encode("utf-8")
send_email(subject="Top News", body=body, to_email="recipient@example.com")
