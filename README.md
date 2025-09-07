# DV Lottery Photo Corrector Bot

A Telegram bot that automatically corrects portrait photos for DV lottery applications using Google's Gemini AI.

## Features

- 🎯 Automatically corrects portrait photos to meet DV lottery requirements
- 🤖 Uses Google Gemini AI for intelligent image processing
- 📱 Simple Telegram interface
- ✅ Ensures photos have:
  - White background
  - Face centered and properly scaled
  - 600x600 pixel dimensions
  - Proper brightness and contrast
  - Head and shoulders visible

## Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (from @BotFather)
- Google Gemini API Key
- Sample reference image (`image.png`)

## Installation

### Step 1: Clone or Download the Project

```bash
# If using git
git clone <your-repo-url>
cd dv-lottery-bot

# Or simply download the files to a folder
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Set Up Environment Variables

1. Copy the example configuration file:
   ```bash
   copy config.env.example config.env
   ```

2. Edit `config.env` file with your API keys:
   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

### Step 4: Get API Keys

#### Telegram Bot Token:
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the bot token and add it to your `.env` file

#### Gemini API Key:
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Create a new project or use existing one
3. Generate an API key
4. Copy the API key and add it to your `.env` file

### Step 5: Prepare Sample Image

1. Place your reference image as `image.png` in the `sample/` directory
2. This image will be used as a sample for the AI to understand the desired output format

## Usage

### Running the Bot

```bash
python telegram_bot.py
```

The bot will start and you should see:
```
Starting DV Lottery Photo Corrector Bot...
```

### Using the Bot

1. Open Telegram and search for your bot
2. Send `/start` to begin
3. Send a portrait photo
4. Wait for processing (10-30 seconds)
5. Receive your corrected photo

### Bot Commands

- `/start` - Start the bot and see welcome message
- `/help` - Show help and instructions
- `/status` - Check bot status

## File Structure

```
dv-lottery-bot/
├── telegram_bot.py          # Main bot script
├── image_processor.py        # Image processing module
├── requirements.txt          # Python dependencies
├── config.env.example       # Environment variables template
├── config.env               # Your actual environment variables (not in git)
├── sample/                  # Sample images directory
│   └── image.png            # Reference image for AI processing
├── .gitignore              # Git ignore rules
└── README.md                # This file
```

## How It Works

1. **User sends photo** via Telegram
2. **Bot downloads** the image temporarily
3. **Image validation** checks if it's a valid image file
4. **Gemini AI processes** the image using the sample reference
5. **AI corrects** the image according to DV lottery requirements
6. **Bot sends back** the processed image
7. **Cleanup** removes temporary files

## Troubleshooting

### Common Issues

1. **"TELEGRAM_BOT_TOKEN not found"**
   - Check your `.env` file exists and contains the correct token
   - Make sure there are no extra spaces or quotes around the token

2. **"Invalid image format"**
   - Ensure you're sending actual image files (JPG, PNG, etc.)
   - Try with a different image

3. **"Failed to process image"**
   - Check your Gemini API key is valid
   - Ensure you have internet connection
   - Try with a clearer, well-lit photo

4. **Bot not responding**
   - Check if the bot is running in terminal
   - Verify the bot token is correct
   - Make sure the bot is not blocked

### Logs

The bot logs all activities. Check the terminal output for detailed error messages.

## API Costs

- **Telegram Bot API**: Free
- **Google Gemini API**: Pay-per-use (check current pricing)

## Security Notes

- Never share your API keys
- Keep your `.env` file private
- The bot only processes images temporarily and deletes them after processing

## Support

If you encounter issues:
1. Check the troubleshooting section
2. Verify your API keys are correct
3. Ensure all dependencies are installed
4. Check your internet connection

## License

This project is for educational and personal use. Please respect the terms of service of Telegram and Google Gemini API.
