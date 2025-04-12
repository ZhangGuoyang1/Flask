from flask import Flask, request, render_template_string
import wikipedia

app = Flask(__name__)


@app.route('/')
def hello():
    return '<h1>Hello World :)</h1>'


@app.route('/greet')
@app.route('/greet/<name>')
def greet(name=""):
    if name:
        return f"Hello {name}"
    else:
        return "Hello"


def celsius_to_fahrenheit(c):
    return c * 9.0 / 5.0 + 32


@app.route('/convert/<celsius>')
def convert(celsius):
    try:
        c = float(celsius)
        f = celsius_to_fahrenheit(c)
        return f"{c}° Celsius is equal to {f:.2f}° Fahrenheit"
    except ValueError:
        return "Invalid input. Please enter a valid number."

@app.route('/wiki', methods=['GET', 'POST'])
def wiki_search():
    if request.method == "POST":
        title = request.form.get("title", "")
        try:
            page = wikipedia.page(title, auto_suggest=False)
        except wikipedia.exceptions.DisambiguationError as e:
            suggestions = e.options
            return render_template_string(
                "<h2>Ambiguous title, please be more specific.</h2><p>{{ suggestions }}</p>",
                suggestions=suggestions)
        except wikipedia.exceptions.PageError:
            return "Page not found. Try a different title."
        except Exception as ex:
            return f"An error occurred: {str(ex)}"
        return render_template_string("""
            <h1>{{ title }}</h1>
            <p>{{ summary }}</p>
            <a href="{{ url }}">Read more</a>
            """, title=page.title, summary=wikipedia.summary(title, sentences=3), url=page.url)
    return '''
        <form method="post">
            Wikipedia Page Title: <input type="text" name="title">
            <input type="submit" value="Search">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
