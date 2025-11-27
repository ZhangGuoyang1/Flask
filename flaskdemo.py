from flask import Flask, render_template, request
import wikipedia

app = Flask(__name__)
app.secret_key = "abc123"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    page = None
    error = None
    options = None

    if request.method == "POST":
        query = request.form["search"]

        try:
            page = wikipedia.page(query, autosuggest=False)
        except wikipedia.DisambiguationError as e:
            options = e.options
        except wikipedia.PageError:
            error = f"Page '{query}' not found. Try another title."

    return render_template("results.html", page=page, error=error, options=options)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
