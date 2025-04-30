from pypdf import PdfReader
import requests
from firecrawl import FirecrawlApp, ScrapeOptions
import re
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

def Extract_text_from_pdf(pdf_path):
    # creating a pdf reader object
    reader = PdfReader(pdf_path)
    return "\n".join([page.extract_text() for page in reader.pages])


def Firecrawl_crawl(url):
    # Scrape a website:
    apiKey = os.getenv('FIRECRAWL_API_KEY')
    app = FirecrawlApp(api_key=apiKey)

    scrape_result = app.scrape_url(url, formats=['markdown', 'html'])
    print(scrape_result)


def Extract_titles():
    # Load the text file
    with open("a.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Look for lines with 'Software Engineer'
    software_roles = [line.strip() for line in lines if 'software engineer' in line.lower()]

    # Print unique matches
    for title in sorted(set(software_roles)):
        print(title)


def parse_job_listings(file_path):
    """
    Parse the scrapped data from the given file and extract job listings.
    
    Args:
        file_path (str): Path to the file containing scrapped website data
        
    Returns:
        list: A list of job titles that can be applied for
    """
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return []
    
    # Read the file content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return []
    
    # Different pattern matching strategies to find job listings
    jobs = []
    
    # Strategy 1: Look for common job listing patterns
    # This looks for patterns like "Job Title: Software Engineer" or "Position: Data Analyst"
    job_patterns = [
        r'(?:Job Title|Position|Role|Job):\s*([^\n]+)',
        r'<[^>]*class="[^"]*job-title[^"]*"[^>]*>(.*?)<\/[^>]*>',
        r'<[^>]*class="[^"]*position[^"]*"[^>]*>(.*?)<\/[^>]*>',
        r'data-job-title="([^"]+)"',
        r'title="([^"]+job[^"]+)"'
    ]
    
    for pattern in job_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            # Clean up the job title
            job_title = match.strip()
            if job_title and len(job_title) < 100:  # Avoid overly long strings
                jobs.append(job_title)
    
    # Strategy 2: Look for HTML elements that might contain job listings
    # This targets job listing structures commonly found in careers pages
    if '<li' in content and ('job' in content.lower() or 'career' in content.lower()):
        li_elements = re.findall(r'<li[^>]*>(.*?)</li>', content, re.DOTALL)
        for li in li_elements:
            if 'job' in li.lower() or 'position' in li.lower() or 'career' in li.lower():
                # Try to extract just the job title from the li element
                cleaned = re.sub(r'<[^>]+>', ' ', li)  # Remove HTML tags
                cleaned = re.sub(r'\s+', ' ', cleaned).strip()  # Normalize whitespace
                if 10 < len(cleaned) < 100:  # Reasonable length for a job title with context
                    jobs.append(cleaned)
    
    # Remove duplicates while preserving order
    unique_jobs = []
    for job in jobs:
        if job not in unique_jobs:
            unique_jobs.append(job)
    
    return unique_jobs



import requests
from bs4 import BeautifulSoup
import re

def scrape_google_jobs(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup)
    jobs = []
    
    for job_block in soup.find_all('li', class_='lLd3Je'):
        title = job_block.find('h3', class_='QJPWVe').text.strip()
        location = job_block.find('span', class_='r0wTof').text.strip()
        experience = job_block.find('span', class_='wVSTAb').text.strip()
        
        min_qual = job_block.find('h4', string='Minimum qualifications')
        qualifications = []
        if min_qual:
            for li in min_qual.find_next('ul').find_all('li'):
                qualifications.append(li.text.strip())
                
        jobs.append({
            'title': title,
            'location': location,
            'experience': experience,
            'qualifications': qualifications,
            'link': job_block.find('a', class_='WpHeLc')['href']
        })
    
    return jobs