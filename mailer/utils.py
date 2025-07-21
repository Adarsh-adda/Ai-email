import imaplib
import email
import httpx
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailLog
import requests

# Get API key from environment variable (SECURE)
import os

PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')

if not PERPLEXITY_API_KEY:
    raise ValueError("PERPLEXITY_API_KEY environment variable is required")


def get_email_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                payload = part.get_payload(decode=True)
                if payload:
                    return payload.decode(errors="ignore")
        return "No plain text body found."
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            return payload.decode(errors="ignore")
        return "No body content found."

import requests


def generate_reply_perplexity(email_body):
    """Main function with comprehensive debugging"""
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "sonar-pro",
        "messages": [
            {
                "role": "system",
                "content": "You are an AI email assistant. Reply professionally to the user's email."
            },
            {
                "role": "user",
                "content": email_body
            }
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }

    try:
        print(f"🔑 Using API Key: {PERPLEXITY_API_KEY[:10] if PERPLEXITY_API_KEY else 'None'}...")
        print(f"🌐 Making request to: {url}")
        print(f"📝 Request  {data}")

        response = requests.post(url, headers=headers, json=data)
        print(f"📡 Status Code: {response.status_code}")
        print(f"📡 Response Headers: {dict(response.headers)}")
        print(f"📡 Raw Response: {response.text}")

        response.raise_for_status()

        res_json = response.json()
        print("📡 Full Perplexity Response:", res_json)
        print("📡 Response keys:", list(res_json.keys()) if isinstance(res_json, dict) else "Not a dict")

        if 'choices' in res_json and len(res_json['choices']) > 0:
            message = res_json['choices'][0]['message']['content']
            print(f"✅ Successfully extracted message: {message[:100]}...")
            return message
        elif 'error' in res_json:
            error_msg = res_json['error']
            print(f"❌ API Error: {error_msg}")
            return f"API Error: {error_msg}"
        else:
            print("⚠️ Unexpected response format:", res_json)
            return "Sorry, I couldn't generate a response due to unexpected format."

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error {response.status_code}: {e}")
        print(f"Response text: {response.text}")

        if response.status_code == 401:
            return "Error: Invalid API key"
        elif response.status_code == 402:
            return "Error: Insufficient credits"
        elif response.status_code == 429:
            return "Error: Rate limit exceeded"
        else:
            return f"HTTP Error {response.status_code}: {e}"

    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error: {e}")
        return "Sorry, network error occurred."
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return "Sorry, unexpected error occurred."





def fetch_and_reply_emails():
    print("🔍 Connecting to mailbox...")
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    mail.select('inbox')

    status, data = mail.search(None, 'UNSEEN')
    email_ids = data[0].split()
    print(f"📬 UNSEEN Emails Found: {len(email_ids)}")

    for num in email_ids:
        _, msg_data = mail.fetch(num, '(RFC822)')
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject = msg['subject']
        sender = email.utils.parseaddr(msg['from'])[1]
        body = get_email_body(msg)

        print(f"📨 Email from: {sender}, Subject: {subject}")
        print(f"📄 Email body (first 200 chars): {body[:200]}")

        # Try the main function first
        ai_reply = generate_reply_perplexity(body)

        # If main function fails, try the chat model
        if ai_reply.startswith("Sorry") or ai_reply.startswith("Error"):
            print("⚠️ Main function failed, trying chat model...")
            ai_reply = generate_reply_perplexity(body)

        print(f"🤖 AI Reply: {ai_reply}")

        send_mail(
            subject=f"Re: {subject}",
            message=ai_reply,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[sender],
        )

        EmailLog.objects.create(
            sender=sender,
            subject=subject,
            body=body,
            reply=ai_reply,
            replied=True
        )

    mail.logout()
    print("✅ Done checking and replying.")


# Test function
def test_perplexity_api():
    """Test function to debug the API without email processing"""
    test_email = "Hi, I wanted to follow up on our meeting yesterday about the project timeline."

    print("Testing Perplexity API...")
    reply = generate_reply_perplexity(test_email)
    print(f"Final reply: {reply}")

    return reply

# Uncomment to test
# if __name__ == "__main__":
#     test_perplexity_api()