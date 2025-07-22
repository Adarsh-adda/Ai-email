# AI Email Reply System

An automated email reply system that uses AI to generate responses to incoming emails.

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Ai-email
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit the `.env` file and add your actual values:
   - `PERPLEXITY_API_KEY`: Your Perplexity AI API key
   - `EMAIL_HOST_USER`: Your Gmail address
   - `EMAIL_HOST_PASSWORD`: Your Gmail app password (not your regular password)
   - `SECRET_KEY`: A Django secret key (generate one for production)

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   # Development server
   python manage.py runserver
   
   # Or with Docker
   docker-compose up
   ```

## Features

- Automated email monitoring and response
- AI-powered reply generation using Perplexity AI
- Celery-based background task processing
- Redis for message queuing

Email monitoring on rebexisaws@gmail.com to get AI generated replies.
