import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()
client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

DOMAIN_MAP = {
    "tax": ["incometax.gov.in", "cbdt.gov.in"],
    "insurance": ["irdai.gov.in", "policybazaar.com"],
    "retirement": ["npstrust.org.in", "epfindia.gov.in"],
    "debt": ["rbi.org.in"],
    "sip": ["sebi.gov.in", "amfiindia.com"]
}

def search_domain(query: str, agent_type: str) -> str:
    domains = DOMAIN_MAP.get(agent_type, [])
    
    try:
        results = client.search(
            query=query,
            include_domains=domains,
            max_results=3
        )
        
        output = ""
        for r in results.get("results", []):
            output += f"Source: {r['url']}\n{r['content']}\n\n"
        
        return output if output else "No results found."
    
    except Exception as e:
        return f"Search failed: {str(e)}"