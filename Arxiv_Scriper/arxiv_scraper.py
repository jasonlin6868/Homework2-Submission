#!/usr/bin/env python3
"""
arXiv Paper Abstract Scraper

This script scrapes arXiv papers, cleans HTML with Trafilatura, and optionally
performs OCR on screenshots. It takes an arXiv category from the user and saves
the results to a JSON file.

Requirements:
    pip install requests beautifulsoup4 trafilatura pytesseract Pillow

Usage:
    python3 arxiv_scraper.py
"""

import json
import time
import os
import sys
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import trafilatura
from urllib.parse import urljoin


def fetch_arxiv_papers(category='cs.CL', max_results=200, start=0):
    """
    Fetch arXiv paper metadata using the arXiv API
    
    Args:
        category: arXiv category (e.g., 'cs.CL', 'cs.AI', 'math.PR')
        max_results: Maximum number of papers to fetch (default: 200)
        start: Starting index for pagination (default: 0)
    
    Returns:
        List of paper metadata dictionaries
    """
    base_url = 'http://export.arxiv.org/api/query'
    params = {
        'search_query': f'cat:{category}',
        'start': start,
        'max_results': min(max_results, 200),  # arXiv API limit is 200 per request
        'sortBy': 'submittedDate',
        'sortOrder': 'descending'
    }
    
    print(f"Fetching papers from arXiv category: {category}")
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    
    # Parse XML response
    soup = BeautifulSoup(response.content, 'xml')
    
    papers = []
    entries = soup.find_all('entry')
    
    for entry in entries:
        try:
            paper_id = entry.find('id').text.split('/')[-1]
            url = f"https://arxiv.org/abs/{paper_id}"
            
            title = entry.find('title').text.strip()
            summary = entry.find('summary').text.strip()
            published = entry.find('published').text.strip()
            
            authors = [author.find('name').text for author in entry.find_all('author')]
            
            papers.append({
                'url': url,
                'title': title,
                'abstract': summary,
                'authors': authors,
                'date': published
            })
        except Exception as e:
            print(f"Error parsing paper: {e}")
            continue
    
    print(f"Successfully fetched {len(papers)} papers")
    return papers


def scrape_arxiv_abstract(arxiv_url, use_trafilatura=True):
    """
    Scrape arXiv abstract page and optionally clean with Trafilatura
    
    Args:
        arxiv_url: URL to arXiv abstract page
        use_trafilatura: If True, use Trafilatura for HTML cleaning
    
    Returns:
        Cleaned text content
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(arxiv_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        if use_trafilatura:
            # Use Trafilatura to extract clean text
            extracted_text = trafilatura.extract(response.text, include_comments=False, include_tables=False)
            return extracted_text if extracted_text else response.text
        else:
            return response.text
            
    except Exception as e:
        print(f"Error scraping {arxiv_url}: {e}")
        return None


def run_arxiv_scraper(category='cs.CL', max_results=200):
    """
    Main function to scrape arXiv papers and save to JSON
    
    Args:
        category: arXiv category to scrape
        max_results: Maximum number of papers (default: 200)
    
    Returns:
        List of paper data dictionaries
    """
    print(f"\n{'='*80}")
    print(f"Starting arXiv scraper")
    print(f"{'='*80}")
    print(f"Category: {category}")
    print(f"Max results: {max_results}")
    print(f"{'='*80}\n")
    
    # Fetch all papers (with pagination if needed)
    all_papers = []
    start = 0
    batch_size = 200
    
    while start < max_results:
        batch_results = min(batch_size, max_results - start)
        papers = fetch_arxiv_papers(category=category, max_results=batch_results, start=start)
        
        if not papers:
            break
            
        all_papers.extend(papers)
        start += len(papers)
        
        # Be nice to arXiv API
        if start < max_results and papers:
            print(f"\nFetched {start} papers so far, waiting 3 seconds...")
            time.sleep(3)
    
    print(f"\nTotal papers fetched: {len(all_papers)}")
    
    # Save to JSON file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f'arxiv_clean_{timestamp}.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_papers, f, indent=2, ensure_ascii=False)
    
    file_size = os.path.getsize(output_file) / (1024 * 1024)  # Size in MB
    
    print(f"\n{'='*80}")
    print(f"Results saved to: {output_file}")
    print(f"File size: {file_size:.2f} MB")
    print(f"Number of papers: {len(all_papers)}")
    print(f"{'='*80}\n")
    
    return all_papers


def get_user_input():
    """
    Get user input for arXiv category and number of papers
    
    Returns:
        Tuple of (category, max_results)
    """
    print("\n" + "="*80)
    print("arXiv Paper Abstract Scraper")
    print("="*80)
    print("\nThis tool scrapes arXiv papers and saves them to a JSON file.")
    print("You can specify an arXiv category and number of papers to fetch.")
    print("\nPopular categories:")
    print("  - cs.CL (Computation and Language)")
    print("  - cs.AI (Artificial Intelligence)")
    print("  - cs.CV (Computer Vision)")
    print("  - cs.LG (Machine Learning)")
    print("  - math.PR (Probability)")
    print("  - physics (All physics)")
    print("="*80)
    
    # Get category from user
    while True:
        category = input("\nEnter arXiv category (e.g., cs.CL) or 'q' to quit: ").strip()
        if category.lower() == 'q':
            print("Exiting...")
            sys.exit(0)
        if category:
            break
        print("Please enter a valid category.")
    
    # Get number of papers from user
    while True:
        try:
            max_results = input("Enter number of papers to fetch (default: 200): ").strip()
            if not max_results:
                max_results = 200
            else:
                max_results = int(max_results)
                if max_results < 1:
                    print("Please enter a number greater than 0.")
                    continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    return category, max_results


def main():
    """
    Main entry point for the script
    """
    try:
        # Get user input
        category, max_results = get_user_input()
        
        # Run the scraper
        results = run_arxiv_scraper(category=category, max_results=max_results)
        
        # Ask if user wants to see a sample
        if results:
            show_sample = input("\nWould you like to see a sample paper? (y/n): ").strip().lower()
            if show_sample == 'y':
                print("\n" + "="*80)
                print("Sample Paper:")
                print("="*80)
                print(json.dumps(results[0], indent=2))
                print("="*80 + "\n")
        
        print("Done!")
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

