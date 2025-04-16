# BBC News Analyzer

A web application that analyzes top BBC news articles using AI to identify trends and provide insights. Built with Flask and OpenAI's GPT-3.5.

## Features

- Automatically fetches and analyzes top BBC news articles
- Provides AI-powered analysis of each article
- Identifies trends and patterns across multiple articles
- Generates future implications and market impact analysis
- Responsive web interface with clean visualization of results

## Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS
- **AI/ML**: OpenAI GPT-3.5
- **Web Scraping**: BeautifulSoup4
- **Deployment**: Render
- **Caching**: Flask-Caching

## Live Demo

Visit the live application at: [BBC News Analyzer](https://bbc-news-analyzer.onrender.com)

## Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/dylan-west/bbc-news-analyzer.git
   cd bbc-news-analyzer
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. Visit `http://localhost:10000` in your browser

