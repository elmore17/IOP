from flask import Flask, render_template, request, send_file
import requests
from bs4 import BeautifulSoup as BS
import csv
from main import Parser
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start_date_time = request.form['start_date_time']
        start_date_time_obj = datetime.strptime(start_date_time, '%Y-%m-%dT%H:%M')
        end_date_time = request.form['end_date_time']
        end_date_time_obj = datetime.strptime(end_date_time, '%Y-%m-%dT%H:%M')
        format_type = request.form['format_type']

        news = []
        res = requests.get('https://1prime.ru/export/rss2/index.xml')
        soup = BS(res.text, 'xml')
        items = soup.find_all('item')
        for item in items:
            pubDate_str = item.find('pubDate').text
            pubDate_obj = datetime.strptime(pubDate_str, '%a, %d %b %Y %H:%M:%S %z')
            formatted_pubDate = pubDate_obj.strftime('%Y-%m-%dT%H:%M')
            formatted_pubDate_obj = datetime.strptime(formatted_pubDate, '%Y-%m-%dT%H:%M')
            if start_date_time_obj <= formatted_pubDate_obj <= end_date_time_obj:
                title = item.find('title')
                tags = item.find('tags')
                
                if title is not None and pubDate_str is not None and tags is not None:
                    subs = item.find_all('dc:subject')
                    subArr = []
                    for sub in subs:
                        subArr.append(sub.text)
                    news.append(Parser(title.text, pubDate_str, subArr, tags.text))

        if format_type == 'csv':
            filename = 'parsed_data.csv'
            with open(filename, 'w', newline='', encoding='utf-16') as csvfile:
                fieldnames = ['Title', 'PubDate', 'Subjects', 'Tags']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for n in news:
                    subjects_str = '\n'.join(n.subj)
                    writer.writerow({
                        'Title': n.title,
                        'PubDate': n.pubDate,
                        'Subjects': subjects_str,
                        'Tags': n.tags
                    })
        elif format_type == 'txt':
            filename = 'parsed_data.txt'
            with open(filename, 'w', encoding='utf-16') as txtfile:
                for n in news:
                    txtfile.write("Title: {}\n".format(n.title))
                    txtfile.write("PubDate: {}\n".format(n.pubDate))
                    txtfile.write("Subjects:\n")
                    for subj in n.subj:
                        txtfile.write(" - {}\n".format(subj))
                    txtfile.write("Tags: {}\n\n".format(n.tags))
        elif format_type == 'json':
            filename = 'parsed_data.json'
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                data_to_save = []
                for n in news:
                    data_to_save.append({
                        'title': n.title,
                        'pubDate': n.pubDate,
                        'subj': n.subj,
                        'tags': n.tags
                    })
                json.dump(data_to_save, jsonfile, ensure_ascii=False, indent=4)
        return send_file(filename, as_attachment=True, download_name=filename)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
