# 📊 Daily Market Intelligence Dashboard

> Your AI-powered morning briefing — news, sentiment, and actionable insights.

## What It Does

🌅 **Morning Briefing** — Daily summary at 7 AM EST with:
- Top AI/Tech/Crypto news
- Market sentiment analysis
- Portfolio impact summary
- Key watch items for the day

📰 **News Aggregation** — Monitors:
- Reddit (r/Artificial, r/AI_Agents, r/MachineLearning)
- Tech blogs (TechCrunch, The Verge, Ars Technica)
- X/Twitter for AI/tech trending topics
- Product hunt for new AI tools

🎯 **Sentiment Tracking** — Compares:
- Social media mood vs. market direction
- Fear & Greed Index
- Sector rotation signals

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run morning briefing
python daily_briefing.py --today

# Generate full report
python daily_briefing.py --full

# Run in daemon mode (checks every 6 hours)
python daily_briefing.py --daemon
```

## Files

- `daily_briefing.py` — Main dashboard script
- `news_aggregator.py` — News collection engine
`sentiment_tracker.py` — Market sentiment analyzer
- `report_generator.py` — Creates beautiful briefings
- `config.json` — Your customization settings

## Setup

1. Copy `config.example.json` to `config.json`
2. Add your preferences (news sources, keywords, etc.)
3. Set up cron for automatic briefings:
   ```bash
   # 7 AM daily
   0 7 * * * /path/to/daily_briefing.py --today
   ```

## Example Output

```
╔══════════════════════════════════════════════════════════════╗
║        📊 DAILY MARKET INTELLIGENCE — Feb 6, 2026              ║
╠══════════════════════════════════════════════════════════════╣
║  🤖 AI/TECH NEWS                                               ║
║  • Sam Altman's "Frontier" platform launching                  ║
║  • NVIDIA maintains AI chip leadership                         ║
║  • OpenAI announces GPT-5 preview                              ║
╠══════════════════════════════════════════════════════════════╣
║  📈 MARKET MOOD                                                ║
║  Fear & Greed: 35 (Fear)                                       ║
║  Sentiment: ⚠️ CAUTIOUS — 7-day software selloff               ║
╠══════════════════════════════════════════════════════════════╣
║  🎯 TODAY'S WATCH                                              ║
║  • Amazon Q4 earnings (AWS + AI capex guidance)               ║
║  • NVDA resistance levels                                     ║
║  • Bitcoin sentiment extremes                                 ║
╚══════════════════════════════════════════════════════════════╝
```

## Philosophy

> "Information is useless if it doesn't drive action."

This dashboard isn't about more news — it's about **better decisions** through:
- Curated signal, not noise
- Sentiment-backed context
- Actionable watch items

---

Built for MrBooBoo. Stay informed. 🚀
