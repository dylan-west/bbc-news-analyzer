import os
import openai
from bs4 import BeautifulSoup
import requests

class BBCAgent:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key

    def get_bbc_content(self, url="https://www.bbc.com"):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text()

    def analyze_content(self, content):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant analyzing BBC news content."},
                {"role": "user", "content": f"Analyze this BBC content concisely. Summarize the main points in 3-5 short bullet points, using as few words as possible, and do not exceed the response length limit:\n\n{content[:4000]}"}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()

    def get_bbc_contents(self, urls):
        contents = []
        for url in urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            contents.append(soup.get_text())
        return contents


    def compare_analyses(self, analyses):
        return {"analyses": analyses}

    def summarize_trends(self, analyses):
        # Join all analyses into one string for the model
        combined = "\n\n".join(analyses)
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes trends across multiple news article analyses."},
                {"role": "user", "content": (
                    "Given the following analyses of BBC articles, provide a detailed overview of the main trends or common themes. "
                    "For each trend, explain what it could mean for the future, especially considering potential changes in the market, public opinion, or policy. "
                    "Be thorough, insightful, and do not exceed the response length limit:\n\n"
                    f"{combined}"
                )}
            ],
            max_tokens=400
        )
        return response.choices[0].message.content.strip()

    def analyze_contents(self, contents):
        analyses = []
        for content in contents:
            try:
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant analyzing BBC news content."},
                        {"role": "user", "content": f"Analyze this BBC content concisely. Summarize the main points in 3-5 short bullet points, using as few words as possible, and do not exceed the response length limit:\n\n{content[:4000]}"}
                    ],
                    max_tokens=150
                )
                result = response.choices[0].message.content.strip()
            except Exception as e:
                result = f"Error analyzing content: {e}"
            analyses.append(result)
        return analyses

    def get_trends_summary(self, analyses):
        combined = "\n\n".join(analyses)
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes trends across multiple news article analyses."},
                    {"role": "user", "content": (
                        "Given the following analyses of BBC articles, provide a detailed overview of 3-5 main trends. "
                        "For each trend:\n"
                        "1. Start with a clear title in quotes\n"
                        "2. Explain the current situation\n"
                        "3. Describe future implications\n"
                        "Format as complete, numbered points. Ensure each point is complete and not cut off.\n\n"
                        f"{combined}"
                    )}
                ],
                max_tokens=400
            )
            trends = response.choices[0].message.content.strip()
            # Only return if the last trend appears complete (ends with a period)
            if not trends.endswith('.'):
                trends = trends.rsplit('\n', 1)[0]  # Remove last incomplete trend
            return trends
        except Exception as e:
            return f"Error summarizing trends: {e}"

def get_top_bbc_articles(n=10):
    url = "https://www.bbc.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = []
    # BBC homepage: popular articles are often in <a> tags with class 'media__link' or similar
    for a in soup.find_all("a", href=True):
        href = a["href"]
        # Filter for news articles (you can refine this as needed)
        if href.startswith("/news") and href not in links:
            links.append(href)
        if len(links) >= n:
            break
    # Prepend domain if needed
    full_links = [url + link if link.startswith("/") else link for link in links]
    return full_links

if __name__ == "__main__":
    api_key = os.getenv("OPENAI_API_KEY")
    agent = BBCAgent(api_key)
    urls = ["https://www.bbc.com/news", "https://www.bbc.com/sport"]
    contents = agent.get_bbc_contents(urls)
    analyses = agent.analyze_contents(contents)
    comparison = agent.compare_analyses(analyses)
    print(comparison)
