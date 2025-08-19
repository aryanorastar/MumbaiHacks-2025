# 🔑 API Setup Guide for Arogya Sentinel

## Required API Keys

### 1. OpenAI API Key (REQUIRED)
- **Get from**: https://platform.openai.com/account/api-keys
- **Cost**: Pay-per-use (GPT-4 recommended)
- **Setup**: Replace `YOUR_OPENAI_API_KEY_HERE` in main.py line 14

### 2. Google Maps API Key (OPTIONAL - Enhanced Air Quality)
- **Get from**: https://console.cloud.google.com/
- **Enable**: Air Quality API
- **Cost**: Free tier available (500 requests/day)
- **Setup**: Replace `YOUR_GOOGLE_MAPS_API_KEY_HERE` in main.py line 15

## Free APIs (No Key Required)

### 3. Nager.Date API
- **Purpose**: Festival and public holiday data
- **Cost**: Completely free
- **Docs**: https://date.nager.at/

### 4. World Air Quality Index API
- **Purpose**: Free air quality data (fallback)
- **Cost**: Free tier (1000 requests/day)
- **Get token**: https://aqicn.org/api/
- **Note**: Uses 'demo' token by default

### 5. India Open Data Platform
- **Purpose**: Public health data
- **Cost**: Free for most datasets
- **Docs**: https://data.gov.in/
- **Note**: Some datasets may require registration

## Quick Setup

1. **Copy the API keys**:
   ```bash
   # Edit main.py lines 14-15
   os.environ["OPENAI_API_KEY"] = "your_actual_openai_key"
   os.environ["GOOGLE_MAPS_API_KEY"] = "your_actual_google_key"  # Optional
   ```

2. **Install dependencies**:
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the system**:
   ```bash
   python main.py
   ```

## API Fallbacks

The system is designed to be resilient:
- If APIs fail, it uses realistic fallback data
- Multiple data sources for air quality
- Graceful error handling for all integrations
- Perfect for hackathon demonstrations even with limited API access

## Production Notes

For production deployment:
- Use environment variables for API keys
- Implement proper rate limiting
- Add API response caching
- Monitor API usage and costs