import argparse
import json
import re
from openai import OpenAI
from bs4 import BeautifulSoup
import markdown
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests
import time
import sys
import threading
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize the Moonshot client
MOONSHOT_API_KEY = os.getenv("MOONSHOT_API_KEY")  # Use the API key from .env
moonshot_client = OpenAI(api_key=MOONSHOT_API_KEY, base_url="https://api.moonshot.com")

class LoadingAnimation:
    def __init__(self):
        self.is_running = False
        self.animation_thread = None
        self.current_state = "Starting"
        self.states = {
            "Starting": "Initializing process",
            "Fetching": "Fetching content",
            "Extracting": "Extracting text",
            "Analyzing": "Analyzing content with AI",
            "Processing": "Processing results",
            "Complete": "Analysis complete"
        }

    def animate(self):
        dots = 1
        while self.is_running:
            status = self.states.get(self.current_state, self.current_state)
            sys.stdout.write(f"\r{status}{'.' * dots}")
            sys.stdout.flush()
            dots = (dots % 3) + 1
            time.sleep(0.5)
        sys.stdout.write("\r" + " " * 50 + "\r")
        sys.stdout.flush()

    def start(self):
        self.is_running = True
        self.animation_thread = threading.Thread(target=self.animate)
        self.animation_thread.start()

    def stop(self):
        self.is_running = False
        if self.animation_thread:
            self.animation_thread.join()

    def update_state(self, state):
        self.current_state = state

def extract_text_from_markdown(md_content):
    """Convert Markdown to plain text."""
    html_content = markdown.markdown(md_content)
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text()

def extract_text_from_html(html_content):
    """Extract plain text from HTML."""
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text()

def fetch_webpage_content(url, loading=None):
    """Fetch webpage content using Selenium for JavaScript-rendered content."""
    try:
        if loading:
            loading.update_state("Fetching")
            
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(5)
        page_source = driver.page_source
        driver.quit()
        
        if loading:
            loading.update_state("Extracting")
            
        soup = BeautifulSoup(page_source, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text(separator=' ', strip=True)
        return ' '.join(text.split())
    except Exception as e:
        raise Exception(f"Failed to fetch webpage: {e}")

def analyze_article(content, loading=None):
    """Send article content to DeepSeek API for analysis."""
    try:
        if loading:
            loading.update_state("Analyzing")
        
        response = moonshot_client.chat.completions.create(
            model="moonshot-v1-8k",  # Changed model name
            messages=[
                {"role": "system", "content": """You are a skilled editor specializing in creating engaging subtitles. 
                Analyze the following article and provide the following in JSON format:
                {
                    "subtitle1": "First subtitle suggestion",
                    "subtitle2": "Second subtitle suggestion",
                    "subtitle3": "Third subtitle suggestion",
                    "subtitle4": "Fourth subtitle suggestion",
                    "subtitle5": "Fifth subtitle suggestion",
                    "excerpt": "Brief summary of the article",
                    "category": ["main category"],
                    "tags": ["tag1", "tag2", "tag3"]
                }

                For the subtitles:
                - Each subtitle MUST be between 90-95 characters long, strictly cannot be longer than 95 characters (very important)
                - Provide additional context or perspective
                - Be conversational and intriguing
                - Complement rather than compete with the main title
                - Start with phrases like "How...", "Why...", "Where...", "When...", "A look at...", 
                  "Inside...", "Exploring...", "Understanding..."

                Example subtitle format (with character count):
                - "How artificial intelligence is revolutionizing the workplace while addressing key challenges in automation" (96 chars)
                - "A deep dive into the evolving landscape of technology and its impact on tomorrow's digital transformation" (98 chars)
                - "Where innovation meets practical application: exploring the intersection of creativity and technical success" (97 chars)
                
                NOT like these (too short):
                - "The AI Revolution" (15 chars)
                - "Technology's Impact" (18 chars)
                - "Future of Work" (13 chars)

                Ensure the response is in valid JSON format enclosed in ```json``` code blocks.
                """},
                {"role": "user", "content": f"Analyze this article and provide the analysis in JSON format:\n\n{content}"},
            ],
            temperature=0.7,
            max_tokens=1000,
            stream=False
        )
        
        result = response.choices[0].message.content
        # Clean up the response to ensure it's valid JSON
        json_match = re.search(r"```json\n(.*?)\n```", result, re.DOTALL)
        if json_match:
            return json_match.group(1)
        return result

    except Exception as e:
        raise Exception(f"API request failed: {e}")

def process_article(article_content, format="md", loading=None):
    """Process the article and extract required information."""
    try:
        if format == "md":
            loading.update_state("Extracting")
            plain_text = extract_text_from_markdown(article_content)
        elif format == "html":
            loading.update_state("Extracting")
            plain_text = extract_text_from_html(article_content)
        elif format == "web":
            plain_text = article_content
        else:
            raise ValueError("Unsupported format. Use 'md', 'html', or 'web'.")

        analysis_result = analyze_article(plain_text, loading)
        loading.update_state("Processing")
        
        # Try to parse the result directly first
        try:
            result = json.loads(analysis_result)
        except json.JSONDecodeError:
            # If direct parsing fails, try to extract JSON from the excerpt
            try:
                excerpt_json = json.loads(analysis_result)
                if isinstance(excerpt_json, dict):
                    result = excerpt_json
                else:
                    raise json.JSONDecodeError("Invalid JSON structure", analysis_result, 0)
            except json.JSONDecodeError:
                # If both attempts fail, use the default structure
                result = {
                    "subtitle1": "",
                    "subtitle2": "",
                    "subtitle3": "",
                    "subtitle4": "",
                    "subtitle5": "",
                    "excerpt": analysis_result,
                    "category": [],
                    "tags": []
                }

        # Ensure all required fields exist
        required_fields = {
            "subtitle1": "",
            "subtitle2": "",
            "subtitle3": "",
            "subtitle4": "",
            "subtitle5": "",
            "excerpt": "",
            "category": [],
            "tags": []
        }
        
        # Update with actual values while maintaining default values for missing fields
        for key in required_fields:
            if key not in result:
                result[key] = required_fields[key]

        # Ensure category is always a list
        if isinstance(result["category"], str):
            result["category"] = [result["category"]]
        
        loading.update_state("Complete")
        return result

    except Exception as e:
        if loading:
            loading.update_state("Error")
        raise e
        
def main():
    parser = argparse.ArgumentParser(description="Analyze articles using DeepSeek API.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-m", "--markdown", help="Path to the Markdown file")
    group.add_argument("-H", "--html", help="Path to the HTML file")
    group.add_argument("-w", "--web", help="URL of the webpage to analyze")
    args = parser.parse_args()

    loading = LoadingAnimation()
    loading.start()

    try:
        if args.markdown:
            file_path = args.markdown
            file_format = "md"
            loading.update_state("Extracting")
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
        elif args.html:
            file_path = args.html
            file_format = "html"
            loading.update_state("Extracting")
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
        elif args.web:
            content = fetch_webpage_content(args.web, loading)
            file_format = "web"
    except FileNotFoundError:
        loading.stop()
        print(f"Error: File not found at {file_path}")
        return
    except Exception as e:
        loading.stop()
        print(f"Error reading content: {e}")
        return

    try:
        result = process_article(content, format=file_format, loading=loading)
        loading.stop()  # Stop the animation before printing results
        print("\nAnalysis Results:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        loading.stop()
        print(f"\nError analyzing article: {e}")

if __name__ == "__main__":
    main()
