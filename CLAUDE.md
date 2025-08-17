# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a tutorial project demonstrating PocketFlow (a 100-line LLM framework) to build an AI chatbot that automatically learns from live websites. The chatbot intelligently crawls web pages, makes decisions about content relevance, and provides comprehensive answers based on discovered information.

## Architecture

The system uses a **PocketFlow-based agent architecture** with three core nodes:

1. **CrawlAndExtract** - Batch processes multiple URLs to extract content and discover links
2. **AgentDecision** - Intelligent agent deciding whether to answer or explore more pages
3. **DraftAnswer** - Generates comprehensive answers based on collected knowledge

### Data Flow
```
CrawlAndExtract → AgentDecision → DraftAnswer
        ↑             ↓
        └──── explore ──┘
```

### Shared Store Structure
The shared state dictionary contains:
- `user_question`: Current user question
- `conversation_history`: Previous Q&A pairs
- `all_discovered_urls`: All URLs found (indexed list)
- `visited_urls`: Set of processed URL indices
- `url_content`: Dict mapping URL index to content
- `url_graph`: Dict mapping URL index to linked indices

## Commands

### Development Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Install browser for crawler
python -m playwright install --with-deps chromium

# Set API key
export GEMINI_API_KEY="your-key-here"
```

### Running the Application

#### Command Line Interface
```bash
# Basic usage
python main.py https://example.com "What is your pricing?"

# Multiple URLs with custom instruction
python main.py https://site1.com https://site2.com "How do I install?" "Focus on technical docs"
```

#### Web Server
```bash
# Direct hosting
python server.py

# Docker hosting
docker build -t website-chatbot .
docker run -p 8000:8000 -e GEMINI_API_KEY="your-key" website-chatbot
```

#### Testing Utilities
```bash
# Test LLM connection
python utils/call_llm.py

# Test web crawler
python utils/web_crawler.py
```

## Key Components

### Core Files
- `main.py` - CLI entry point with conversational loop
- `server.py` - FastAPI web server with WebSocket support
- `flow.py` - PocketFlow configuration and node connections
- `nodes.py` - Three core node implementations

### Utility Modules
- `utils/call_llm.py` - Google Gemini API wrapper
- `utils/web_crawler.py` - crawl4ai-based web scraping
- `utils/url_validator.py` - Domain filtering for URLs

### Web Interface
- `static/index.html` - Configuration page
- `static/chatbot.html` - Interactive chat interface
- `static/chatbot.js` - Embeddable chatbot widget

## Configuration Parameters

### Global Limits
- `max_iterations`: 5 (max exploration cycles)
- `max_pages`: 50-100 (max pages to visit)
- `content_max_chars`: 10000 (content per page limit)
- `max_urls_per_iteration`: 5-10 (URLs per batch)

### Environment Variables
- `GEMINI_API_KEY` - Required for LLM calls
- `GEMINI_MODEL` - Model selection (defaults to gemini-2.5-flash)

## Development Notes

### Testing Approach
- The system uses manual testing through CLI and web interface
- WebSocket-based real-time updates show crawling progress
- Each node has fallback handling for failures

### Error Handling
- Web crawling failures are logged and skipped
- LLM failures trigger fallback responses
- Input validation prevents XSS attacks in web interface

### Extensibility
- New nodes can be added to `nodes.py` and connected in `flow.py`
- Crawler supports domain filtering via `allowed_domains`
- Custom instructions can guide agent behavior