import requests
from bs4 import BeautifulSoup
import openai
import PyPDF2

# Set OpenAI API key
openai.api_key = "APIIII"

# Fetch content from a given URL
def fetch_content_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Remove unnecessary tags
            for script in soup(["script", "style"]):
                script.decompose()
            return soup.get_text()
        else:
            print(f"Failed to fetch {url}")
            return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

# Summarize content using OpenAI API
def summarize_with_openai(content):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": f"Summarize the following content:\n\n{content}"}
            ],
            max_tokens=150, 
            temperature=0.7
        )
        summary = response['choices'][0]['message']['content']
        return summary
    except Exception as e:
        print(f"Error summarizing content: {e}")
        return None

# Extract URLs from the PDF
def extract_urls(pdf_path, num_rows=10):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    
    lines = text.split('\n')
    urls = []
    collecting = False
    current_url = ""
    
    # Collect URLs, handling multi-line URLs
    for line in lines:
        if 'https://' in line or collecting:
            current_url += line.strip()
            collecting = True
            if line.endswith("/"):
                urls.append(current_url)
                current_url = ""
                collecting = False
        
        if len(urls) >= num_rows:
            break
    
    return urls

# Extract URLs from the PDF
urls = extract_urls('Earning_calendar.pdf')

# Store summaries in a text file
with open('summaries.txt', 'a') as f:
    for url in urls:
        content = fetch_content_from_url(url)
        if content:
            print("\nContent fetched successfully, summarizing...")
            summary = summarize_with_openai(content)
            if summary:
                print(f"\nSummary of the content:\n{summary}")
                f.write(f"URL: {url}\nSummary:\n{summary}\n\n")

print("Summaries saved to 'summaries.txt'")