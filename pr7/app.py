from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Массив слов для поиска (регистронезависимо)
words = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"]

@app.route('/')
def index1():
    return render_template('index1.html')

@app.route('/index2_post', methods=['POST'])
def index2_post():
    input1 = request.form['input1']
    input2 = request.form['input2']
    return render_template('index2.html', input1=input1, input2=input2)

@app.route('/index3')
def index3():
    return render_template('index3.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    single_line_input = request.form['single_line_input']
    multi_line_output = request.form['multi_line_output']
    return f"Однострочное поле ввода: {single_line_input}<br>Многострочное поле вывода:<br>{multi_line_output}"

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query'].lower()
    matching_words = [word for word in words if word.lower().startswith(query)]
    return jsonify(matching_words)

@app.route('/index4')
def index4():
    return render_template('index4.html')

if __name__ == '__main__':
    app.run(debug=True)
