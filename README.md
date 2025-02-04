# AI Content Summarizer

A simple yet powerful Python-based content analyzer that uses DeepSeek API and Moonshot API to generate titles, subtitles, excerpts, categories, and tags for any article. Works with Markdown files, HTML content, and web pages.

## Features

- Generates 5 engaging titles (under 60 characters)
- Creates 5 descriptive subtitles (90-95 characters)
- Provides article summary/excerpt
- Suggests relevant categories and tags
- Supports multiple input formats:
  - Markdown files
  - HTML files
  - Web URLs (with JavaScript rendering support)
- Real-time loading animation
- Error handling and validation

## Prerequisites
- Obtain API Key from DeepSeek (https://platform.deepseek.com/)
- Obtain API Key from Moonshot (https://platform.moonshot.com/)
## Installation
```bash
pip install openai beautifulsoup4 markdown selenium requests python-dotenv
```

## Usage

### Analyzing a Markdown File

Users can use the -m flag to analyze a Markdown file, -H flag to analyze an HTML file, or -w flag to analyze a web page.

```bash
python summarizer.py -m path/to/article.md
```

### Analyzing an HTML File
```bash
python summarizer.py -H path/to/article.html
```

### Analyzing a Web Page
```bash
python summarizer.py -w https://example.com/article
```

## Output Example

```json
{
  "title1": "AI Revolution: How Machine Learning is Transforming Industries",
  "title2": "The Future of AI: Breaking Down Complex Technologies",
  "title3": "Machine Learning Demystified: A Practical Guide",
  "title4": "Understanding AI: From Theory to Real-World Applications",
  "title5": "AI Innovation: Bridging the Gap Between Theory and Practice",
  "subtitle1": "How artificial intelligence is revolutionizing the workplace while addressing key challenges in automation",
  "subtitle2": "A deep dive into the evolving landscape of technology and its impact on tomorrow's digital transformation",
  "subtitle3": "Understanding the fundamental principles driving AI advancement and their practical applications",
  "subtitle4": "Where innovation meets practical application: exploring the intersection of creativity and success",
  "subtitle5": "Inside the transformative power of AI: analyzing its impact on various industry sectors",
  "excerpt": "Brief summary of the article content...",
  "category": ["Technology"],
  "tags": ["AI", "Machine Learning", "Innovation"]
}
```

## Configuration

Replace the `DEEPSEEK_API_KEY` and `MOONSHOT_API_KEY` in summarizer.py with your DeepSeek and Moonshot API keys:

```python
DEEPSEEK_API_KEY = "your-api-key-here"
MOONSHOT_API_KEY = "your-api-key-here"
```

## Alias

```bash
alias f(){ cd /users/the_path_to_your_project/summarizer && source venv/bin/activate && python summarizer.py $1 "$2" && deactivate && cd -; unset -f f; }; f
```

## Error Handling

The script includes comprehensive error handling for:
- File not found
- Invalid URLs
- API failures
- JSON parsing errors
- Network issues

## License

MIT License - feel free to use and modify as needed.
