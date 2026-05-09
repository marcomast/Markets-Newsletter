# Market Newsletter Generator

An automated script that generates institutional-grade market intelligence briefings by analyzing real-time market news using AI and sends them via email.

## Features

- **Real-time Market News**: Fetches the latest market news from NewsAPI focusing on macro, fixed income, and equities
- **AI-Powered Analysis**: Uses OpenAI's Claude to analyze news and generate institutional-level insights
- **Institutional Perspective**: Analyzes markets from a bulge bracket bank trading floor perspective
- **Comprehensive Coverage**: 
  - Market snapshot of recent 24 hours
  - Context against recent past trends
  - Near-term outlook (1-4 weeks)
  - Long-term perspective (3-12 months)
  - Personal conviction and take
  - Actionable trade recommendation with entry/exit levels
- **Automated Email Delivery**: Sends formatted HTML email to your inbox

## Prerequisites

You'll need accounts/keys for:

1. **OpenAI API**: For AI-powered news analysis
   - Sign up at: https://platform.openai.com
   - Get API key from: https://platform.openai.com/api-keys
   - Requires paid credits (typical cost: $1-3 per run)

2. **NewsAPI**: For fetching market news
   - Sign up at: https://newsapi.org
   - Free tier available with API key

3. **Gmail Account**: For sending emails
   - Use your Gmail address
   - Need an "App-specific password": https://myaccount.google.com/apppasswords
   - (Not your regular Gmail password for security)

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project directory:

```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:

```
OPENAI_API_KEY=sk-... (from https://platform.openai.com/api-keys)
NEWSAPI_KEY=... (from https://newsapi.org/account/api-keys)
GMAIL_USER=marcomast1872@gmail.com
GMAIL_PASSWORD=... (Your regular Gmail password)
RECIPIENT_EMAIL=marcomast1872@gmail.com
```

**Important**: Never commit your `.env` file to version control!

### 3. Obtain API Keys

#### OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy and paste into `.env` file

#### NewsAPI Key
1. Go to https://newsapi.org/register
2. Sign up for free account
3. Copy API key from your account page
4. Paste into `.env` file

#### Gmail Setup
1. Use your regular Gmail account: `marcomast1872@gmail.com`
2. Your password is the same one you use to log into Gmail
3. Paste it into `.env` file as `GMAIL_PASSWORD`

**If authentication fails:**
- Go to https://myaccount.google.com/lesssecureapps
- Click "Turn on Less secure app access"
- Then try running the script again

## Usage

### Run Immediately

```bash
python main.py
```

This will:
1. Fetch the latest market news
2. Analyze with AI
3. Format as HTML email
4. Send to your email address
5. Display results in console

### Schedule Runs

#### Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., Daily at 6:00 PM)
4. Set action: Run program
   - Program: `C:\Python\python.exe` (or your Python path)
   - Arguments: `C:\Users\marco\Desktop\Market Newsletter\main.py`
   - Start in: `C:\Users\marco\Desktop\Market Newsletter`

#### Cron Job (Linux/Mac)

Add to crontab:
```bash
# Run daily at 6 PM
0 18 * * * cd /path/to/Market\ Newsletter && python main.py
```

## Email Output

The script generates a professional HTML email containing:

- **Market Snapshot**: What happened in the last 24 hours
- **Recent Context**: How current news fits into recent trends
- **Near-Term Outlook**: Expected moves in next 1-4 weeks
- **Long-Term Perspective**: 3-12 month outlook
- **Author's Conviction**: Bold take on what matters most
- **Proposed Trade**: 
  - Specific asset or strategy
  - Entry points and stop losses
  - Target levels
  - Risk/reward analysis
  - Recommended positioning

## Cost Estimates

- **OpenAI**: ~$1-3 per run (depends on article count and analysis depth)
- **NewsAPI**: Free tier (100 requests/day)
- **Gmail**: Free
- **Total**: ~$30-90/month if run daily

## Troubleshooting

### "Missing required environment variables"
- Check `.env` file exists in project directory
- Verify all required keys are filled in
- Restart Python after updating `.env`

### "Could not authenticate with email"
- Verify Gmail username (`marcomast1872@gmail.com`) and password are correct
- Try enabling "Less secure app access": https://myaccount.google.com/lesssecureapps
- Make sure you're using your regular Gmail password (not something else)

### "API key invalid"
- OpenAI: Check key starts with "sk-"
- NewsAPI: Verify key is correct from newsapi.org/account
- Test keys in their respective dashboards

### "No articles found"
- Check internet connection
- Verify NewsAPI key is valid
- Try running again (rate limits may apply)

### Email not formatting correctly
- Some email clients may not render HTML well
- Try opening in different email client or web browser
- Check email source code for malformed HTML

## Features & Customization

### Modify News Topics

Edit the `search_terms` list in `fetch_market_news()`:
```python
search_terms = [
    "Federal Reserve interest rates",
    "bonds fixed income",
    # Add more custom terms here
]
```

### Change AI Model

Update the model in `analyze_with_llm()`:
```python
response = self.openai_client.messages.create(
    model="gpt-4",  # or "gpt-3.5-turbo", "claude-opus", etc.
    ...
)
```

### Adjust Analysis Depth

Change `max_tokens` in `analyze_with_llm()`:
```python
max_tokens=2000,  # Increase for more detailed analysis
```

### Customize Email Template

Edit HTML in `format_email()` method:
- Styling in `<style>` tags
- Content structure in body

## Security Notes

1. **Never** commit `.env` to version control
2. Use separate app passwords for email (not your actual password)
3. Rotate API keys periodically
4. Use environment variables for all sensitive data
5. Consider using a password manager for credentials

## Support & Troubleshooting

For API issues:
- OpenAI: https://platform.openai.com/docs
- NewsAPI: https://newsapi.org/docs
- Gmail SMTP: https://support.google.com/mail/answer/7126229

## License

Personal use. Modify as needed.
