import base64
import mimetypes
import os
import io
from PIL import Image
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')

class ImageProcessor:
    def __init__(self):
        self.client = genai.Client(
            api_key=os.environ.get("GEMINI_API_KEY"),
        )
        self.model = "gemini-2.5-flash-image-preview"
        
    def encode_image_to_base64(self, image_path):
        """Convert image file to base64 string"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def save_binary_file(self, file_name, data):
        """Save binary data to file"""
        with open(file_name, "wb") as f:
            f.write(data)
        print(f"File saved to: {file_name}")
    
    def process_image(self, user_image_path, sample_image_path="./sample/image.png"):
        """
        Process user image using Gemini API with sample image as reference
        
        Args:
            user_image_path: Path to the user's uploaded image
            sample_image_path: Path to the sample image (default: ./image.png)
        
        Returns:
            Path to the processed image or None if failed
        """
        try:
            print(f"Processing image: {user_image_path}")
            print(f"Using sample image: {sample_image_path}")
            
            # Check if sample image exists
            if not os.path.exists(sample_image_path):
                print(f"Sample image not found: {sample_image_path}")
                return None
            
            # Encode both images to base64
            sample_image_b64 = self.encode_image_to_base64(sample_image_path)
            user_image_b64 = self.encode_image_to_base64(user_image_path)
            print("Images encoded to base64 successfully")
            
            # Create the prompt for image correction
            prompt = """
            Given a user-uploaded photo, resize and correct it into a standard passport/ID photo format with:

            White background (clean, uniform).
            Face centered and scaled to fit the frame.
            Image size: 600x600 pixels.
            Proper brightness and contrast so the face is clearly visible.
            Crop extra background while keeping the head and shoulders visible to the point as shown in the reference image no more.
            Ensure the output is a sharp, high-quality image in JPEG or PNG format.

            Use the first image as a reference sample and correct the second image accordingly.
            """
            
            # Prepare content with both images
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_bytes(
                            mime_type="image/png",
                            data=base64.b64decode(sample_image_b64)
                        ),
                        types.Part.from_bytes(
                            mime_type="image/jpeg",
                            data=base64.b64decode(user_image_b64)
                        ),
                        types.Part.from_text(text=prompt),
                    ],
                ),
            ]
            
            # Configure generation
            generate_content_config = types.GenerateContentConfig(
                response_modalities=["IMAGE"],
            )
            
            # Generate processed image
            print("Sending request to Gemini API...")
            file_index = 0
            output_path = None
            
            for chunk in self.client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=generate_content_config,
            ):
                if (
                    chunk.candidates is None
                    or chunk.candidates[0].content is None
                    or chunk.candidates[0].content.parts is None
                ):
                    continue
                    
                if (chunk.candidates[0].content.parts[0].inline_data and 
                    chunk.candidates[0].content.parts[0].inline_data.data):
                    
                    file_name = f"processed_image_{file_index}"
                    file_index += 1
                    inline_data = chunk.candidates[0].content.parts[0].inline_data
                    data_buffer = inline_data.data
                    file_extension = mimetypes.guess_extension(inline_data.mime_type)
                    
                    if file_extension is None:
                        file_extension = ".png"
                    
                    output_path = f"{file_name}{file_extension}"
                    self.save_binary_file(output_path, data_buffer)
                    
                    # Resize the processed image to 600x600 pixels
                    resized_path = self.resize_image_to_600x600(output_path)
                    if resized_path:
                        # Remove the original file and use the resized one
                        if os.path.exists(output_path):
                            os.remove(output_path)
                        output_path = resized_path
                    
                    break
            
            return output_path
            
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def resize_image_to_600x600(self, image_path):
        """
        Resize image to exactly 600x600 pixels while maintaining aspect ratio
        
        Args:
            image_path: Path to the image file to resize
            
        Returns:
            Path to the resized image or None if failed
        """
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if necessary (handles RGBA, P mode, etc.)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize to 600x600 using high-quality resampling
                resized_img = img.resize((600, 600), Image.Resampling.LANCZOS)
                
                # Create new filename with _600x600 suffix
                base_name, ext = os.path.splitext(image_path)
                resized_path = f"{base_name}_600x600.png"
                
                # Save as PNG (lossless)
                resized_img.save(resized_path, 'PNG')
                
                print(f"Image resized to 600x600: {resized_path}")
                return resized_path
                
        except Exception as e:
            print(f"Error resizing image: {str(e)}")
            return None
    
    def validate_image(self, image_path):
        """Validate if the uploaded file is a valid image"""
        try:
            with Image.open(image_path) as img:
                img.verify()
            return True
        except Exception:
            return False

# Example usage
if __name__ == "__main__":
    processor = ImageProcessor()
    
    # Test with a sample image (you'll need to provide a test image)
    # result = processor.process_image("test_user_image.jpg")
    # if result:
    #     print(f"Image processed successfully: {result}")
    # else:
    #     print("Image processing failed")
