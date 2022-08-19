from flask import Flask
app = Flask(__name__)

# These routes are for mock tests with the nginx proxy

@app.route("/photo/<acct>")
def propertybase(acct=''):
    return f"Property base {acct}"

@app.route("/photos/<photo>")
def photos(photo=''):
    return "photos %s" % photo

@app.route("/precincts/<precinct>")
def precincts(precinct=''):
    return "precinct %s" % precinct

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
