from dotenv import load_dotenv
import os
import re
from markupsafe import Markup

load_dotenv()  # Load environment variables from .env

from flask import Flask, request, render_template, jsonify
from src.bbc_agent import BBCAgent, get_top_bbc_articles

app = Flask(__name__)

def convert_numbered_list(text):
    """
    Converts consecutive numbered lines in a block of text to a single HTML ordered list.
    """
    lines = text.split('\n')
    new_lines = []
    in_list = False
    list_items = []

    for line in lines:
        match = re.match(r'^\s*\d+\.\s+(.*)', line)
        if match:
            list_items.append(match.group(1))
            in_list = True
        else:
            if in_list:
                # End of list, output the list
                new_lines.append('<ol>' + ''.join(f'<li>{item}</li>' for item in list_items) + '</ol>')
                list_items = []
                in_list = False
            new_lines.append(line)
    # If the text ends with a list
    if in_list and list_items:
        new_lines.append('<ol>' + ''.join(f'<li>{item}</li>' for item in list_items) + '</ol>')

    return Markup('\n'.join(new_lines))

def convert_dashes_to_ul(text):
    lines = text.split('\n')
    in_list = False
    new_lines = []
    list_items = []
    for line in lines:
        if line.strip().startswith('- '):
            list_items.append(line.strip()[2:])
            in_list = True
        else:
            if in_list:
                new_lines.append('<ul>' + ''.join(f'<li>{item}</li>' for item in list_items) + '</ul>')
                list_items = []
                in_list = False
            new_lines.append(line)
    if in_list and list_items:
        new_lines.append('<ul>' + ''.join(f'<li>{item}</li>' for item in list_items) + '</ul>')
    return Markup('\n'.join(new_lines))

def convert_lists_to_html(text):
    """
    Converts trend summaries to properly formatted HTML.
    """
    if not text:
        return text

    lines = text.split('\n')
    new_lines = []
    current_trend = None

    for line in lines:
        # Match trend titles (numbered with quotes)
        title_match = re.match(r'^\s*(\d+)\.\s*"([^"]+)"', line)
        
        if title_match:
            # Start new trend with proper numbering
            number = title_match.group(1)
            title = title_match.group(2)
            new_lines.append(f'<h3>{number}. "{title}"</h3>')
        elif line.strip() == '---':
            # Add spacing between trends
            new_lines.append('<hr>')
        else:
            # Regular content lines
            if line.strip():
                new_lines.append(f'<p>{line}</p>')

    return Markup('\n'.join(new_lines))

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    urls = []
    error = None
    if request.method == 'POST':
        urls = request.form.get('urls', '').split(',')
    else:
        # On GET, fetch top 10 BBC articles
        urls = get_top_bbc_articles(10)
    api_key = os.getenv('OPENAI_API_KEY')
    agent = BBCAgent(api_key)
    try:
        contents = agent.get_bbc_contents(urls)
        analyses = agent.analyze_contents(contents)
        # Use only convert_lists_to_html for all analyses
        analyses = [convert_lists_to_html(a) for a in analyses]
        result = agent.compare_analyses(analyses)
        zipped = zip(urls, result["analyses"]) if result and "analyses" in result else []
        trends = agent.get_trends_summary(analyses)
        trends = convert_lists_to_html(trends)
    except Exception as e:
        error = f"An error occurred: {e}"
        zipped = []
        trends = ""
    return render_template('index.html', result=result, urls=urls, zipped=zipped, trends=trends, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000))) 