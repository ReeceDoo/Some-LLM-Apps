import os

def main():
    api_key = os.getenv('API_KEY')
    if api_key:
        print(f"Your API key is: {api_key}")
    else:
        print("API key not found. Make sure it's set correctly.")

if __name__ == "__main__":
    main()
