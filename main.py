"""
Market Newsletter Generator
Fetches market news, analyzes with LLM, and sends institutional insights via email
"""

import os
import sys
import smtplib
import json
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

# Now import OpenAI after env vars are loaded
from openai import OpenAI


class MarketNewsletterGenerator:
    def __init__(self):
        # Get environment variables
        openai_api_key = os.getenv("OPENAI_API_KEY")
        self.newsapi_key = os.getenv("NEWSAPI_KEY")
        self.gmail_user = os.getenv("GMAIL_USER")
        self.gmail_password = os.getenv("GMAIL_PASSWORD")
        self.recipient_email = os.getenv("RECIPIENT_EMAIL")
        
        # Validate and initialize OpenAI client
        if not openai_api_key:
            print("ERROR: OPENAI_API_KEY not found in environment!")
            print(f"Current working directory: {os.getcwd()}")
            print(f".env file present: {os.path.exists('.env')}")
            print("\nMake sure:")
            print("  1. .env file exists in the current directory")
            print("  2. OPENAI_API_KEY is set in .env")
            print("  3. The value starts with 'sk-'")
            sys.exit(1)
        
        try:
            self.openai_client = OpenAI(api_key=openai_api_key)
        except Exception as e:
            print(f"ERROR: Failed to initialize OpenAI client: {e}")
            sys.exit(1)
        
        # Validate other required environment variables
        if not all([self.newsapi_key, self.gmail_user, self.gmail_password, self.recipient_email]):
            missing = []
            if not self.newsapi_key: missing.append("NEWSAPI_KEY")
            if not self.gmail_user: missing.append("GMAIL_USER")
            if not self.gmail_password: missing.append("GMAIL_PASSWORD")
            if not self.recipient_email: missing.append("RECIPIENT_EMAIL")
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
    
    def fetch_market_news(self):
        """Fetch market news from NewsAPI for the last 24 hours"""
        print("Fetching market news...")
        
        # Keywords focused on macro, fixed income, equities, and market-moving news
        search_terms = [
            "Federal Reserve interest rates",
            "bonds fixed income",
            "stock market S&P 500",
            "inflation economic data",
            "central bank policy",
            "forex currency markets",
            "emerging markets",
            "commodity prices oil",
            "credit spreads yields",
            "quantitative tightening"
        ]
        
        all_articles = []
        
        for term in search_terms:
            try:
                url = "https://newsapi.org/v2/everything"
                params = {
                    "q": term,
                    "sortBy": "publishedAt",
                    "language": "en",
                    "apiKey": self.newsapi_key,
                    "pageSize": 5
                }
                
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                if data["status"] == "ok":
                    all_articles.extend(data["articles"])
            except requests.RequestException as e:
                print(f"Error fetching news for '{term}': {e}")
                continue
        
        # Remove duplicates based on URL
        seen_urls = set()
        unique_articles = []
        for article in all_articles:
            if article["url"] not in seen_urls:
                seen_urls.add(article["url"])
                unique_articles.append(article)
        
        print(f"Fetched {len(unique_articles)} unique market articles")
        return unique_articles[:20]  # Limit to top 20 articles
    
    def analyze_with_llm(self, articles):
        """Use OpenAI to analyze market news and generate insights"""
        print("Analyzing market news with AI...")
        
        # Format articles for LLM
        articles_text = "\n\n".join([
            f"Title: {article['title']}\n"
            f"Source: {article['source']['name']}\n"
            f"Published: {article['publishedAt']}\n"
            f"Summary: {article.get('description', 'N/A')}"
            for article in articles
        ])
        
        prompt = f"""You are a smart market analyst who breaks down institutional trading concepts for traders who actually care about making money. 
Think of tone like explaining to a trading buddy at the desk, not a Bloomberg terminal.

Analyze the following market news from the last 24 hours and create a practical market commentary with actionable insights.

RECENT NEWS:
{articles_text}

Please provide:
1. MARKET SNAPSHOT (2-3 paragraphs): What actually moved in the last 24 hours? (macro, rates, equities, forex, commodities) - skip the fluff
2. RECENT CONTEXT (2-3 paragraphs): How does this fit into what's been happening? What's the actual trend?
3. NEAR-TERM OUTLOOK (2-3 paragraphs): What could happen next week or two? Key dates/catalysts to watch
4. LONG-TERM PERSPECTIVE (2-3 paragraphs): Where is this heading over the next 6-12 months? What's the bigger picture?
5. YOUR TAKE: What matters most RIGHT NOW and why you actually care about it
6. PROPOSED TRADE: A real trade you'd actually do if you had conviction. What's the play?
   - What to buy/sell/hedge and why
   - When/where to get in
   - Where it breaks (stop loss)
   - Where you're happy to take profit
   - Why this wins if you're right, what could go wrong

Keep it real. Use specific metrics and numbers. Assume the reader knows markets but appreciates straight talk.
Be direct - what's the actual edge here?"""
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        return response.choices[0].message.content
    
    def format_email(self, analysis):
        """Format the analysis as an HTML email"""
        timestamp = datetime.now().strftime("%B %d, %Y at %H:%M %Z")
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #1a1a1a;
            max-width: 900px;
            margin: 0;
            padding: 20px;
        }}
        .header {{
            border-bottom: 3px solid #1e40af;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            margin: 0;
            color: #1e40af;
            font-size: 28px;
        }}
        .timestamp {{
            color: #666;
            font-size: 12px;
            margin-top: 5px;
        }}
        .section {{
            margin-bottom: 25px;
        }}
        .section h2 {{
            color: #1e40af;
            font-size: 18px;
            border-left: 4px solid #1e40af;
            padding-left: 12px;
            margin-bottom: 12px;
        }}
        .section p {{
            margin: 10px 0;
            text-align: justify;
        }}
        .trade-box {{
            background-color: #f0f9ff;
            border-left: 4px solid #dc2626;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }}
        .trade-box h3 {{
            color: #dc2626;
            margin-top: 0;
        }}
        .footer {{
            border-top: 1px solid #ccc;
            padding-top: 15px;
            margin-top: 30px;
            font-size: 12px;
            color: #666;
        }}
        .conviction {{
            background-color: #fef3c7;
            padding: 15px;
            border-radius: 4px;
            border-left: 4px solid #f59e0b;
            margin: 15px 0;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📈 MARCO'S MARKET NOTES</h1>
        <div class="timestamp">Today's Take · {timestamp}</div>
    </div>
    
    <div style="white-space: pre-wrap; font-family: 'Courier New', monospace; font-size: 14px; line-height: 1.5;">
{analysis}
    </div>
    
    <div class="footer">
        <p><strong>Marco's Market Notes</strong></p>
        <p>Daily takes on what's moving and why it matters for your portfolio. 
        Breaking down institutional concepts for people who actually trade.</p>
        <p style="margin-top: 20px; color: #999; font-size: 11px;">
            ⚠️ Disclaimer: For informational purposes. Not investment advice. Do your own research.
            Past performance ≠ future results. This is Marco's opinion, not a recommendation.
        </p>
    </div>
</body>
</html>
"""
        return html_content
    
    def send_email(self, html_content):
        """Send the email via Gmail SMTP"""
        print("Sending email...")
        
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Market Intelligence Brief - {datetime.now().strftime('%B %d, %Y')}"
        msg["From"] = self.gmail_user
        msg["To"] = self.recipient_email
        
        # Attach HTML content
        msg.attach(MIMEText(html_content, "html"))
        
        try:
            # Gmail SMTP server
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10)
            server.login(self.gmail_user, self.gmail_password)
            server.sendmail(self.gmail_user, self.recipient_email, msg.as_string())
            server.quit()
            print(f"✓ Email sent successfully to {self.recipient_email}")
        except smtplib.SMTPException as e:
            print(f"✗ Failed to send email: {e}")
            raise
    
    def run(self):
        """Execute the full newsletter generation pipeline"""
        try:
            print("\n" + "="*60)
            print("MARKET NEWSLETTER GENERATOR")
            print("="*60 + "\n")
            
            # Fetch news
            articles = self.fetch_market_news()
            
            if not articles:
                print("No market news found. Exiting.")
                return
            
            # Analyze with LLM
            analysis = self.analyze_with_llm(articles)
            
            # Format email
            html_email = self.format_email(analysis)
            
            # Send email
            self.send_email(html_email)
            
            print("\n" + "="*60)
            print("Newsletter generation completed successfully!")
            print("="*60 + "\n")
            
        except Exception as e:
            print(f"\n✗ Error during newsletter generation: {e}")
            raise


if __name__ == "__main__":
    generator = MarketNewsletterGenerator()
    generator.run()