import requests
import time
import subprocess
import sys

def test_service():
    # Start the FastAPI server in the background
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd="."
    )
    time.sleep(3)  # Wait for the server to start

    base_url = "http://127.0.0.1:8000"
    test_email = "test@example.com"
    test_password = "securepassword123"

    try:
        print("\n--- Testing Registration ---")
        reg_resp = requests.post(f"{base_url}/register", json={"email": test_email, "password": test_password})
        print(f"Status: {reg_resp.status_code}, Response: {reg_resp.json()}")

        print("\n--- Testing Login ---")
        login_resp = requests.post(f"{base_url}/login", data={"username": test_email, "password": test_password})
        print(f"Status: {login_resp.status_code}")
        token = login_resp.json().get("access_token")
        print(f"Token: {token[:20]}...")

        print("\n--- Testing Protected Route (/users/me) ---")
        me_resp = requests.get(f"{base_url}/users/me", headers={"Authorization": f"Bearer {token}"})
        print(f"Status: {me_resp.status_code}, Response: {me_resp.json()}")

        print("\n--- Testing Forgot Password ---")
        forgot_resp = requests.post(f"{base_url}/forgot-password", json={"email": test_email})
        print(f"Status: {forgot_resp.status_code}, Response: {forgot_resp.json()}")

    finally:
        process.terminate()
        process.wait()

if __name__ == "__main__":
    test_service()
