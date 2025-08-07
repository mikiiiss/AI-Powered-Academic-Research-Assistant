from fastapi import FastAPI
import requests
import socket

app = FastAPI()

def check_connection():
    try:
        # Verify DNS resolution first
        socket.gethostbyname('arxiv.org')
        
        # Try both HTTP and HTTPS
        for protocol in ['https', 'http']:
            try:
                url = f"{protocol}://arxiv.org"
                response = requests.get(
                    url,
                    headers=ARXIV_HEADERS,
                    timeout=10,
                    allow_redirects=True
                )
                return {
                    "reachable": True,
                    "protocol": protocol,
                    "status": response.status_code
                }
            except:
                continue
                
        return {"reachable": False}
        
    except socket.gaierror:
        return {"error": "DNS resolution failed"}

@app.get("/test-connection")
async def test_connection():
    return check_connection()