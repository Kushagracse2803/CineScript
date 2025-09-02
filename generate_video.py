import time
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import datetime

load_dotenv()

gemini_key = os.getenv("GEMINI_KEY")
if not gemini_key:
    raise ValueError("GEMINI_KEY not found in environment variables")

client = genai.Client(api_key=gemini_key)

def generate_video_from_prompt(prompt_text):
    print(f"Attempting to generate video for prompt: '{prompt_text}'")
    try:
        operation = client.models.generate_videos(
            model="veo-3.0-generate-preview",
            prompt=prompt_text,
            config=types.GenerateVideosConfig(
                negative_prompt="cartoon, drawing, low quality",
                aspect_ratio="16:9",  # Check Veo API docs for supported aspect ratios
            ),
        )

        max_retries = 60  # Max 10 minutes (60 * 10 seconds)
        retries = 0
        while not operation.done and retries < max_retries:
            print(f"Waiting for video generation to complete... (Attempt {retries + 1}/{max_retries})")
            time.sleep(10)
            operation = client.operations.get(operation)
            retries += 1

        if operation.done:
            if operation.response and operation.response.generated_videos:
                generated_video = operation.response.generated_videos[0]
                
                # Generate a unique filename in Videos folder
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                os.makedirs("Videos", exist_ok=True)  # Ensure folder exists
                filename = f"Videos/generated_video_{timestamp}.mp4"

                print(f"Video generation complete. Downloading to {filename}...")
                try:
                    client.files.download(file=generated_video.video)
                    generated_video.video.save(filename)
                    print(f"Video saved as {filename}")
                except Exception as e:
                    print(f"Error downloading or saving video: {e}")
            else:
                print("Video generation completed, but no video found in the response.")
                if operation.error:
                    print(f"API Error: {operation.error.message}")
        else:
            print(f"Video generation timed out after {max_retries * 10} seconds.")
            if operation.error:
                print(f"API Error during timeout: {operation.error.message}")

    except Exception as e:
        print(f"An error occurred during video generation: {e}")
