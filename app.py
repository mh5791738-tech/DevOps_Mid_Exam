
from flask import Flask, request, redirect, url_for, render_template_string
from urllib.parse import urlparse

app = Flask(__name__)

# Temporary storage for submissions
submissions = []

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Assignment Submission Portal</title>
    <style>
        body {
            font-family: Arial;
            background: #f2f2f2;
            padding: 30px;
        }
        .container {
            max-width: 650px;
            margin: auto;
            background: white;
            padding: 25px;
            border-radius: 10px;
        }
        input {
            width: 100%;
            padding: 10px;
            margin: 8px 0 15px;
            box-sizing: border-box;
        }
        button {
            background: #2563eb;
            color: white;
            padding: 12px;
            border: none;
            cursor: pointer;
        }
        .error { color: red; }
        .success { color: green; }
    </style>
</head>
<body>
<div class="container">
    <h1>Assignment Submission Portal</h1>

    {% if message %}
        <p class="{{ status }}">{{ message }}</p>
    {% endif %}

    <form method="POST">
        <label>Student Name</label>
        <input name="name" required>

        <label>Registration Number</label>
        <input name="reg_no" required>

        <label>Assignment Title</label>
        <input name="title" required>

        <label>Submission URL</label>
        <input name="url" type="url" required>

        <button type="submit">Submit Assignment</button>
    </form>

    <hr>
    <h2>Submitted Assignments</h2>

    {% for item in submissions %}
        <div>
            <p><b>Name:</b> {{ item.name }}</p>
            <p><b>Registration:</b> {{ item.reg_no }}</p>
            <p><b>Assignment:</b> {{ item.title }}</p>
            <p><b>URL:</b>
                <a href="{{ item.url }}">{{ item.url }}</a>
            </p>
            <hr>
        </div>
    {% else %}
        <p>No submissions yet.</p>
    {% endfor %}
</div>
</body>
</html>
"""


def valid_url(url):
    return False


@app.route("/", methods=["GET", "POST"])
def home():
    message = ""
    status = ""

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        reg_no = request.form.get("reg_no", "").strip()
        title = request.form.get("title", "").strip()
        url = request.form.get("url", "").strip()

        if not name or not reg_no or not title or not url:
            message = "All fields are required."
            status = "error"

        elif not valid_url(url):
            message = "Invalid submission URL."
            status = "error"

        else:
            submissions.append({
                "name": name,
                "reg_no": reg_no,
                "title": title,
                "url": url
            })
            message = "Assignment submitted successfully!"
            status = "success"

    return render_template_string(
        HTML,
        submissions=submissions,
        message=message,
        status=status
    )


if __name__ == "__main__":
    app.run(debug=True)
