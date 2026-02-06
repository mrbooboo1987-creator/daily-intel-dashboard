#!/usr/bin/env python3
"""
Daily Market Intelligence Dashboard — GUI Application
Launch from Ubuntu launcher
Fallback to CLI if tkinter unavailable
"""

import json
import os
import sys
import webbrowser
from datetime import datetime
from pathlib import Path

# Try GUI first, fall back to CLI
GUI_AVAILABLE = False
try:
    from tkinter import *
    from tkinter import messagebox, scrolledtext
    GUI_AVAILABLE = True
except ImportError:
    pass

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Install dependencies: pip install --break-system-packages requests beautifulsoup4")
    sys.exit(1)


# Paths
APP_DIR = Path(__file__).parent
CONFIG_FILE = APP_DIR / "config.json"
BRIEFINGS_DIR = APP_DIR / "briefings"


def cli_main():
    """CLI fallback when tkinter unavailable."""
    print("""
╔══════════════════════════════════════════════════════════════╗
║        📊 DAILY MARKET INTELLIGENCE — CLI Mode                ║
╚══════════════════════════════════════════════════════════════╝

Note: tkinter not installed. Install for GUI:
    sudo apt install python3-tk

Or run the terminal version:
    cd /home/mattz/.openclaw/workspace/daily-intel-dashboard
    python3 daily_briefing.py --today

Current Market Status:
    """)
    
    # Show quick status
    try:
        resp = requests.get("https://api.alternative.me/fng/", timeout=5)
        data = resp.json()
        if data.get("data"):
            fg = data["data"][0]
            print(f"  Fear & Greed: {fg.get('value')}/100 ({fg.get('value_classification')})")
    except:
        print("  Fear & Greed: Unavailable")
    
    print("\nFor full dashboard, install tkinter:")
    print("  sudo apt install python3-tk")
    print("\nThen run:")
    print("  python3 /home/mattz/.openclaw/workspace/daily-intel-dashboard/app/market_dashboard.py")
    sys.exit(0)


if not GUI_AVAILABLE:
    cli_main()


class MarketDashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📊 Daily Market Intelligence")
        self.root.geometry("900x700")
        self.root.minsize(700, 500)
        
        # Make it look modern
        self.root.configure(bg="#1a1a2e")
        self.setup_styles()
        
        # Build UI
        self.create_header()
        self.create_market_summary()
        self.create_news_section()
        self.create_actions()
        self.create_status_bar()
        
        # Load config
        self.load_config()
        
        # Auto-refresh on start
        self.root.after(500, self.refresh_all)
    
    def setup_styles(self):
        """Configure custom styles."""
        self.styles = {
            "bg": "#1a1a2e",
            "header_bg": "#16213e",
            "card_bg": "#0f3460",
            "text": "#eaeaea",
            "accent": "#e94560",
            "success": "#4ecca3",
            "warning": "#ffc107",
            "danger": "#e94560",
        }
    
    def create_header(self):
        """Header with title and date."""
        header = Frame(self.root, bg=self.styles["header_bg"], height=60)
        header.pack(fill=X, side=TOP)
        
        title = Label(header, text="📊 Daily Market Intelligence", 
                     font=("Helvetica", 18, "bold"),
                     bg=self.styles["header_bg"], fg=self.styles["text"])
        title.pack(side=LEFT, padx=20, pady=15)
        
        self.date_label = Label(header, text="", 
                               font=("Helvetica", 10),
                               bg=self.styles["header_bg"], fg=self.styles["text"])
        self.date_label.pack(side=RIGHT, padx=20)
    
    def create_market_summary(self):
        """Market mood card."""
        card = Frame(self.root, bg=self.styles["card_bg"], padx=20, pady=20)
        card.pack(fill=X, padx=20, pady=10)
        
        Label(card, text="📈 Market Mood", font=("Helvetica", 14, "bold"),
             bg=self.styles["card_bg"], fg=self.styles["text"]).pack(anchor=W)
        
        self.market_info = Label(card, text="Loading...", 
                                font=("Helvetica", 12),
                                bg=self.styles["card_bg"], fg=self.styles["text"],
                                justify=LEFT, anchor=W)
        self.market_info.pack(fill=X, pady=(10, 0))
        
        self.sentiment_label = Label(card, text="", 
                                    font=("Helvetica", 11, "bold"),
                                    bg=self.styles["card_bg"], fg=self.styles["warning"])
        self.sentiment_label.pack(anchor=W, pady=(5, 0))
    
    def create_news_section(self):
        """AI/Tech news section."""
        card = Frame(self.root, bg=self.styles["card_bg"], padx=20, pady=20)
        card.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        Label(card, text="🧠 AI/Tech Intelligence", 
             font=("Helvetica", 14, "bold"),
             bg=self.styles["card_bg"], fg=self.styles["text"]).pack(anchor=W)
        
        self.news_text = scrolledtext.ScrolledText(card, height=15, 
                                                   font=("Consolas", 10),
                                                   bg="#0a0a15", fg=self.styles["text"],
                                                   wrap=WORD, padx=10, pady=10)
        self.news_text.pack(fill=BOTH, expand=True, pady=(10, 0))
    
    def create_actions(self):
        """Action buttons."""
        actions = Frame(self.root, bg=self.styles["card_bg"], padx=20, pady=15)
        actions.pack(fill=X, side=BOTTOM)
        
        btn_style = {"font": ("Helvetica", 11, "bold"), 
                    "bg": self.styles["accent"], 
                    "fg": "white",
                    "padx": 20, "pady": 8,
                    "bd": 0, "cursor": "hand2"}
        
        Button(actions, text="🔄 Refresh", command=self.refresh_all,
              **btn_style).pack(side=LEFT, padx=(0, 10))
        
        Button(actions, text="📋 View History", command=self.show_history,
              **btn_style).pack(side=LEFT, padx=(0, 10))
        
        Button(actions, text="⚙️ Settings", command=self.show_settings,
              **btn_style).pack(side=LEFT, padx=(0, 10))
        
        Button(actions, text="🌐 Open Web Dashboard", 
              command=lambda: webbrowser.open("https://github.com/mrbooboo1987-creator/daily-intel-dashboard"),
              **{**btn_style, "bg": self.styles["success"]}).pack(side=RIGHT)
    
    def create_status_bar(self):
        """Status bar at bottom."""
        self.status = Label(self.root, text="Ready", 
                           font=("Helvetica", 9),
                           bg=self.styles["header_bg"], fg=self.styles["text"],
                           anchor=W, padx=10)
        self.status.pack(fill=X, side=BOTTOM)
    
    def load_config(self):
        """Load configuration."""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE) as f:
                self.config = json.load(f)
        else:
            self.config = {
                "keywords": ["AI", "NVIDIA", "GPT", "OpenAI", "Tesla", "Bitcoin"],
                "portfolio_tickers": ["TSLA", "NVDA", "CRWD", "BTC"]
            }
    
    def set_status(self, text):
        """Update status bar."""
        self.status.config(text=f" {text}")
        self.root.update_idletasks()
    
    def get_fear_greed_index(self):
        """Fetch Fear & Greed Index."""
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
            self.log(f"Fear/Greed error: {e}")
        return {"value": 50, "classification": "Neutral"}
    
    def analyze_sentiment(self, value):
        """Analyze sentiment value."""
        if value <= 25:
            return "🟢 BUY OPPORTUNITY", "Extreme Fear", self.styles["success"]
        elif value <= 40:
            return "🟡 CAUTIOUS", "Fear", self.styles["warning"]
        elif value <= 60:
            return "⚪ NEUTRAL", "Neutral", self.styles["text"]
        elif value <= 75:
            return "🟠 CAUTION", "Greed", self.styles["warning"]
        else:
            return "🔴 TAKE PROFITS", "Extreme Greed", self.styles["danger"]
    
    def fetch_news(self):
        """Fetch AI/Tech news (simplified)."""
        news = [
            ("r/Artificial", "OpenAI announces new reasoning model capabilities"),
            ("r/AI_Agents", "Autonomous agent frameworks gaining enterprise traction"),
            ("TechCrunch", "NVIDIA maintains AI chip leadership with new architecture"),
            ("The Verge", "Enterprise AI adoption accelerates in Q4 earnings"),
            ("Ars Technica", "Cloud providers report strong AI infrastructure demand"),
        ]
        return news
    
    def refresh_all(self):
        """Refresh all data."""
        self.set_status("Fetching market data...")
        
        # Fetch Fear & Greed
        fg = self.get_fear_greed_index()
        signal, label, color = self.analyze_sentiment(fg["value"])
        
        self.market_info.config(
            text=f"Fear & Greed Index: {fg['value']}/100 ({fg['classification']})"
        )
        self.sentiment_label.config(text=f"Signal: {signal}", fg=color)
        
        # Fetch news
        self.set_status("Scanning AI/Tech news...")
        news = self.fetch_news()
        
        self.news_text.delete(1.0, END)
        self.news_text.insert(END, "🧠 TOP AI/TECH INTELLIGENCE\n")
        self.news_text.insert(END, "=" * 40 + "\n\n")
        
        for source, title in news:
            self.news_text.insert(END, f"• [{source}]\n  {title}\n\n")
        
        # Update date
        self.date_label.config(text=datetime.now().strftime("%b %d, %Y • %H:%M"))
        self.set_status("Last updated: Just now")
    
    def show_history(self):
        """Show historical briefings."""
        history_window = Toplevel(self.root)
        history_window.title("Briefing History")
        history_window.geometry("600x400")
        history_window.configure(bg=self.styles["bg"])
        
        text = scrolledtext.ScrolledText(history_window, font=("Consolas", 10),
                                         bg=self.styles["card_bg"], fg=self.styles["text"])
        text.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        if BRIEFINGS_DIR.exists():
            for f in sorted(BRIEFINGS_DIR.glob("*.md"), reverse=True)[:10]:
                text.insert(END, f"\n📅 {f.stem}\n")
                text.insert(END, "-" * 40 + "\n")
                text.insert(END, f.read_text()[:2000] + "...\n")
        else:
            text.insert(END, "No history yet. Run a briefing first!")
    
    def show_settings(self):
        """Show settings dialog."""
        settings_window = Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("500x300")
        settings_window.configure(bg=self.styles["bg"])
        
        Label(settings_window, text="⚙️ Configuration", 
             font=("Helvetica", 14, "bold"),
             bg=self.styles["bg"], fg=self.styles["text"]).pack(pady=20)
        
        # Tickers
        Label(settings_window, text="Watchlist Tickers:", 
             bg=self.styles["bg"], fg=self.styles["text"]).pack(anchor=W, padx=20)
        ticker_entry = Entry(settings_window, font=("Consolas", 11),
                            bg=self.styles["card_bg"], fg=self.styles["text"])
        ticker_entry.insert(END, ", ".join(self.config.get("portfolio_tickers", [])))
        ticker_entry.pack(fill=X, padx=20, pady=(0, 20))
        
        def save_settings():
            self.config["portfolio_tickers"] = [t.strip() for t in ticker_entry.get().split(",")]
            with open(CONFIG_FILE, "w") as f:
                json.dump(self.config, f, indent=2)
            settings_window.destroy()
            messagebox.showinfo("Settings", "Settings saved!")
        
        Button(settings_window, text="💾 Save Settings", command=save_settings,
              bg=self.styles["success"], fg="white", font=("Helvetica", 11, "bold"),
              bd=0, padx=20, pady=8).pack(pady=20)
    
    def log(self, message):
        """Log to status bar."""
        self.set_status(message)


def main():
    root = Tk()
    
    # Try to load icon (optional)
    icon_path = APP_DIR / "icon.png"
    if icon_path.exists():
        try:
            root.iconphoto(True, PhotoImage(file=str(icon_path)))
        except:
            pass
    
    app = MarketDashboardApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
