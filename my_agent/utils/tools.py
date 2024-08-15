import subprocess
from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
import tempfile
import os

@tool
def aider(github_clone_path: str, aider_question: str):
    """
    Run Aider commands to analyze a Github repo.

    Ask Aider specific questions about the usage of the repo and how it drives business value.

    You must input the repository name. Aider will return it's analysis.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        # NOTE: This is not ideal, but need to address storage solution
        # First clone the repo
        result = subprocess.run(f"git clone {github_clone_path}", shell=True, text=True, capture_output=True)
        try:
            result = subprocess.run(f"aider --no-check-update --no-auto-commits -m '{aider_question}' --yes --dry-run", shell=True, text=True, capture_output=True)
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Error: {result.stderr}"
        except Exception as e:
            return str(e)

tools = [aider, TavilySearchResults(max_results=1)]