import json
from dotenv import dotenv_values
from flask import Flask, render_template, request
from openai import OpenAI 

config = dotenv_values(".env")
client = OpenAI(api_key=config["APIKEY"])  

app = Flask(
    __name__, template_folder="templates", static_url_path="", static_folder="static"
)


def get_colors(msg):
    response = client.chat.completions.create(
        model="gpt-4.1-nano",  
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a JSON-only color palette generator. "
                    "Respond only with a valid JSON array of 2 to 8 hex color codes like "
                    "[\"#000000\", \"#ffffff\"]. No explanation."
                )
            },
            {"role": "user", "content": msg}
        ],
        max_tokens=100,
        temperature=0.3
    )

    raw = response.choices[0].message.content.strip()
    return json.loads(raw)  


@app.route("/palette", methods=["POST"])
def prompt_to_palette():
    query = request.form.get("query")
    colors = get_colors(query)
    return {"colors": colors}


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
