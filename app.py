import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":

        prompt = request.form["prompt"]
        job = request.form["job"]
        resume = request.form["resume"]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You're an expert career coach."},
                {"role": "user", "content": generate_full_prompt(prompt, job, resume)}
            ],
            temperature=1, # configure how random the outputs will be (0 - predictive, 2 - random)
        )

        return redirect(url_for("index", result=response.choices[0].message.content))

    result = request.args.get("result")
    if result:
        result = result.replace('\n', '<br/>')
    
    return render_template("index.html", result=result)


def generate_full_prompt(prompt, job, resume):
    return f"""{prompt} \
            Here is a job description: "{job}" \
            Here is a resume: "{resume}"
            """
