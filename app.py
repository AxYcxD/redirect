from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Authorization Complete</title>
  <style>
    body {
      background-color: #0e0e0e;
      color: #ffffff;
      font-family: Arial, sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
      text-align: center;
    }
    .box {
      background: #1c1c1c;
      padding: 30px;
      border-radius: 12px;
      box-shadow: 0 0 20px #00ffff50;
    }
    h1 {
      color: #00ffff;
    }
  </style>
</head>
<body>
  <div class="box">
    <h1>✅ Authorization Complete</h1>
    <p>You’ve successfully verified. You may now close this window.</p>
    {% if code %}
      <p><strong>OAuth2 Code:</strong> {{ code }}</p>
    {% endif %}
  </div>
</body>
</html>
"""

@app.route("/")
def home():
    # Optional: Show the 'code' param if present (from Discord redirect)
    code = request.args.get("code")
    return render_template_string(HTML_PAGE, code=code)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
