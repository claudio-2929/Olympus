import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

def web_search(query: str) -> str:
    """
    Performs a web search using Tavily API.
    Args:
        query: The search query.
    Returns:
        A string summary of search results.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "Error: TAVILY_API_KEY not found in environment variables."
    
    try:
        client = TavilyClient(api_key=api_key)
        response = client.search(query, search_depth="advanced")
        
        results = []
        for result in response.get("results", [])[:5]: # Update to top 5 results
            results.append(f"Title: {result['title']}\nURL: {result['url']}\nContent: {result['content']}\n")
            
        return "\n---\n".join(results)
    except Exception as e:
        return f"Error performing web search: {e}"
