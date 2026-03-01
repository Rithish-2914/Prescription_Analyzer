import requests
import time
import os

API_URL = "http://127.0.0.1:8000/explain"

def test_text_endpoint():
    print("--- Testing Text Endpoint ---")
    payload = {"prescription_text": "Tab Amoxicillin 500mg TDS × 7 days PC"}
    try:
        response = requests.post(API_URL, data=payload)
        print(f"Status: {response.status_code}")
        print(response.json())
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_image_endpoint(image_path):
    print("\n--- Testing Image Endpoint ---")
    if not os.path.exists(image_path):
        print(f"Image {image_path} not found.")
        return False
        
    try:
        with open(image_path, "rb") as f:
            files = {"file": ("test_img.png", f, "image/png")}
            response = requests.post(API_URL, files=files)
            print(f"Status: {response.status_code}")
            print(response.json())
            return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    test_text_endpoint()
    
    # We will test the generated image path next
    image_path = os.path.join(os.getenv("LOCALAPPDATA", r"C:\Users\ACER\AppData\Local"), 
        ".gemini", "antigravity", "artifacts", "prescription_test.png")
    # Actually, the user's artifact dir is C:\Users\ACER\.gemini\antigravity\brain\df4a82fe-ec7d-4557-afbe-6a25e95387dd
    # We will pass the path directly or adjust based on generate_image output
