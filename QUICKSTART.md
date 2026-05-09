# QUICK START GUIDE - Market Newsletter Generator

## What This Does

Runs a Python script that:
1. **Fetches market news** from the last 24 hours (via NewsAPI)
2. **Analyzes with AI** to create institutional market insights (via OpenAI)
3. **Generates a detailed report** with market analysis and trade ideas
4. **Sends you an email** with the full brief

The email includes:
- What happened in markets today
- How it connects to recent trends
- What's likely in the next few weeks
- Long-term outlook (3-12 months)
- **A specific trade recommendation** an institutional trader would make right now

## STEP 1: Get Your API Keys (5 minutes)

### OpenAI API Key
1. Go to: https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (starts with "sk-")
5. **Save it somewhere safe** - you'll need it in Step 2

(Note: OpenAI charges ~$1-3 per run based on analysis length)

### NewsAPI Key
1. Go to: https://newsapi.org/register
2. Create a free account
3. Verify your email
4. Go to: https://newsapi.org/account
5. Copy your API key
6. **Save it**

### Gmail Password
Just use your regular Gmail password (the one you use to log into Gmail):
1. Your Gmail password goes in the `.env` file as `GMAIL_PASSWORD`
2. That's it - nothing special needed

**If it doesn't work:**
- You may need to allow "less secure apps" at: https://myaccount.google.com/lesssecureapps
- Or try generating an app-specific password at: https://myaccount.google.com/apppasswords (requires 2-Factor Authentication)

## STEP 2: Set Up Environment (2 minutes)

1. **Open Command Prompt** in the Market Newsletter folder:
   - Hold Shift + Right-click in the folder
   - Select "Open PowerShell window here" (or "Open Command window here")

2. **Run setup**:
   ```
   setup.bat
   ```
   This installs all Python dependencies automatically.

## STEP 3: Configure Credentials (2 minutes)

1. **Copy the example config**:
   - In the folder, right-click `.env.example`
   - Select "Copy"
   - Right-click empty space
   - Select "Paste"
   - Rename to `.env` (remove the ".example")

2. **Edit the .env file**:
   - Right-click `.env`
   - Open with Notepad
   - Replace the placeholder values:
     ```
     OPENAI_API_KEY=sk-your-actual-key-here
     NEWSAPI_KEY=your-newsapi-key-here
     GMAIL_USER=marcomast1872@gmail.com
     GMAIL_PASSWORD=your-regular-gmail-password
     RECIPIENT_EMAIL=marcomast1872@gmail.com
     ```
   - Save (Ctrl+S)
   - Close

   **IMPORTANT**: Keep this file SECRET. Don't share it or upload to GitHub.

## STEP 4: Run the Script (1 minute)

### Test Run (First Time)

1. **Open Command Prompt** in the folder again
2. **Run**:
   ```
   python main.py
   ```
3. **Watch the output**:
   - You'll see it fetching news
   - Analyzing with AI
   - Sending email
   - Should take 30-60 seconds

4. **Check your email**:
   - Look for "Market Intelligence Brief"
   - Should arrive in your inbox in ~10 seconds

If it works, great! Move to Step 5.

If you get errors, see the **TROUBLESHOOTING** section below.

## STEP 5: Automate (Optional but Recommended)

### Option A: Daily at Same Time (Windows Task Scheduler)

1. **Run the task setup**:
   ```
   setup_task.bat
   ```

2. **Follow the prompts**:
   - It will ask what time to run (suggest: 18:00 for 6 PM)
   - It creates the task automatically

3. **Verify**:
   - Open Task Scheduler (search for "Task Scheduler")
   - Look for "Market Newsletter Generator"
   - Right-click and select "Run" to test

### Option B: Run on Demand Anytime

Just open Command Prompt and run:
```
python main.py
```

## QUICK COMMAND REFERENCE

```
# Install dependencies
setup.bat

# Run newsletter
python main.py

# Set up daily automation
setup_task.bat

# Delete the scheduled task (if needed)
schtasks /delete "Market Newsletter Generator" /f
```

## CUSTOMIZATION

### Change When It Runs Daily
1. Open Task Scheduler
2. Find "Market Newsletter Generator"
3. Right-click > Properties
4. Go to "Triggers" tab
5. Edit the time

### Change What News Topics It Analyzes
1. Open `config.ini`
2. Edit `search_keywords` section
3. Save
4. Run script again

### Get More Detailed Analysis
1. Open `config.ini`
2. Change `max_tokens = 2000` to `3000` or higher
3. Save
4. This makes reports longer/more detailed (costs more)

### Change the Analysis Perspective
Edit the prompt in `main.py` around line 150 to customize what the AI looks for.

## TROUBLESHOOTING

### Error: "Missing required environment variables"

**Solution**: 
- Make sure `.env` file is in the same folder as `main.py`
- Check that all 5 variables are filled in (no blanks)
- Close and reopen Command Prompt
- Try again

### Error: "Could not authenticate with email"

**Check**:
1. Gmail username is correct: `marcomast1872@gmail.com`
2. Gmail password is correct (the password you use to log into Gmail)
3. Try enabling "less secure apps": https://myaccount.google.com/lesssecureapps

**If still failing:**
- Go to https://myaccount.google.com/security
- Enable 2-Factor Authentication
- Then generate app-specific password at: https://myaccount.google.com/apppasswords
- Use the app password instead

### Error: "Invalid API key for OpenAI"

**Check**:
1. Key starts with "sk-"
2. Copy the ENTIRE key (no missing characters)
3. Not expired or revoked at: https://platform.openai.com/api-keys
4. Has available credits: https://platform.openai.com/account/billing/overview

### Error: "NewsAPI key not valid"

**Check**:
1. You copied the full key
2. Account is verified at: https://newsapi.org/account
3. Try generating a new key

### Python/Setup Issues

Make sure Python is installed:
1. Open Command Prompt
2. Type: `python --version`
3. Should show version like `Python 3.9.0`

If not installed, get it from: https://www.python.org/downloads/

### Email Won't Send

Check these in order:
1. Internet connection working
2. Gmail credentials correct in `.env`
3. Try waiting 30 seconds (sometimes Gmail rate limits)
4. Try again with new app password

### Script Runs but No Email

1. Check junk/spam folder in Gmail
2. Verify recipient email in `.env` is correct
3. Check console output for error messages

## EMAIL CONTENTS EXPLAINED

Each email includes:

| Section | What It Is |
|---------|-----------|
| **Market Snapshot** | What moved in last 24 hours - bonds, stocks, forex, commodities |
| **Recent Context** | How today fits into the last week/month of market moves |
| **Near-Term Outlook** | What's likely to happen next 1-4 weeks with key dates |
| **Long-Term View** | 3-12 month outlook - big structural themes |
| **Author's Conviction** | The AI's bold take on what matters most right now |
| **Proposed Trade** | Specific actionable trade with entry, exit, stop loss, targets |

## COSTS

Running daily:
- **OpenAI**: ~$30-90/month (about $1-3 per run)
- **NewsAPI**: Free (100 requests/day limit)
- **Gmail**: Free
- **Total**: ~$30-90/month if run every day

You can reduce costs by:
- Running less frequently (3x per week instead of daily)
- Using simpler model (gpt-3.5-turbo instead of gpt-4)
- Reducing analysis depth in config.ini

## SUPPORT

- **OpenAI Issues**: https://help.openai.com/
- **NewsAPI Issues**: https://newsapi.org/docs
- **Gmail Issues**: https://support.google.com/mail/

## SUCCESS INDICATORS

✓ Script runs without errors
✓ Email appears in inbox
✓ Email contains today's date
✓ Email has market analysis and trade idea
✓ Task runs automatically if scheduled

---

**That's it!** You now have a sophisticated market intelligence system running.

For questions about how it works, see `README.md`
For code details, see `main.py` comments
