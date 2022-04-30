from flask import Flask, request                                                                                                                           
  
import deseret

app = Flask(__name__)
app.config["DEBUG"] = False

page_html = '''
<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" href="/static/style.css">
    <title>Deseret Alphabet Translator</title>
  </head>
  <body><body>
    <div class="login-page">
      <div class="form">
        <div class="login-header">
          <h3>Deseret Alphabet Translator</h3>
          <p>Enter text in the Latin alphabet:</p>
        </div>
      <textarea class="input" rows="4" cols="28" name="latin_text" form="latin_input_form">{latin_text}</textarea>
      <form method="post" action"." class="login-form" id="latin_input_form">
                <p><input class="button" type="submit" size="" value="Convert to Deseret" /></p>
      </form>
      <div class="login-header">
        <p class="message">{latin_text}</p>
        <br/>
        <p class="message">{deseret_text}</p>
      </div>
      <div class="login-header">
        <p>{errors}</p>
      </div>
      </div>
    </div>
  </body></body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def adder_page():
    errors = ""
    latin_text = "Enter your text here..."
    deseret_text = ""
    if request.method == "POST":
        latin_text = None
        try:
            latin_text = str(request.form["latin_text"])
            print(latin_text)
        except:
            errors += "<p>{!r} cannot be loaded.</p>\n".format(request.form["latin_text"])
        if latin_text != "Enter your text here...":
            try:
                deseret_text = deseret.latin2des(latin_text)
            except KeyError as e:
                errors += "<p>Could not locate the word {errors} in the source dictionary.</p>".format(errors=e)
            print(deseret_text)
    return page_html.format(errors=errors, deseret_text=deseret_text, latin_text=latin_text)
