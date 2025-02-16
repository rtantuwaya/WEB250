from flask import Flask, render_template, request

app = Flask(__name__)

def convert_units(value, from_unit, to_unit):
    conversion_factors = {
        'meters': 1,
        'kilometers': 1000,
        'miles': 1609.34
    }

    if from_unit == to_unit:
        return value

    value_in_meters = value * conversion_factors[from_unit]
    result = value_in_meters / conversion_factors[to_unit]
    return result

# Root route (home page)
@app.route('/')
def home():
    return render_template('index.html')  # Ensure you have an index.html template

@app.route('/convert', methods=['GET', 'POST'])
def convert():
    result = None
    if request.method == 'POST':
        value = float(request.form['value'])
        from_unit = request.form['from_unit']
        to_unit = request.form['to_unit']
        result = convert_units(value, from_unit, to_unit)
    return render_template('unit_converter.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)
