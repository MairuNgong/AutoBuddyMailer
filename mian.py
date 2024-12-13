from fastapi import FastAPI, HTTPException
from typing import Dict
from pydantic import BaseModel, Field
import uvicorn
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))

app = FastAPI()


if __name__ == "__main__" :
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")

# Define the request model
class MessageRequest(BaseModel):
    participants : Dict[str,str] = Field(
         default={
            "John": "john@example.ac.th",
            "Ken": "Ken@example.ac.th",
            "Alice": "Alice@example.ac.th",
            "Snow": "Snow@example.ac.th",
            "Milli": "Milli@example.ac.th"
        },
        description="Default list of participants"
    )
    template: str  = Field(
         default=(
            "สวัสดี {giver}💕,\n"
            "บัดดี้ของเธอคือ {buddy}!\n"
            "ขอให้สนุกกับการเลือกของขวัญนะ💖✨"
        ),
        description="Default message template"
    )

def assign_buddies(participants):
    names = list(participants.keys())
    shuffled = names[:]
    while True:
        random.shuffle(shuffled)
        if all(name != buddy for name, buddy in zip(names, shuffled)):
            break
    return dict(zip(names, shuffled))

@app.post("/sent-emails")
def sent_emails(request: MessageRequest):
    try:
          server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
          server.starttls()
          server.login(SENDER_EMAIL, SENDER_PASSWORD)

          responseBody = []
          assignments = assign_buddies(request.participants)
          for giver, buddy in assignments.items():
                  receiver_email = request.participants[giver]

                  message = MIMEMultipart()
                  message["From"] = SENDER_EMAIL
                  message["To"] = receiver_email
                  message["Subject"] = "บัดดี้ของเธอคือ...(Real)"

                  body = request.template.format(giver=giver, buddy=buddy)
                  message.attach(MIMEText(body, "plain"))

                  # server.sendmail(SENDER_EMAIL, receiver_email, message.as_string())
                  responseBody.append(f"Email sent to {giver} at {receiver_email}")

    except Exception as e:
         responseBody = e
    finally:
         server.quit()
    
    return {"response": responseBody}
