  from flask import Flask, request                                                                                                                                                                                                                                                                                         
  
  import deseret
  
  app = Flask(__name__)
  app.config["DEBUG"] = True
  
  @app.route("/", methods=["GET", "POST"])
  def adder_page():
      errors = ""
      if request.method == "POST":
          latin_text = None
          try:
              latin_text = str(request.form["latin_text"])
              print(latin_text)
          except:
              errors += "<p>{!r} cannot be loaded.</p>\n".format(request.form["latin_text"])
          if latin_text is not None:
              print('here')
              deseret_text = deseret.latin2des(latin_text)
              print(deseret_text)
              return '''
                  <html>
                      <body>
                          <form method="post" action".">
                              <p><input name="latin_text" /></p>
                              <p><input type="submit" value="To Deseret→" /></p> 
                          </form>
                          <p>{deseret_text}</p>
                      </body>
                  </html>
              '''.format(deseret_text=deseret_text)
  
      return '''
          <html>
              <body>
                  {errors}
                  <form method="post" action=".">
                      <p><input name="latin_text" /></p>
                      <p><input type="submit" value="To Deseret→" /></p>
                  </form>
              </body>
          </html>
      '''.format(errors=errors)
