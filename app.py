from src.get_data import read_config_data
import os
from flask import Flask, render_template, request, jsonify
#from flask_debugtoolbar import DebugToolbarExtension
from prediction import prediction

webapp_root_folder = "webapp"
config = read_config_data("params.yaml")
template_dir = os.path.join(webapp_root_folder, "templates")

app = Flask(__name__, template_folder=template_dir)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            if request.form:
                data = dict(request.form)
                response = prediction.form_response(data)
                return render_template("index.html", response=response)
            elif request.json:
                response = prediction.api_response(request.json)
                return jsonify(response)
        except Exception as e:
            #error = {"error": "Something went wrong, please try again later"}
            error = {"error": e}
            return render_template("404.html", error=error)
        
    else:
        return render_template("index.html")

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    #app.debug = True
    #app.config['SECRET_KEY'] = 'keysd1234'
    #toolbar = DebugToolbarExtension(app)
    #app.run(host='0.0.0.0', port=5000)