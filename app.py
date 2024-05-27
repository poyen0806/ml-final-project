# import modules
from flask import Flask, render_template, request

# create an instance of the Flask class
app = Flask(__name__)

# define routes
@app.route('/css')
def index():
    return render_template('index.html')

# add new route here

# run the app
if __name__ == '__main__':
    app.run(debug=True)