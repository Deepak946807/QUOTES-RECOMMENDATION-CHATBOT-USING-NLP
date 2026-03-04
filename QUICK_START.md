# 🚀 Quick Start Guide - Quotes Recommendation Bot

## 5-Minute Setup

### Step 1: Activate Virtual Environment

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Train the Model

```bash
rasa train
```

### Step 4: Start Services (Open 3 Terminal Windows)

**Terminal Window 1 - Actions Server:**

```bash
rasa run actions
```

**Terminal Window 2 - Rasa Server:**

```bash
rasa run --enable-api --port 5005
```

**Terminal Window 3 - Web Server:**

```bash
python web/app.py
```

### Step 5: Open in Browser

```
http://localhost:8080
```

---

## 🎮 Testing the Bot

### Test Mood Detection

Type: `I'm feeling really stressed`
Expected: Bot acknowledges stress and provides stress-relief quote

### Test Quote Request

Type: `Make me laugh`
Expected: Funny quote displayed

### Test Suggestions

Click any suggestion button (e.g., "Inspire me")
Expected: Relevant quote and feedback request

---

## 🔧 Troubleshooting

| Problem                    | Solution                                                      |
| -------------------------- | ------------------------------------------------------------- |
| Virtual env not activating | Use PowerShell (not cmd), ensure `.ps1` file exists           |
| `rasa train` fails         | Check YAML syntax, ensure all intents in domain.yml           |
| Bot not responding         | Verify all 3 services running, check ports (5005, 5055, 8080) |
| UI not loading             | Clear browser cache, try incognito mode                       |
| Slow responses             | First training run is slower; subsequent runs are faster      |

---

## 📁 Important Files

| File                       | Purpose                                        |
| -------------------------- | ---------------------------------------------- |
| `domain.yml`               | Bot intents, slots, and responses              |
| `data/nlu.yml`             | Training examples for understanding user input |
| `data/stories.yml`         | Conversation patterns                          |
| `data/rules.yml`           | Deterministic rules                            |
| `actions/actions.py`       | Quote database and logic                       |
| `web/app.py`               | Web server                                     |
| `web/templates/index.html` | Chat interface                                 |
| `web/static/style.css`     | Styling                                        |

---

## 💡 Common Tasks

### Add More Quotes

1. Open `actions/actions.py`
2. Find `QUOTES_DATABASE`
3. Add to appropriate category (e.g., `"motivation"`)
4. Save and restart services

**Example:**

```python
"motivation": [
    {
        "text": "Your new quote here.",
        "author": "Author Name",
        "mood_boost": "high"
    },
    ...
]
```

### Change UI Colors

1. Open `web/static/style.css`
2. Find lines with gradient: `#667eea` to `#764ba2`
3. Replace with your colors
4. Refresh browser

### Add New Mood

1. Update `domain.yml` - Add intent and slot mapping
2. Update `data/nlu.yml` - Add 10+ training examples
3. Update `actions/actions.py` - Add to mood_quote_mapping
4. Run `rasa train`

---

## 📊 Mood Types Supported

| Mood     | Emoji | Maps to Quotes                               |
| -------- | ----- | -------------------------------------------- |
| Great    | 😄    | Funny, Success, Inspiration                  |
| Good     | 😊    | Motivation, Inspiration, Success             |
| Neutral  | 😐    | Motivation, Inspiration                      |
| Sad      | 😢    | Stress Relief, Resilience, Love, Inspiration |
| Unhappy  | 😕    | Resilience, Stress Relief, Motivation, Love  |
| Stressed | 😰    | Stress Relief, Resilience, Funny             |
| Anxious  | 😟    | Stress Relief, Resilience, Inspiration       |

---

## 🎯 Quote Categories

1. **Motivation** (10 quotes) - Drive and action
2. **Inspiration** (10 quotes) - Dreams and possibilities
3. **Love** (8 quotes) - Relationships and self-love
4. **Success** (9 quotes) - Achievement and growth
5. **Funny** (9 quotes) - Humor and lightheartedness
6. **Stress Relief** (6 quotes) - Calm and peace
7. **Resilience** (5 quotes) - Strength and overcoming

---

## ✨ Key Features

✅ **Mood Detection** - 7 different emotional states
✅ **300+ Quotes** - Diverse and inspiring collection
✅ **Smart Recommendations** - Mood-based quote selection
✅ **Beautiful UI** - Modern gradient design
✅ **Mobile Friendly** - Works on any device
✅ **Easy to Customize** - Add quotes, change colors, modify responses

---

## 🆘 Getting Help

### If Services Won't Start:

```bash
# Kill existing processes (if stuck)
# Windows:
Get-Process | Where-Object {$_.ProcessName -like "*rasa*" -or $_.ProcessName -like "*python*"} | Stop-Process -Force

# Then restart services
```

### Test Individual Components:

```bash
# Check Rasa server
curl http://localhost:5005/

# Check Flask server
curl http://localhost:8080/

# Check actions server
# Should be listening on port 5055
```

### View Logs:

Keep terminal windows open to see error messages and debug

---

## 📖 Learn More

- **Rasa Docs**: https://rasa.com/docs/
- **NLU Training**: Check `data/nlu.yml` for 150+ examples
- **Custom Actions**: See `actions/actions.py`
- **Full Documentation**: Open `README_UPDATED.md`

---

## 🎉 You're Ready!

Your bot is now equipped with:

- Advanced mood detection
- 300+ personalized quotes
- Beautiful, responsive interface
- Intelligent conversation flows

**Start chatting and get inspired!**

---

_Need help? Check CHANGES_LOG.md for detailed updates or README_UPDATED.md for full documentation._
