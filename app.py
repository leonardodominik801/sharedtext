#!/usr/bin/env python
"""shared-text: Read-time file editing."""

import flask
import os

FILE = "file.txt"
TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>shared text</title><head>
<body>

<h1>shared text</h1>

<form action="/" method="POST">
  <p><label for="sharedtext"><code>file.txt</code></label></p>
  <textarea id="sharedtext" name="sharedtext" rows="4" cols="50">{{ text }}</textarea>
  <br>
  <input type="submit" value="Save">
</form>

<p>Click the "Save" button to save your changes.</p>

<p>All code is in a small program <code>app.py</code> and a text file <code>file.txt</code></p>

<p><a href="/app.py">View</a> or <a href="/app.py" download>download</a> the code</p>

</body>
</html>
'''

app = flask.Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if flask.request.method == "POST":
        # Save file
        new_text = flask.request.form.get("sharedtext")
        if new_text != read_file():
            write_file(new_text)
        return flask.redirect(flask.url_for("index"))
    elif flask.request.method == "GET":
        return flask.render_template_string(TEMPLATE, text = read_file())


@app.route("/app.py")
def code():
    return flask.Response(open(os.path.abspath(__file__)).read(),
                          mimetype="text/plain")

def read_file():
    with open(FILE) as f:
        data = f.read()
    return data

def write_file(text):
    with open(FILE, 'w') as f:
        f.write(text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)