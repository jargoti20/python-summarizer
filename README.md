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

1. Install the virtual environment
```bash
python -m venv venv
```

2. Install the dependencies
```bash
pip install openai beautifulsoup4 markdown selenium requests python-dotenv
```

3. Create a `.env` file and add your API keys, you can use the `.env.example` file as a template
```bash
DEEPSEEK_API_KEY=your_deepseek_api_key
MOONSHOT_API_KEY=your_moonshot_api_key
```

## Usage

### Activate the virtual environment
```bash
source venv/bin/activate
```

### Analyzing a Markdown File

Users can use the flags `-m` to analyze a Markdown file, `-H` to analyze an HTML file, or `-w` to analyze a web page.

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

## Using Moonshot API

The default `summarizer.py` file uses the DeepSeek API. Users can use the `summarizer-moonshot.py` file to use the Moonshot API.
```bash
python summarizer-moonshot.py -m path/to/article.md
```

## Alias

I personally use have added an alias to my `.zshrc` file to make it easier to run the script.

```bash
alias f(){ cd /users/the_path_to_your_project/summarizer && source venv/bin/activate && python summarizer.py $1 "$2" && deactivate && cd -; unset -f f; }; f
```

Replace `/users/the_path_to_your_project/summarizer` with the path to your project and `f` with whatever name you want to use. Then run the following command to activate the alias.
```bash
source ~/.zshrc
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