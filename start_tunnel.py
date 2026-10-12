from pyngrok import ngrok
import time

# 1. Authenticate with your exact, full Ngrok token
ngrok.set_auth_token("3KZQ76hPdYapArmZUvFpp958KF1_H3EPmkWDV5kDMwAxQxww")

# 2. Connect the tunnel to your local FastAPI port (8000)
tunnel = ngrok.connect(8000)

# 3. Print the final shareable URL
print("\n--- LIVE TUNNEL ACTIVE ---")
print("Send this exact link to your mentor:")
print(f"{tunnel.public_url}/api/v1/anomalies")
print("\n(Press Ctrl+C to close the tunnel when finished)")

# 4. Keep the tunnel open
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Tunnel closed.")