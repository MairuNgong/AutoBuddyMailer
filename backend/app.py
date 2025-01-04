from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
    uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="info")

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
    subject : str
    template: str

def assign_buddies(participants):
    names = list(participants.keys())
    if len(names) == 1 :
      return dict(zip(names,names))
    shuffled = names[:]
    while True:
        random.shuffle(shuffled)
        if all(name != buddy for name, buddy in zip(names, shuffled)):
            break
    return dict(zip(names, shuffled))


origins = [
    "http://localhost:8080",  
    "http://127.0.0.1:8080",  
    "http://frontend:8080",  
    "http://backend:8000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)


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
                  message["Subject"] = request.subject

                  body = request.template.format(giver=giver, buddy=buddy)
                  message.attach(MIMEText(body, "plain"))

                  # server.sendmail(SENDER_EMAIL, receiver_email, message.as_string())
                  responseBody.append(f"Email sent to {giver} at {receiver_email}")

    except Exception as e:
         responseBody = e
    finally:
         server.quit()
    
    return {"response": responseBody}
