from flask import Flask,render_template, request, jsonify

app = Flask(__name__,template_folder="templates")

@app.route("/")
def hello():
	return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
	data = request.get_json() # retrieve the data sent from JavaScript
	# process the data using Python code
	result = f"This is the data passed from JS {data['value']}. And this is the default information {data['default']}."
	return jsonify(result=result) # return the result to JavaScript

if __name__ == '__main__':
	app.run(debug=True)
