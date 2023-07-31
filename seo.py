from flask import Flask, render_template, request, Response, render_template_string, send_file
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import openai
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import requests
import csv
import os

app = Flask(__name__)
Bootstrap(app)
openai.api_key = '##### YOUR KEY #####'

def get_html(url):
    response = requests.get(url)
    response.encoding = 'utf-8'  
    return response.text

def remove_unwanted_characters(text):
    text = text.rstrip('.')  # remove dot at the end
    text = text.strip('"')   # remove quotes at the beginning and the end
    return text
    
def get_seo_optimized_text(url, listkey, original_text, type_of_text, language):
    if type_of_text == "title":
        data = {
            'prompt': f'Create a short, SEO-optimized frase not more than 65 symbols for a webpage with the title: "{original_text}", which may include (but not necessarily all) the following key phrases: "{listkey}". The {type_of_text} should be in {language}, and if the language is Russian, not every word should start with a capital letter.',
            'max_tokens': 140,
            'temperature': 0.3,
            'model': 'text-davinci-003'
        }
    elif type_of_text == "meta description":
        data = {
            'prompt': f'Create a short, SEO-optimized {type_of_text} not more than 170 symbols for a webpage with the title: "{original_text}", which may include (but not necessarily all) the following key phrases: "{listkey}". The {type_of_text} should be in {language}.',
            'max_tokens': 350,
            'temperature': 0.3,
            'model': 'text-davinci-003'
        }
    response = requests.post('https://api.openai.com/v1/completions', headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + openai.api_key}, json=data)
    if response.status_code == 200:
        result = response.json()['choices'][0]['text'].strip()
        return result.strip('"')  # Removing any leading/trailing double quotes
    else:
        print(f"Error generating {type_of_text} for title: {original_text}\nAPI Response: {response.text}\n")
        return ""
        
def get_title_description(url, listkey, language):
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('title').string
    description = soup.find('meta', attrs={'name':'description'})

    description = description['content'] if description else get_seo_optimized_text(url, listkey, title, "meta description", language)
    optimized_title = get_seo_optimized_text(url, listkey, title, "title", language)
    optimized_title = remove_unwanted_characters(optimized_title)
    
    return [url, title, optimized_title, description]

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'urls' in request.form:
            urls = request.form['urls'].split('\n')
            listkey = request.form['listkey'].split('\n')
            language = request.form['language']
            data = []
            for url in urls:
                url = url.strip()
                data.append(get_title_description(url, listkey, language))
            df = pd.DataFrame(data, columns=['URL', 'Title', 'Optimized Title', 'Description'])

            # Save CSV to temp file
            filename = secure_filename('output.csv')
            df.to_csv(filename, index=False)
            
            # Show table and download link
            table_html = df.to_html(classes="styled-table")
            styles = '''
            <style>
            .styled-table {
                width: 100%;
                border-collapse: collapse;
                margin: 25px 0;
                font-size: 0.9em;
                font-family: sans-serif;
                min-width: 400px;
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
            }
            .styled-table thead tr {
                background-color: #009879;
                color: #ffffff;
                text-align: left;
            }
            .styled-table th,
            .styled-table td {
                padding: 12px 15px;
            }
            .styled-table tbody tr {
                border-bottom: thin solid #dddddd;
            }
            .styled-table tbody tr:nth-of-type(even) {
                background-color: #f3f3f3;
            }
            .styled-table tbody tr:last-of-type {
                border-bottom: 2px solid #009879;
            }
            </style>
            '''
            download_link = '<a href="/download">Download CSV file</a>'
            return f"{styles}{table_html}<br>{download_link}"
        else:
            return "Error: No URLs provided", 400

    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>SEO Tool by Mikhail Glikman</title>
        <style>
            body {
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #f8f9fa;
                font-family: Arial, sans-serif;
            }
            .container {
                padding: 20px;
                border-radius: 10px;
                background-color: white;
                box-shadow: 0px 0px 15px 5px rgba(0,0,0,0.1);
            }
            textarea, select, input[type="submit"] {
                width: 100%;
                margin: 10px 0;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #ced4da;
            }
            input[type="submit"] {
                cursor: pointer;
                color: white;
                background-color: black;
                border: none;
                font-size: 150%;
            }
            input[type="submit"]:hover {
                background-color: #343a40;
            }
            footer {
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
                text-align: center;
                padding: 10px;
                background-color: #f8f9fa;
            }
            a {
                color: inherit;
                text-decoration: none;
            }
            a:hover {
                color: #007bff;
            }
            table {
                   width: 100%;
                   border-collapse: collapse;
                   margin: 20px 0;
               }
               table, th, td {
                   border: 1px solid #ddd;
               }
               th, td {
                   padding: 15px;
                   text-align: left;
               }
               th {
                   background-color: #f2f2f2;
               }
               tr:nth-child(even) {
                   background-color: #f2f2f2;
               }
        </style>
</head>
<body>
    <div class="container">
        <h1 style="text-align: center;">Creating Meta Descriptions and Titles <br>based on URLs and general keywords</h1>

        <form method="post" action="/">
            <label for="urls">Enter the URLs (each URL on a new line):</label>
            <textarea id="urls" name="urls" rows="10"></textarea>

            <label for="listkey">General keywords:</label>
            <textarea id="listkey" name="listkey" rows="5"></textarea>

            <label for="language">Choose a language:</label>
            <select id="language" name="language">
                <option value="English">English</option>
                <option value="Spanish">Spanish</option>
                <option value="Russian">Russian</option>
            </select>

            <input type="submit" value="Show Table and Download CSV">
        </form>
    </div>
    <footer>
         2023 <a href="mailto:mikhail@glikman.es">Mikhail Glikman</a>
    </footer>
</body>
</html>
    ''')

@app.route('/download')
def download():
    filename = secure_filename('output.csv')
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            csv_data = file.read()
        os.remove(filename)  # remove the file after download
        return Response(
            csv_data,
            mimetype="text/csv",
            headers={"Content-disposition":
                     "attachment; filename=output.csv"})
    else:
        return "Error: File does not exist."

if __name__ == '__main__':
    app.run()
