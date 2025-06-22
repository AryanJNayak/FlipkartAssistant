from pyngrok import ngrok
import os
import subprocess
import time
from dotenv import load_dotenv

load_dotenv()
# Set auth token and expose port 8501
ngrok.set_auth_token(os.getenv("NGROK_TOKEN"))
public_url = ngrok.connect(8501)
print("🔗 Public URL:", public_url)

# Start Streamlit app using subprocess
print("🚀 Starting Streamlit...")
process = subprocess.Popen(["streamlit", "run", "app.py"])

# Keep the notebook alive
try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    print("🛑 Stopping app...")
    process.terminate()
    ngrok.disconnect(public_url)