from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)


app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Adjust the path to templates folder
template_dir = os.path.abspath('./templates')
app.template_folder = template_dir

csv_file_path = 'sample data.csv'

# Initialize or load DataFrame
if os.path.exists(csv_file_path):
  df = pd.read_csv(csv_file_path, encoding='latin1')
else:
  df = pd.DataFrame(columns=[
    'material_name', 'material_type', 'thickness', 'density', 'flammability_rating',
    'ignition_temp', 'burn_time', 'heat_release_rate', 'smoke_production',
    'toxicity', 'regulations', 'use_case', 'manufacturer', 'flammability_class', 'pass_fail'
  ])

@app.route('/')
def home():
  try:
    table_html = df.to_html(classes='data', header="true")  # Generate a single HTML string
    return render_template('index.html', table_html=table_html)
  except Exception as e:
    app.logger.error(f"Error rendering home template: {e}")
    return "An error occurred while rendering the home page.", 500

@app.route('/search', methods=['GET', 'POST'])
def search():
    try:
        if request.method == 'POST':
            query = request.form['query']
            filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
            return render_template('search.html', tables=[filtered_df.to_html(classes='data', header="true")])
        return render_template('search.html')
    except Exception as e:
        app.logger.error(f"Error processing search request: {e}")
        return "An error occurred while processing the search request.", 500

@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    try:
        if request.method == 'POST':
            new_entry = {
                'material_name': request.form['material_name'],
                'material_type': request.form['material_type'],
                'thickness': request.form['thickness'],
                'density': request.form['density'],
                'flammability_rating': request.form['flammability_rating'],
                'ignition_temp': request.form['ignition_temp'],
                'burn_time': request.form['burn_time'],
                'heat_release_rate': request.form['heat_release_rate'],
                'smoke_production': request.form['smoke_production'],
                'toxicity': request.form['toxicity'],
                'regulations': request.form['regulations'],
                'use_case': request.form['use_case'],
                'manufacturer': request.form['manufacturer'],
                'flammability_class': request.form['flammability_class'],
                'pass_fail': request.form['pass_fail']
            }
            global df
            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            df.to_csv(csv_file_path, index=False, encoding='latin1')
            flash('New entry added successfully!')
            return redirect(url_for('home'))
        return render_template('add_edit.html')
    except Exception as e:
        app.logger.error(f"Error adding new entry: {e}")
        return "An error occurred while adding a new entry.", 500

@app.route('/predict', methods=['GET', 'POST'])
def predict_flammability():
    try:
        if request.method == 'POST':
            material_name = request.form['material_name']
            result = "Pass" if request.form['flammability_class'] == 'Low' else "Fail"
            return render_template('predict.html', prediction=result)
        return render_template('predict.html')
    except Exception as e:
        app.logger.error(f"Error predicting flammability: {e}")
        return "An error occurred while predicting flammability.", 500

if __name__ == '__main__':
    app.run(debug=True)
