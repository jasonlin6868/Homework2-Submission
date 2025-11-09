# arXiv Paper Abstract Scraper

A Python script to scrape arXiv papers, clean HTML content with Trafilatura, and save results to JSON format.

## Features

- ✅ Fetch latest papers from any arXiv category
- ✅ Clean HTML content using Trafilatura
- ✅ Extract paper metadata: URL, title, abstract, authors, date
- ✅ Save results to timestamped JSON files
- ✅ Interactive command-line interface
- ✅ Respects arXiv API rate limits

## Requirements

Install the required dependencies:

```bash
pip install requests beautifulsoup4 trafilatura
```

Optional (for OCR functionality):
```bash
pip install pytesseract Pillow
```

## Usage

### Basic Usage

Simply run the script and follow the prompts:

```bash
python3 arxiv_scraper.py
```

The script will ask you:
1. **arXiv category** (e.g., `cs.CL`, `cs.AI`, `cs.CV`, `math.PR`)
2. **Number of papers** to fetch (default: 200)

### Example

```
Enter arXiv category (e.g., cs.CL): cs.CL
Enter number of papers to fetch: 50
```

### Popular arXiv Categories

- **cs.CL** - Computation and Language
- **cs.AI** - Artificial Intelligence
- **cs.CV** - Computer Vision
- **cs.LG** - Machine Learning
- **cs.NE** - Neural and Evolutionary Computing
- **math.PR** - Probability
- **physics** - All physics papers

### Output

The script generates a timestamped JSON file with the following format:

```json
[
  {
    "url": "https://arxiv.org/abs/2510.26802v1",
    "title": "Paper Title",
    "abstract": "Paper abstract...",
    "authors": ["Author 1", "Author 2", ...],
    "date": "2025-10-30T17:59:55Z"
  },
  ...
]
```

Example output file: `arxiv_clean_20251101_222345.json`

## Configuration

The script respects arXiv's API limits:
- Maximum 200 papers per API request
- 3-second delay between requests when fetching more than 200 papers

## Troubleshooting

### Import Errors

If you get import errors, make sure all dependencies are installed:

```bash
pip install -r requirements.txt
```

### Network Issues

If you encounter connection issues:
- Check your internet connection
- Ensure arXiv API is accessible
- Try reducing the number of papers

## License

Free to use for educational and research purposes.

## Author

Created for Class 2 AI Courses - Data Collection & Extraction

