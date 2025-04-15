from src.bbc_agent import BBCAgent
from src.utils import load_config

if __name__ == "__main__":
    config = load_config("config.json")
    api_key = config["api_key"]
    urls = config["urls"]

    agent = BBCAgent(api_key)
    contents = agent.get_bbc_contents(urls)
    analyses = agent.analyze_contents(contents)
    comparison = agent.compare_analyses(analyses)
    print(comparison) 