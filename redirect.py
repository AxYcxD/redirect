from flask import Flask, request, redirect, session, render_template_string
import requests
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Replace with fixed string if needed

# Replace these or set them as environment variables
CLIENT_ID = os.getenv("CLIENT_ID", "YOUR_DISCORD_CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "YOUR_DISCORD_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI", "https://yourdomain.com/callback")

DISCORD_API_ENDPOINT = "https://discord.com/api"

HTML_TEMPLATE = """
<html>
<head><title>Discord OAuth2</title></head>
<body>
  {% if user %}
    <h2>✅ Logged in as {{ user['username'] }}#{{ user['discriminator'] }}</h2>
    <p><strong>User ID:</strong> {{ user['id'] }}</p>
    <p><strong>Your IP:</strong> {{ ip }}</p>
  {% else %}
    <a href="/login"><button>Login with Discord</button></a>
  {% endif %}
</body>
</html>
"""

@app.route("/")
def index():
    user = session.get("user")
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    return render_template_string(HTML_TEMPLATE, user=user, ip=ip)

@app.route("/login")
def login():
    return redirect(
        f"{DISCORD_API_ENDPOINT}/oauth2/authorize?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify"
    )

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Error: no code provided by Discord."

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "scope": "identify"
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(f"{DISCORD_API_ENDPOINT}/oauth2/token", data=data, headers=headers)
    response.raise_for_status()

    access_token = response.json().get("access_token")
    user_info = requests.get(
        f"{DISCORD_API_ENDPOINT}/users/@me",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    session["user"] = user_info
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
