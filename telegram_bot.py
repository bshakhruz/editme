import os
import logging
import tempfile
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from image_processor import ImageProcessor

# Load environment variables
load_dotenv('config.env')

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class DVPhotoBot:
    def __init__(self):
        self.token = os.environ.get("TELEGRAM_BOT_TOKEN")
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")
        
        self.image_processor = ImageProcessor()
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send a message when the command /start is issued."""
        welcome_message = """
🎯 Welcome to DV Lottery Photo Corrector Bot!

I can help you correct your portrait photos for DV lottery applications.

📋 Instructions:
1. Send me a portrait photo of yourself
2. I'll process it to meet DV lottery requirements:
   • White background
   • Face centered and properly scaled
   • 600x600 pixels
   • Proper brightness and contrast
   • Head and shoulders visible

📸 Just send your photo and I'll process it for you!

Use /help for more information.
        """
        await update.message.reply_text(welcome_message)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send a message when the command /help is issued."""
        help_message = """
🆘 Help - DV Lottery Photo Corrector Bot

📸 How to use:
1. Send a clear portrait photo of yourself
2. Wait for processing (usually takes 10-30 seconds)
3. Receive your corrected photo ready for DV lottery

✅ Photo requirements:
• Clear, well-lit portrait
• Face should be clearly visible
• Avoid sunglasses or hats
• Good quality image

❌ What I'll fix:
• Add white background
• Center and scale your face
• Adjust brightness and contrast
• Crop to proper dimensions
• Ensure high quality output

Commands:
/start - Start the bot
/help - Show this help message
/status - Check bot status
/sample - View sample DV lottery photo
/requirements - View detailed photo requirements

Just send your photo to get started!
        """
        await update.message.reply_text(help_message)
    
    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Check bot status"""
        status_message = """
🤖 Bot Status: Online ✅

Services:
• Image Processing: Active
• Gemini API: Connected
• Sample Image: Available

Ready to process your photos!
        """
        await update.message.reply_text(status_message)
    
    async def sample_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send sample image"""
        try:
            sample_image_path = "./image.png"
            if os.path.exists(sample_image_path):
                with open(sample_image_path, 'rb') as sample_file:
                    await update.message.reply_photo(
                        photo=sample_file,
                        caption="📸 Sample DV Lottery Photo\n\nThis is an example of how your photo should look after processing:\n• White background\n• Face centered and properly scaled\n• 600x600 pixels\n• Clear and professional appearance"
                    )
            else:
                await update.message.reply_text("❌ Sample image not found. Please contact the administrator.")
        except Exception as e:
            logger.error(f"Error sending sample image: {str(e)}")
            await update.message.reply_text("❌ Error loading sample image. Please try again later.")
    
    async def requirements_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show DV lottery photo requirements"""
        requirements_message = """
📋 DV Lottery Photo Requirements

✅ REQUIRED SPECIFICATIONS:
• Size: 600 x 600 pixels
• Format: JPEG or PNG
• Background: Plain white or off-white
• Face: Centered, looking directly at camera
• Expression: Neutral (no smiling, frowning, or raised eyebrows)
• Eyes: Open and clearly visible
• Head: 22mm to 35mm from chin to top of head
• Shoulders: Visible in the photo

❌ NOT ALLOWED:
• Sunglasses or tinted glasses
• Hats or head coverings (except religious)
• Shadows on face or background
• Red-eye effect
• Blurry or low-quality images
• Other people in the photo
• Filters or digital alterations

📸 TIPS FOR BEST RESULTS:
• Use good lighting (natural light preferred)
• Take photo against white wall or background
• Look directly at camera
• Keep neutral expression
• Ensure face is well-lit and clear

Send me your photo and I'll process it to meet these requirements!
        """
        await update.message.reply_text(requirements_message)
    
    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming photos"""
        try:
            # Send processing message
            processing_msg = await update.message.reply_text("🔄 Processing your photo... Please wait!")
            
            # Get the highest quality photo
            photo = update.message.photo[-1]
            
            # Download the photo
            file = await context.bot.get_file(photo.file_id)
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                await file.download_to_drive(temp_file.name)
                temp_path = temp_file.name
            
            try:
                # Validate image
                if not self.image_processor.validate_image(temp_path):
                    await processing_msg.edit_text("❌ Invalid image format. Please send a valid photo.")
                    return
                
                # Process the image
                processed_path = self.image_processor.process_image(temp_path)
                
                if processed_path and os.path.exists(processed_path):
                    # Send the processed image as a file
                    with open(processed_path, 'rb') as processed_file:
                        await processing_msg.edit_text("✅ Photo processed successfully!")
                        await update.message.reply_document(
                            document=processed_file,
                            filename="dv_lottery_photo_600x600.png",
                            caption="🎯 Your DV lottery photo is ready!\n\nThis photo meets all DV lottery requirements:\n• White background\n• Proper dimensions (600x600)\n• Centered face\n• Optimal brightness and contrast\n• Lossless PNG format"
                        )
                    
                    # Clean up processed file
                    os.unlink(processed_path)
                else:
                    await processing_msg.edit_text("❌ Failed to process image. Please try again with a different photo.")
            
            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    
        except Exception as e:
            logger.error(f"Error processing photo: {str(e)}")
            await update.message.reply_text("❌ An error occurred while processing your photo. Please try again.")
    
    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle document uploads (images sent as files)"""
        try:
            document = update.message.document
            
            # Check if it's an image
            if not document.mime_type or not document.mime_type.startswith('image/'):
                await update.message.reply_text("❌ Please send an image file (JPG, PNG, etc.)")
                return
            
            # Send processing message
            processing_msg = await update.message.reply_text("🔄 Processing your image... Please wait!")
            
            # Download the document
            file = await context.bot.get_file(document.file_id)
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{document.file_name.split(".")[-1]}') as temp_file:
                await file.download_to_drive(temp_file.name)
                temp_path = temp_file.name
            
            try:
                # Validate image
                if not self.image_processor.validate_image(temp_path):
                    await processing_msg.edit_text("❌ Invalid image format. Please send a valid image.")
                    return
                
                # Process the image
                processed_path = self.image_processor.process_image(temp_path)
                
                if processed_path and os.path.exists(processed_path):
                    # Send the processed image as a file
                    with open(processed_path, 'rb') as processed_file:
                        await processing_msg.edit_text("✅ Image processed successfully!")
                        await update.message.reply_document(
                            document=processed_file,
                            filename="dv_lottery_photo_600x600.png",
                            caption="🎯 Your DV lottery photo is ready!\n\nThis photo meets all DV lottery requirements:\n• White background\n• Proper dimensions (600x600)\n• Centered face\n• Optimal brightness and contrast\n• Lossless PNG format"
                        )
                    
                    # Clean up processed file
                    os.unlink(processed_path)
                else:
                    await processing_msg.edit_text("❌ Failed to process image. Please try again with a different image.")
            
            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            await update.message.reply_text("❌ An error occurred while processing your image. Please try again.")
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages"""
        await update.message.reply_text(
            "📸 Please send me a photo to process!\n\nUse /help for instructions."
        )
    
    def run(self):
        """Run the bot"""
        # Create application
        application = Application.builder().token(self.token).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("status", self.status))
        application.add_handler(CommandHandler("sample", self.sample_command))
        application.add_handler(CommandHandler("requirements", self.requirements_command))
        application.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))
        application.add_handler(MessageHandler(filters.Document.IMAGE, self.handle_document))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
        
        # Start the bot
        logger.info("Starting DV Lottery Photo Corrector Bot...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    try:
        bot = DVPhotoBot()
        bot.run()
    except Exception as e:
        logger.error(f"Failed to start bot: {str(e)}")
        print(f"Error: {str(e)}")
        print("Please check your API keys in config.env file")
