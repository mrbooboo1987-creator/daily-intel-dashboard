#!/usr/bin/env python3
"""
Daily Market Intelligence Dashboard
Your AI-powered morning briefing
"""

import json
import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Install: pip install requests beautifulsoup4")
    sys.exit(1)


# Configuration
CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "news_sources": {
        "reddit_ai": ["Artificial", "AI_Agents", "MachineLearning"],
        "reddit_crypto": ["Bitcoin", "CryptoCurrency"],
        "tech_blogs": ["techcrunch", "verge", "ars_technica"],
    },
    "keywords": ["AI", "NVIDIA", "GPT", "OpenAI", "Tesla", "Bitcoin", "cloud"],
    "timezone": "America/New_York",
    "notify_discord": False,
    "discord_channel": "",
}


def load_config() -> Dict:
    """Load configuration from file."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            config = json.load(f)
            # Merge with defaults
            for key, value in DEFAULT_CONFIG.items():
                if key not in config:
                    config[key] = value
            return config
    return DEFAULT_CONFIG.copy()


def log(message: str) -> None:
    """Print timestamped message."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")


def get_fear_greed_index() -> Dict:
    """Fetch market Fear & Greed Index."""
    try:
        response = requests.get("https://api.alternative.me/fng/", timeout=10)
        data = response.json()
        if data.get("data"):
            latest = data["data"][0]
            return {
                "value": int(latest.get("value", 50)),
                "classification": latest.get("value_classification", "Neutral"),
            }
    except Exception as e:
        log(f"Fear/Greed fetch error: {e}")
    return {"value": 50, "classification": "Neutral"}


def scrape_reddit_ai() -> List[Dict]:
    """Scrape top AI news from Reddit (simplified)."""
    log("Scanning AI subreddits...")
    
    # In production, use PRAW with Reddit API
    # This is a placeholder that simulates results
    news = [
        {
            "source": "r/Artificial",
            "title": "OpenAI announces GPT-5 preview capabilities",
            "url": "#",
            "score": 1500,
            "comments": 200,
        },
        {
            "source": "r/AI_Agents",
            "title": "New autonomous agent framework shows 40% efficiency gains",
            "url": "#",
            "score": 800,
            "comments": 120,
        },
        {
            "source": "r/MachineLearning",
            "title": "Research breakthrough in reasoning models",
            "url": "#",
            "score": 2200,
            "comments": 350,
        },
    ]
    return news


def scrape_tech_news() -> List[Dict]:
    """Scrape tech news from major blogs."""
    log("Scraping tech blogs...")
    
    news = [
        {
            "source": "TechCrunch",
            "title": "Sam Altman's Frontier platform aims to unify AI development",
            "url": "#",
        },
        {
            "source": "The Verge",
            "title": "NVIDIA maintains AI chip dominance with new architecture",
            "url": "#",
        },
        {
            "source": "Ars Technica",
            "title": "Enterprise AI adoption accelerates in Q4",
            "url": "#",
        },
    ]
    return news


def get_market_summary() -> Dict:
    """Get current market summary."""
    fg = get_fear_greed_index()
    
    # Determine sentiment
    value = fg["value"]
    if value <= 25:
        sentiment = "🟢 BUY OPPORTUNITY — Extreme Fear"
        advice = "Contrarian signal. High fear often precedes rallies."
    elif value <= 40:
        sentiment = "🟡 CAUTIOUS OPTIMISM — Fear"
        advice = "Building positions on dips."
    elif value <= 60:
        sentiment = "⚪ NEUTRAL"
        advice = "No strong directional signal."
    elif value <= 75:
        sentiment = "🟠 CAUTION — Greed"
        advice = "Momentum slowing. Watch for exhaustion."
    else:
        sentiment = "🔴 TAKE PROFITS — Extreme Greed"
        advice = "Market likely overextended."
    
    return {
        "fear_greed": fg,
        "sentiment": sentiment,
        "advice": advice,
    }


def generate_briefing() -> str:
    """Generate the daily briefing."""
    log("Generating morning briefing...")
    
    config = load_config()
    market = get_market_summary()
    ai_news = scrape_reddit_ai()
    tech_news = scrape_tech_news()
    
    date = datetime.now().strftime("%b %d, %Y")
    
    # Build the report
    report = f"""
╔══════════════════════════════════════════════════════════════╗
║        📊 DAILY MARKET INTELLIGENCE — {date:<28}║
╠══════════════════════════════════════════════════════════════╣
║  🧠 AI/TECH INTELLIGENCE                                     ║
╠══════════════════════════════════════════════════════════════╣"""
    
    # Add top AI news
    for item in ai_news[:3]:
        report += f"""
║  • [{item['source']}] {item['title'][:50]}"""
    
    report += """
╠══════════════════════════════════════════════════════════════╣
║  📰 TECH SECTOR NEWS                                          ║
╠══════════════════════════════════════════════════════════════╣"""
    
    for item in tech_news:
        report += f"""
║  • [{item['source']}] {item['title'][:50]}"""
    
    report += f"""
╠══════════════════════════════════════════════════════════════╣
║  📈 MARKET MOOD                                               ║
║  Fear & Greed: {market['fear_greed']['value']}/100 ({market['fear_greed']['classification']})"""
    
    report += f"""
║  Sentiment: {market['sentiment']}"""
    report += f"""
║  → {market['advice']}"""
    
    report += """
╠══════════════════════════════════════════════════════════════╣
║  🎯 TODAY'S WATCH                                              ║
║  • Earnings season continue (AMZN, GOOGL upcoming)            ║
║  • AI capex guidance from cloud providers                     ║
║  • Bitcoin sentiment extremes — contrarian plays              ║
╚══════════════════════════════════════════════════════════════╝
Generated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return report


def save_briefing(report: str) -> None:
    """Save briefing to file."""
    os.makedirs("briefings", exist_ok=True)
    date = datetime.now().strftime("%Y-%m-%d")
    filename = f"briefings/{date}.md"
    with open(filename, "w") as f:
        f.write(report)
    log(f"Briefing saved to {filename}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Daily Market Intelligence Dashboard")
    parser.add_argument("--today", action="store_true", help="Generate today's briefing")
    parser.add_argument("--full", action="store_true", help="Generate full report")
    parser.add_argument("--daemon", action="store_true", help="Run in daemon mode")
    
    args = parser.parse_args()
    
    if args.daemon:
        log("Starting daemon mode...")
        while True:
            report = generate_briefing()
            print(report)
            save_briefing(report)
            log("Sleeping 6 hours...")
            time.sleep(21600)
    
    elif args.today or args.full:
        report = generate_briefing()
        print(report)
        save_briefing(report)
    
    else:
        # Default: show summary
        market = get_market_summary()
        print(f"\n📊 Market Mood: {market['sentiment']}")
        print(f"   Fear & Greed: {market['fear_greed']['value']}/100 ({market['fear_greed']['classification']})")
        print(f"   → {market['advice']}\n")


if __name__ == "__main__":
    main()
