# snapchat score bot

Smart, modular automation to simulate safe, human-like Snapchat activity to build/track score at scale.

<p align="center"> 
  <a href="https://github.com/yourusername/snapchat-score-bot">
    <img src="https://img.shields.io/badge/Try%20It%20Free-1E90FF?style=for-the-badge&logo=fire&logoColor=white" alt="Try it Free" width="30%">
  </a> 
</p>

<p align="center">
  <a href="https://discord.gg/vBu9huKBvy">
    <img src="https://img.shields.io/badge/Join-Discord-5865F2?logo=discord" alt="Join Discord">
  </a>
  <a href="https://t.me/devpilot1">
    <img src="https://img.shields.io/badge/Contact-Telegram-2CA5E0?logo=telegram" alt="Contact on Telegram">
  </a>
</p>

## Introduction
**snapchat score bot** helps growth hackers and QA teams automate routine Snapchat actions (open/send snaps, add friends, view stories, light chatting patterns) with realistic delays, device isolation, and proxy support. Built for phone-farm setups (real Android), emulators, or headless flows to test engagement and track score changes safely.

**Key Benefits**
- **Time-saving:** Schedule and batch actions across many devices/accounts.
- **Scalable:** Horizontal scaling via Docker + queue workers.
- **Safer:** Human-like randomness, device isolation, and proxy rotation.

## Features
- Human-like schedulers: randomized delays, day/night windows, action caps.
- Multi-device orchestration (ADB/Appium) with per-device profiles & proxies.
- Pluggable runners: **Python (Appium/ADB)** and **Node.js (Playwright/ADB)**.
- Score tracker: snapshots score before/after runs with CSV/JSON export.
- Task presets: open-snaps, send-snaps to streak list, add-friends, view-stories.
- Anti-pattern guards: cool-downs, max sends/hour, session rotation.
- .env-driven config + per-account YAML for overrides.

<p align="center">
  <img src="snapchat-score-bot.png" alt="snapchat-score-bot hero image" width="90%">
</p>

## Use Cases
- Warm-up new accounts gradually before real campaigns.
- QA/testing Snapchat flows on many devices automatically.
- Research: measure which activity patterns move score without flags.
- Phone-farm orchestration with reporting and audit trails.

## Contact
<p align="left">
  <a href="https://discord.gg/vBu9huKBvy">
    <img src="https://img.shields.io/badge/Join-Discord-5865F2?logo=discord" alt="Join Discord">
  </a>
  <a href="https://t.me/devpilot1">
    <img src="https://img.shields.io/badge/Contact-Telegram-2CA5E0?logo=telegram" alt="Contact on Telegram">
  </a>
</p>

---

## Installation Instructions

### Pre-requisites
- **Python 3.10+**
- **Node.js 18+** (optional Node runner)
- **Java JDK 11+**, **Android Platform Tools (ADB)**
- **Appium Server** (if using Appium flows)
- **Docker** (optional for containerized workers)
- **Devices/Emulators:** Real Android (recommended) or Android emulator
- **Proxies (optional):** HTTP/SOCKS or mobile proxies per device

### Clone the Repo
```bash
git clone https://github.com/yourusername/snapchat-score-bot.git
cd snapchat-score-bot
```


---

## Run Commands

### Python (CLI)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python cli.py run --preset streaks --accounts ./accounts --duration 45m
```

### Node.js (CLI)
```bash
npm i
node runner.js run --preset open-and-send --accounts ./accounts --duration 30m
```

### Docker
```bash
docker build -t snapchat-score-bot .
docker run --rm --env-file .env -v $PWD/accounts:/app/accounts -v $PWD/reports:/app/reports --network host snapchat-score-bot python cli.py run --preset streaks --accounts ./accounts
```



<p align="center">
  <a href="https://discord.gg/vBu9huKBvy">
    <img src="https://img.shields.io/badge/Join-Discord-5865F2?logo=discord" alt="Join Discord">
  </a>
  <a href="https://t.me/devpilot1">
    <img src="https://img.shields.io/badge/Contact-Telegram-2CA5E0?logo=telegram" alt="Contact on Telegram">
  </a>
</p>

