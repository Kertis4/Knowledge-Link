from flask import Flask, jsonify, send_file
from openai import OpenAI
from download_data import download_data
import markdown
from weasyprint import HTML
from flask_cors import CORS, cross_origin
from plot_script import plot_change_over_time_from_csv
app = Flask(__name__)
cors = CORS(app)
oai_client = OpenAI(api_key="redacted")

federal_states = []
with open("federal_states.txt") as f:
    f = f.readlines()
    for line in f:
        federal_states.append(line.strip())

indicators = []
with open("normal_indicators.txt") as f:
    f = f.readlines()
    for line in f:
        indicators.append(line.strip())

@app.route('/api/federal-states')
@cross_origin()
def federal_states_api():
    return jsonify(federal_states)

@app.route('/api/indicators')
@cross_origin()
def indicators_api():
    return jsonify(indicators)

@app.route('/api/data/<year>/<federal_state>/<indicator>')
def data_api(year, federal_state, indicator):
    data = download_data(indicator, federal_state, year)
    return data, 200, {'Content-Type': 'text/csv'}

@app.route('/api/ai/<federal>/<year>/<indicator>')#<additional>')
def api_prompt(federal, year, indicator):
    # if not additional or additional == "" or additional == None:
    #     additional = ""
    data = download_data(indicator, federal, year)
    completion = oai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a statistical researcher tasked with writing a research report on the provided statistics from Germany. Focus on the data from a specific federal state (Insert state). Analyse the statistics and trends within the dataset, providing a detailed interpretation of the data. Provide an overview of the federal state, its key characteristics, and the scope of the report. Include any relevant historical or current context about the region. Summarize the key findings from the data in bullet points. Highlight significant trends, patterns, or anomalies in areas such as demographics, economy, health, education, or environment. Use clear and concise language. Discuss potential historical, political, social, or economic reasons that may explain the observed trends. Include historical or current political context that may have influenced the statistics. Identify the challenges or issues related to the statistics. Discuss the potential effects these challenges might have on the federal state and its population. Provide actionable suggestions to address the challenges or enhance positive trends. Suggest policy measures, initiatives, or areas for improvement. Highlight gaps in the data or areas that require deeper investigation. Suggest specific research questions or topics that could provide more insights. Summarize the main points of the report and their implications for the federal state."},
            {
                "role": "user",
                "content": f"Here is my data on {indicator} from {year}. {data}"
            }
        ]
    )
    #print(data)
    text = str(completion.choices[0].message.content)
    html = markdown.markdown(text)
    html = """<header><h1 style="text-align:center">Byte Me - Knowledge Link</h1></header>""" + html
    HTML(string=html).write_pdf("report.pdf")
    #return pdf file
    return send_file("report.pdf", as_attachment=False)

# @app.route('/api/plot/<federal>/<year>/<indicator>')
# def plot_route(federal, year, indicator):
#     data = download_data(indicator, federal, year)
#     #plot_change_over_time_from_csv(str(data), )
#     return
if __name__ == '__main__':
    app.run(debug=True)
