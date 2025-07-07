# 🚀 Setup Guide - Customize for Your Company

## Quick Setup

### 1. Configure Your Company Details

Edit the `config.py` file in the root directory:

```python
# Company Details
COMPANY_NAME = "Your Company Name"  # e.g., "TechCorp Solutions"
FOUNDER_NAME = "Your Name"          # e.g., "John Smith"
COMPANY_DESCRIPTION = "a leading technology consulting company"

# Portfolio Links (optional - leave empty to use AI-selected links)
PORTFOLIO_LINK_1 = "https://your-portfolio1.com"
PORTFOLIO_LINK_2 = "https://your-portfolio2.com"
```

### 2. Set Up Your API Key

Create a `.env` file in the `app` folder:
```
GROQ_API_KEY=your_groq_api_key_here
```

Get your free API key from: https://console.groq.com/keys

### 3. Customize Your Portfolio

Replace `my_portfolio.csv` with your own portfolio data:
- **Techstack**: Your skills/technologies
- **Links**: URLs to your portfolio projects

### 4. Run the Application

```bash
cd project-genai-cold-email-generator
streamlit run app/main.py
```

## Features

✅ **Generic Company Support** - No more hardcoded "AtliQ" or "Mohan"  
✅ **Easy Configuration** - Simple config file for company details  
✅ **Web Interface** - Company settings tab in the app  
✅ **Custom Portfolio Links** - Specify your own portfolio links for emails  
✅ **Professional Emails** - AI-generated personalized outreach  

## Customization Options

### Via Web Interface
1. Go to "Company Settings" tab
2. Fill in your company details
3. Click "Save Settings"

### Via Config File
Edit `config.py` for permanent changes:
- Company name and description
- Contact person name
- Portfolio links (optional)
- Email subject prefixes
- Portfolio file location

## Ready to Use!

Your Cold Email Generator is now personalized for your company and ready to generate professional outreach emails! 🎉 