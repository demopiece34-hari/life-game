import streamlit as st
import json, os, random
from datetime import date, datetime, timedelta
import plotly.express as px

st.set_page_config(page_title="Life Game GOD MODE 😈", layout="wide")

DATA_FILE = "data.json"

LOGIN_USER = st.secrets.get("LOGIN_USER", "hari") if hasattr(st, "secrets") else "hari"
LOGIN_PASS = st.secrets.get("LOGIN_PASS", "9442176514") if hasattr(st, "secrets") else "9442176514"
RESET_PASS = st.secrets.get("RESET_PASS", "h1a2r3i4s5h6") if hasattr(st, "secrets") else "h1a2r3i4s5h6"


def default_data():
    return {
        "points": 0,
        "xp": 0,
        "ma001_last": "",
        "ma001_strict": True,
        "streak": 0,
        "best_streak": 0,
        "last": "",
        "avatar": "😎",
        "name": "Player",
        "dream": "",
        "dream_steps": [],
        "history": {},
        "badges": [],
        "reasons": {},
        "start_date": str(date.today()),
        "final_submitted": {},
        "locked_days": [],
        "custom_tasks": [],
        "custom_task_xp": {},
        "theme": "Dark",
        "quote_mode": True,
        "difficulty": "Normal",
        "mobile_nav": False,
        "moods": {},
        "temp_progress": {},
        "weekly_goals": {},
        "shop_items": [],
        "unlocked_shop": [],

        # NEW UPGRADE
        "control_tracker": {
            "MA001": {"fail_count": 0, "best_clean": 0, "current_clean": 0, "last_fail": ""},
            "PN002": {"fail_count": 0, "best_clean": 0, "current_clean": 0, "last_fail": ""}
        },
        "water_logs": {},
        "money": {
            "balance": 0,
            "income": [],
            "expense": []
        },
        "punishments": {},
        "punishment_done": {},
        "life_wheel": {}
    }


def load():
    base = default_data()
    if not os.path.exists(DATA_FILE):
        return base

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except:
        return base

    for k in base:
        if k not in data:
            data[k] = base[k]

    return data


def save(d):
    with open(DATA_FILE, "w") as f:
        json.dump(d, f, indent=2)


def compute_streak(history):
    streak = 0
    d = date.today()
    while str(d) in history:
        streak += 1
        d -= timedelta(days=1)
    return streak


def safe_progress(value):
    return max(0.0, min(float(value), 1.0))


def motivation(score):
    if score >= 90:
        return "🔥 Beast mode! Today you controlled your day."
    elif score >= 70:
        return "💪 Good work. Small improvements daily create big change."
    elif score >= 40:
        return "⚠️ Average day. Don’t quit, fix tomorrow."
    return "🚨 Reset your focus. One bad day is not the end."


def get_theme_css(theme):
    if theme == "Light":
        bg = "#f8fafc"
        text = "#0f172a"
        card = "rgba(0,0,0,0.06)"
    elif theme == "Purple":
        bg = "linear-gradient(135deg,#2e1065,#4c1d95)"
        text = "white"
        card = "rgba(255,255,255,0.10)"
    elif theme == "Green":
        bg = "linear-gradient(135deg,#052e16,#14532d)"
        text = "white"
        card = "rgba(255,255,255,0.10)"
    else:
        bg = "linear-gradient(135deg,#0f172a,#1e293b)"
        text = "white"
        card = "rgba(255,255,255,0.08)"

    return f"""
    <style>
    body {{background:{bg};color:{text};}}
    .card {{
        background:{card};
        padding:20px;
        border-radius:20px;
        backdrop-filter:blur(12px);
        margin-bottom:15px;
        animation:fade 0.6s;
    }}
    @keyframes fade {{
        from{{opacity:0;transform:translateY(20px);}}
        to{{opacity:1;}}
    }}
    @keyframes float {{
        0%{{transform:translateY(0)}}
        50%{{transform:translateY(-12px)}}
        100%{{transform:translateY(0)}}
    }}
    .stButton button {{
        background:linear-gradient(45deg,#6366f1,#8b5cf6);
        color:white;
        border-radius:10px;
        transition:0.3s;
    }}
    .stButton button:hover {{transform:scale(1.05);}}
    @media(max-width:768px){{
        .block-container{{padding:1rem;}}
        h1{{font-size:28px!important;}}
        h2{{font-size:22px!important;}}
        h3{{font-size:18px!important;}}
        .card{{padding:14px!important;border-radius:14px!important;}}
    }}
    </style>
    """


data = load()
today = date.today()
today_str = str(today)

data["streak"] = compute_streak(data.get("history", {}))
data["best_streak"] = max(data.get("best_streak", 0), data["streak"])
save(data)

# LOGIN
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 Login")
    user = st.text_input("Username", key="login_user")
    pwd = st.text_input("Password", type="password", key="login_pwd")

    if st.button("LOGIN", key="login_btn"):
        if user == LOGIN_USER and pwd == LOGIN_PASS:
            st.session_state.login = True
            st.success("Login Success ⛓️‍💥")
            st.rerun()
        else:
            st.error("Wrong credentials 🔗")
    st.stop()

# =========================
# 60 DAYS HARD RESET MODE
# Login block ku keela, # CAPTCHA ku mela paste pannunga
# =========================

data.setdefault("challenge_60", {
    "enabled": True,
    "start_date": today_str,
    "day": 1,
    "completed_days": [],
    "failed": False,
    "unlocked_main_game": False
})

challenge = data["challenge_60"]

challenge_tasks = [
    "No Porn 🚫",
    "No Masturbation 🚫",
    "Instagram Only 8min ⏳",
    "YouTube Only 8min ⏳",
    "Workout 10min 💪",
    "Wake Up 6:00 AM ⏰",
    "10 Pushups 🔥",
    "Breathing 3min 🌬️",
    "Reading 20min 📚"
]


def coach_reply(q, current_day):
    q = q.lower()

    if "instagram" in q:
        return "📵 Instagram 8 minutes mattum. Timer set panni use pannunga."
    elif "youtube" in q:
        return "▶️ YouTube 8 minutes mattum. Shorts avoid pannunga."
    elif "miss" in q or "fail" in q:
        return "⚠️ One task miss na Day 1 reset. But restart panna defeat illa, discipline training."
    elif "workout" in q or "pushup" in q:
        return "💪 10 mins workout + 10 pushups daily. Small consistency dhaan big change."
    elif "reading" in q:
        return "📚 20 minutes reading phone away vechu silent place la pannunga."
    elif "motivation" in q:
        return "🔥 Today win pannina future version strong aagum. One day at a time."
    elif "60" in q or "day" in q:
        return f"🔥 Ippo Day {current_day}/60. 60 days complete panna main LIFE GAME unlock aagum."
    else:
        return "🧠 Rule simple: daily all tasks complete pannu. One task miss na reset."

def recovery_stage(completed_count):
    focus = min(100, int((completed_count / 60) * 100))
    dopamine = min(100, int((completed_count / 60) * 95))
    self_control = min(100, int((completed_count / 60) * 100))
    energy = min(100, int((completed_count / 60) * 90))
    confidence = min(100, int((completed_count / 60) * 85))

    if completed_count < 7:
        stage = "STARTING RESET"
        message = "Mind cravings varalam. But daily discipline build aagum."
    elif completed_count < 15:
        stage = "CONTROL BUILDING"
        message = "Focus konjam improve aagum. Phone control strong aagum."
    elif completed_count < 30:
        stage = "BRAIN REBALANCE"
        message = "Energy, confidence, concentration better feel aagalam."
    elif completed_count < 45:
        stage = "STRONG DISCIPLINE"
        message = "Old habit control strong aagum. Self respect increase aagum."
    else:
        stage = "GOD MODE LOADING"
        message = "Lifestyle stable aagum. Main game unlock near."

    return focus, dopamine, self_control, energy, confidence, stage, message

if not challenge.get("unlocked_main_game", False):

    completed_days = challenge.get("completed_days", [])
    current_day = len(completed_days) + 1

    if current_day > 60:
        challenge["unlocked_main_game"] = True
        save(data)
        st.success("🔥 60 DAYS COMPLETED")
        st.balloons()
        st.rerun()

    completed_count = len(completed_days)
    days_left = 60 - completed_count
    progress_percent = int((completed_count / 60) * 100)

    focus, dopamine, self_control, energy, confidence, recovery_stage_name, recovery_message = recovery_stage(completed_count)

    if current_day <= 10:
        coach_face = "🙂"
        coach_mode = "STARTER MODE"
        coach_msg = "Start strong. Small discipline daily big change."
    elif current_day <= 30:
        coach_face = "😎"
        coach_mode = "WARRIOR MODE"
        coach_msg = "Good progress. Don’t break the streak."
    elif current_day <= 50:
        coach_face = "🔥"
        coach_mode = "BEAST MODE"
        coach_msg = "You are becoming stronger. Stay locked in."
    else:
        coach_face = "👑"
        coach_mode = "GOD MODE LOADING"
        coach_msg = "Final stage. Main LIFE GAME is near."

    st.markdown("""
<style>
.challenge-wrap {
    display: grid;
    grid-template-columns: 1fr 330px;
    gap: 22px;
}
.hero-card {
    background: linear-gradient(135deg,#020617,#0f172a,#1e1b4b);
    border: 1px solid rgba(99,102,241,0.4);
    border-radius: 24px;
    padding: 24px;
    box-shadow: 0 0 35px rgba(99,102,241,0.35);
    animation: fadeUp 0.8s ease;
    color: white;
}
.stat-grid {
    display: grid;
    grid-template-columns: repeat(4,1fr);
    gap: 14px;
}
.stat-box {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 18px;
    padding: 18px;
    text-align: center;
}
.warning-box {
    background: linear-gradient(135deg,rgba(127,29,29,0.7),rgba(30,41,59,0.5));
    border: 1px solid #ef4444;
    color: white;
    padding: 18px;
    border-radius: 18px;
    text-align: center;
    margin: 20px 0;
    animation: pulseRed 1.8s infinite;
}
.coach-panel {
    position: sticky;
    top: 20px;
    background: linear-gradient(135deg,#020617,#082f49);
    border: 1px solid rgba(34,197,94,0.45);
    border-radius: 24px;
    padding: 22px;
    box-shadow: 0 0 35px rgba(34,197,94,0.30);
    animation: fadeRight 0.9s ease;
    color: white;
}
.coach-avatar {
    font-size: 90px;
    text-align: center;
    animation: floatCoach 3s infinite ease-in-out;
}
.coach-bubble {
    background: rgba(14,165,233,0.14);
    border: 1px solid rgba(56,189,248,0.35);
    padding: 16px;
    border-radius: 18px;
    color: white;
    margin-top: 12px;
}
.glow-title {
    color: white;
    text-shadow: 0 0 18px rgba(250,204,21,0.8);
}
@keyframes floatCoach {
    0% {transform: translateY(0) scale(1);}
    50% {transform: translateY(-14px) scale(1.05);}
    100% {transform: translateY(0) scale(1);}
}
@keyframes pulseRed {
    0% {box-shadow: 0 0 10px rgba(239,68,68,0.35);}
    50% {box-shadow: 0 0 28px rgba(239,68,68,0.75);}
    100% {box-shadow: 0 0 10px rgba(239,68,68,0.35);}
}
@keyframes fadeUp {
    from {opacity:0; transform:translateY(25px);}
    to {opacity:1; transform:translateY(0);}
}
@keyframes fadeRight {
    from {opacity:0; transform:translateX(30px);}
    to {opacity:1; transform:translateX(0);}
}
@media(max-width:900px){
    .challenge-wrap {
        grid-template-columns: 1fr;
    }
    .stat-grid {
        grid-template-columns: repeat(2,1fr);
    }
    .coach-panel {
        position: relative;
        top: 0;
    }
}
</style>
""", unsafe_allow_html=True)

    st.markdown(f"""
<div class="challenge-wrap">

<div>
<div class="hero-card">
<h1 class="glow-title">🔥 60 DAYS HARD RESET CHALLENGE</h1>

<div class="stat-grid">
<div class="stat-box">
<h3>DAY</h3>
<h1>{current_day} / 60</h1>
<p>{days_left} Days Left</p>
</div>

<div class="stat-box">
<h3>XP TODAY</h3>
<h1>100 XP</h1>
<p>Daily Reward</p>
</div>

<div class="stat-box">
<h3>STREAK</h3>
<h1>{completed_count} Days</h1>
<p>Keep it up</p>
</div>

<div class="stat-box">
<h3>STATUS</h3>
<h2>{coach_mode}</h2>
<p>{coach_msg}</p>
</div>
</div>

<div class="warning-box">
<h2>⚠️ ONE TASK MISS = RESET TO DAY 1</h2>
<p>No excuses. Only results.</p>
</div>

<h2>🎯 TODAY'S TASKS</h2>
<p>Complete all tasks and press FINAL SUBMIT.</p>

<div style="background:rgba(255,255,255,0.08);border-radius:20px;padding:16px;margin-top:20px;">
<h3>📊 60 Days Progress</h3>
<div style="background:#334155;border-radius:20px;height:18px;">
<div style="background:linear-gradient(90deg,#22c55e,#84cc16);width:{progress_percent}%;height:18px;border-radius:20px;"></div>
</div>
<p>{progress_percent}% completed</p>
</div>
</div>
</div>

<div class="coach-panel">
<h2>🤖 AI COACH</h2>
<div class="coach-avatar">{coach_face}</div>
<h3 style="text-align:center;color:#22c55e;">{coach_mode}</h3>

<div class="coach-bubble">
<b>Hey KING 🔥</b><br>
Day {current_day} complete panna one step closer to main LIFE GAME.
Focus pannunga. Consistency dhaan power.
</div>

<div class="coach-bubble">
<b>Reminder:</b><br>
One task miss panna reset. So today full complete pannunga.
</div>
</div>

</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="
background:linear-gradient(135deg,#052e16,#064e3b,#0f172a);
border:1px solid rgba(34,197,94,0.5);
border-radius:24px;
padding:22px;
margin-top:20px;
color:white;
box-shadow:0 0 30px rgba(34,197,94,0.25);
animation: fadeUp 0.8s ease;
">

<h2>🧠 LIVE RECOVERY DASHBOARD</h2>
<h3 style="color:#22c55e;">{recovery_stage_name}</h3>
<p>{recovery_message}</p>

<p>🎯 Focus Recovery: {focus}%</p>
<div style="background:#334155;border-radius:20px;height:14px;">
<div style="background:linear-gradient(90deg,#22c55e,#84cc16);width:{focus}%;height:14px;border-radius:20px;"></div>
</div>

<p>⚡ Dopamine Balance: {dopamine}%</p>
<div style="background:#334155;border-radius:20px;height:14px;">
<div style="background:linear-gradient(90deg,#38bdf8,#22c55e);width:{dopamine}%;height:14px;border-radius:20px;"></div>
</div>

<p>🛡️ Self Control: {self_control}%</p>
<div style="background:#334155;border-radius:20px;height:14px;">
<div style="background:linear-gradient(90deg,#a855f7,#22c55e);width:{self_control}%;height:14px;border-radius:20px;"></div>
</div>

<p>💪 Energy Level: {energy}%</p>
<div style="background:#334155;border-radius:20px;height:14px;">
<div style="background:linear-gradient(90deg,#facc15,#22c55e);width:{energy}%;height:14px;border-radius:20px;"></div>
</div>

<p>👑 Confidence: {confidence}%</p>
<div style="background:#334155;border-radius:20px;height:14px;">
<div style="background:linear-gradient(90deg,#fb7185,#22c55e);width:{confidence}%;height:14px;border-radius:20px;"></div>
</div>

<hr>

<p style="color:#bbf7d0;">
✅ No porn + no masturbation + social media control + workout + reading daily follow panna,
discipline and focus gradually improve aagura mathiri track pannalam.
</p>

</div>
    """, unsafe_allow_html=True)

    st.warning("""
⚠️ STRICT RULES

❌ One task miss panna...
❌ One bad habit break panna...
❌ One day skip panna...

🔥 FULL RESET TO DAY 1
""")

    day_key = f"challenge_day_{today_str}"

    data.setdefault("challenge_progress", {})
    data["challenge_progress"].setdefault(day_key, {})

    done = 0

    for task in challenge_tasks:
        checked = st.checkbox(
            task,
            value=data["challenge_progress"][day_key].get(task, False),
            key=f"challenge_{today_str}_{task}"
        )

        data["challenge_progress"][day_key][task] = checked

        if checked:
            done += 1

    today_progress = int((done / len(challenge_tasks)) * 100)

    st.progress(today_progress / 100)
    st.write(f"Today's Progress: {today_progress}%")

    st.markdown("---")
    st.subheader("🤖 Ask AI Coach")

    doubt = st.text_input("60 days challenge doubt type pannunga", key=f"coach_doubt_{today_str}")

    if st.button("Ask Coach 🤖", key=f"ask_coach_{today_str}"):
        if doubt.strip():
            st.success(coach_reply(doubt, current_day))
        else:
            st.warning("Doubt type pannunga.")

    save(data)

    if st.button("FINAL SUBMIT 🔒"):

        all_done = all(
            data["challenge_progress"][day_key].get(t, False)
            for t in challenge_tasks
        )

        if not all_done:
            st.error("""
❌ TASK MISSED

🔥 FULL RESET STARTED
Back to DAY 1
""")

            challenge["completed_days"] = []
            challenge["day"] = 1
            challenge["failed"] = True
            data["challenge_progress"] = {}

            save(data)
            st.stop()

        else:
            if today_str not in challenge["completed_days"]:
                challenge["completed_days"].append(today_str)

            challenge["day"] = len(challenge["completed_days"]) + 1
            challenge["failed"] = False

            data["xp"] += 100
            data["points"] += 100

            save(data)

            st.success(f"""
🔥 DAY {current_day} COMPLETED

⚡ Stay focused.
🏆 60 days complete panna main game unlock aagum.
""")

            st.rerun()

    st.stop()
    
# CAPTCHA
if "captcha_q" not in st.session_state:
    a = random.randint(10, 50)
    b = random.randint(10, 50)
    op = random.choice(["+", "-", "*"])
    ans = a + b if op == "+" else a - b if op == "-" else a * b
    st.session_state.captcha_q = f"{a} {op} {b}"
    st.session_state.captcha_ans = str(ans)

days_passed = (today - datetime.strptime(data["start_date"], "%Y-%m-%d").date()).days
level = min(100, int((days_passed / 365) * 100))
remaining_days = max(0, 365 - days_passed)

BADGE_RULES = {
    10: ("🪵", "Marakattai", 50),
    20: ("🥈", "Silver", 100),
    30: ("🥈", "Silver II", 150),
    40: ("💎", "Platinum", 200),
    50: ("💎", "Platinum II", 250),
    60: ("🔷", "Diamond", 300),
    70: ("👑", "Master", 400),
    80: ("🧠", "Elite", 500),
    90: ("⚡", "Elite Master", 700),
    100: ("🔥", "GOD MODE", 1000)
}


def check_badges():
    unlocked = []
    for lvl, (icon, name, reward) in BADGE_RULES.items():
        if level >= lvl and name not in data["badges"]:
            data["badges"].append(name)
            data["xp"] += reward
            data["points"] += reward
            unlocked.append((icon, name, reward))
    return unlocked


new_badges = check_badges()
if new_badges:
    save(data)
    for icon, name, reward in new_badges:
        st.balloons()
        st.success(f"🎉 {icon} {name} UNLOCKED!")
        st.info(f"💰 Reward: +{reward} XP & Points 🔥")

st.markdown(get_theme_css(data.get("theme", "Dark")), unsafe_allow_html=True)

menu = [
    "🏠 Dashboard",
    "🎮 Missions",
    "📊 Stats",
    "📅 Calendar",
    "📜 History",
    "📄 Report",
    "🎯 Dream",
    "🧑 Profile",
    "🏆 Badges",
    "🛒 Shop",
    "🚫 Control Tracker",
    "💧 Water Tracker",
    "💸 Money Tracker",
    "⚖️ Life Wheel",
    "⚙️ Settings"
]

if data.get("mobile_nav", False):
    choice = st.sidebar.selectbox("Navigation", menu, key="main_navigation_mobile")
else:
    choice = st.sidebar.radio("Navigation", menu, key="main_navigation")

weekday = today.strftime("%A")

task_groups = {
    "Morning": ["Wake 5:30", "Brush", "Bath", "Prayer", "Washing"],
    "Workout 💪": ["Walking (40min) 🚶", "Exercise (30min) 🏋️", "Kegel Exercise 🧠", "Breathing 🌬️"],
    "Learning 📚": ["Python (30min)", "English (15min)", "Reading (1hr)"],
    "Health 🥗": ["Water 2L 🌊", "No Junk Food 🌮"],
    "Control 🎯": ["MA001", "PN002"],
    "Limited Control ⏳": ["Instagram (20min)", "YouTube (20min)"]
}

if data.get("custom_tasks"):
    task_groups["Custom ⭐"] = data["custom_tasks"]

if data.get("dream_steps"):
    task_groups["Dream Steps 🎯"] = data["dream_steps"]

if today_str in data.get("punishments", {}) and not data.get("punishment_done", {}).get(today_str, False):
    task_groups["Punishment Mission ⚠️"] = data["punishments"][today_str]

if weekday == "Saturday":
    task_groups["Weekend"] = ["Movie 🎬"]

if weekday == "Sunday":
    task_groups["Weekend"] = ["Oil Bath 🛁"]

task_xp = {
    "Wake 5:30": 10, "Brush": 5, "Bath": 5, "Prayer": 10, "Washing": 5,
    "Walking (40min) 🚶": 20, "Exercise (30min) 🏋️": 25,
    "Kegel Exercise 🧠": 15, "Breathing 🌬️": 10,
    "Python (30min)": 20, "English (15min)": 15, "Reading (1hr)": 15,
    "Water 2L 🌊": 10, "No Junk Food 🌮": 20,
    "Instagram (20min)": 5, "YouTube (20min)": 5,
    "Movie 🎬": 5, "Oil Bath 🛁": 5,
    "MA001": 30, "PN002": 30,
    "Extra Study 30min 📚": 30,
    "Extra Study 1hr 🔥": 60,
    "Clean Room 🧹": 20,
    "No Social Media Today 🚫": 40,
    "Write Self Review ✍️": 20
}
task_xp.update(data.get("custom_task_xp", {}))

# DASHBOARD
if choice == "🏠 Dashboard":
    st.title("🎯 LIFE GAME")

    money_balance = data.get("money", {}).get("balance", 0)

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("🔥 XP", data["xp"])
    col2.metric("💰 Points", data["points"])
    col3.metric("⚡ Streak", data["streak"])
    col4.metric("🏆 Best Streak", data["best_streak"])
    col5.metric("💸 Money", f"₹{money_balance}")

    if today_str not in data.get("history", {}):
        st.warning("⚠️ Today final submit pending!")

    if today_str in data.get("punishments", {}) and not data.get("punishment_done", {}).get(today_str, False):
        st.error("⚠️ Punishment mission pending! Finish it in Missions page.")

    st.markdown(f"""
    <div class='card'>
    <h1 style='text-align:center;font-size:70px;animation:float 3s infinite;'>{data['avatar']}</h1>
    <h2 style='text-align:center;'>{data['name']}</h2>
    <h3 style='text-align:center;'>Level {level}/100</h3>
    <p style='text-align:center;'>🎯 Remaining Days: {remaining_days}</p>
    <p style='text-align:center;'>Dream: {data.get("dream","")}</p>
    </div>
    """, unsafe_allow_html=True)

    today_score = data.get("history", {}).get(today_str, None)
    if today_score is not None and data.get("quote_mode", True):
        st.info(motivation(today_score))
    elif data.get("quote_mode", True):
        st.info("🚀 Finish today’s missions and final submit.")

    mood = st.selectbox("Today Mood", ["😄 Happy", "🙂 Good", "😐 Normal", "😞 Low"], key="today_mood")
    if st.button("Save Mood"):
        data["moods"][today_str] = mood
        save(data)
        st.success("Mood saved ✅")

# MISSIONS
elif choice == "🎮 Missions":
    st.title("🎮 Missions")

    done = 0
    total = 0
    missed = []
    completed = []
    category_scores = {}

    locked = today_str in data.get("locked_days", [])
    workout_tasks = ["Walking (40min) 🚶", "Exercise (30min) 🏋️", "Kegel Exercise 🧠", "Breathing 🌬️"]
    workout_done = 0
    punishment_tasks_today = data.get("punishments", {}).get(today_str, [])

    if locked:
        st.error("🔒 Today already FINAL SAVED! Editing disabled ❌")

    if punishment_tasks_today and not data.get("punishment_done", {}).get(today_str, False):
        st.warning("⚠️ Punishment mission irukku. Idha complete pannina thaan proper discipline maintain aagum.")

    saved_temp = data.get("temp_progress", {}).get(today_str, {})

    for g, tasks in task_groups.items():
        st.subheader(g)
        group_done = 0

        for t in tasks:
            total += 1

            if t in ["MA001", "PN002"]:
                st.error("🚫 STRICT WARNING: Avoid this habit completely.")

            if g == "Punishment Mission ⚠️":
                st.warning(f"⚠️ Punishment Task: {t}")

            key = f"task_{today_str}_{g}_{t}"
            default_checked = saved_temp.get(t, False)

            checked = st.checkbox(t, value=default_checked, key=key, disabled=locked)

            if not locked:
                data.setdefault("temp_progress", {}).setdefault(today_str, {})[t] = checked
                save(data)

            if checked:
                done += 1
                group_done += 1
                completed.append(t)
                if t in workout_tasks:
                    workout_done += 1
            else:
                missed.append(t)

        category_scores[g] = int((group_done / len(tasks)) * 100) if tasks else 0

    missed = list(dict.fromkeys(missed))
    score = int((done / total) * 100) if total else 0

    st.progress(score / 100)
    st.write(f"Score: {score}%")

    st.subheader("📌 Category Progress")
    for g, s in category_scores.items():
        st.write(f"{g}: {s}%")
        st.progress(safe_progress(s / 100))

    if data.get("quote_mode", True):
        st.info(motivation(score))

    reasons_today = {}

    if missed:
        st.subheader("Missed Reasons")
        for i, t in enumerate(missed):
            r = st.text_input(f"{t}", key=f"reason_input_{today_str}_{i}_{t}", disabled=locked)
            if r:
                reasons_today[t] = r

    if st.button("SAVE", key="temp_save_btn", disabled=locked):
        st.success("✅ Progress Saved (Temporary)")
        st.session_state.temp_score = score
        st.session_state.temp_done = done
        st.session_state.temp_missed = missed
        st.session_state.temp_reasons = reasons_today
        st.session_state.temp_workout_done = workout_done

    st.markdown("---")
    st.subheader("👀 Review Today Summary")
    st.write(f"✅ Completed: {len(completed)}")
    st.write(f"❌ Missed: {len(missed)}")
    st.write(f"📊 Final Score Preview: {score}%")

    st.subheader("🔒 Final Submit")

    current_hour = datetime.now().hour
    anti_cheat_block = current_hour >= 23

    if locked:
        st.error("🔒 Today already FINAL SAVED!")
    elif anti_cheat_block:
        st.warning("⏰ Anti-cheat: Final save blocked after 11 PM.")
    else:
        st.write(f"🧠 Solve CAPTCHA: {st.session_state.captcha_q}")
        captcha_input = st.text_input("Enter Answer", key=f"captcha_input_{today_str}")

        if st.button("FINAL SAVE 💀", key="final_save_btn"):
            if captcha_input != st.session_state.captcha_ans:
                st.error("❌ Wrong Answer! Try again 😈")
            else:
                final_score = st.session_state.get("temp_score", score)
                final_missed = st.session_state.get("temp_missed", missed)
                final_reasons = st.session_state.get("temp_reasons", reasons_today)
                final_workout_done = st.session_state.get("temp_workout_done", workout_done)

                punishment_pending = False
                if punishment_tasks_today:
                    for pt in punishment_tasks_today:
                        if pt in final_missed:
                            punishment_pending = True

                if punishment_pending:
                    st.error("⚠️ Punishment mission complete pannama final save panna mudiyathu.")
                    st.stop()

                data["history"][today_str] = final_score
                data["xp"] += final_score
                data["points"] += final_score

                if final_workout_done == len(workout_tasks):
                    data["xp"] += 50
                    data["points"] += 50

                if final_score == 100:
                    data["xp"] += 100
                    data["points"] += 100

                penalty = 0
                for t in final_missed:
                    penalty += task_xp.get(t, 5)

                if data.get("difficulty") == "Soft":
                    penalty = int(penalty * 0.5)
                elif data.get("difficulty") == "Hard":
                    penalty = int(penalty * 1.5)

                data["xp"] -= penalty
                data["points"] -= penalty

                # Control tracker + punishment generator
                tomorrow_str = str(today + timedelta(days=1))
                data.setdefault("control_tracker", default_data()["control_tracker"])

                for bad_task in ["MA001", "PN002"]:
                    if bad_task in final_missed:
                        data["control_tracker"][bad_task]["current_clean"] += 1
                        data["control_tracker"][bad_task]["best_clean"] = max(
                            data["control_tracker"][bad_task]["best_clean"],
                            data["control_tracker"][bad_task]["current_clean"]
                        )
                        data["xp"] += 30
                        data["points"] += 30
                    else:
                        data["control_tracker"][bad_task]["fail_count"] += 1
                        data["control_tracker"][bad_task]["current_clean"] = 0
                        data["control_tracker"][bad_task]["last_fail"] = today_str
                        data["xp"] -= 50
                        data["points"] -= 50

                        data.setdefault("punishments", {})
                        data["punishments"].setdefault(tomorrow_str, [])

                        if bad_task == "MA001":
                            extra = ["Extra Study 1hr 🔥", "Write Self Review ✍️", "No Social Media Today 🚫"]
                        else:
                            extra = ["Extra Study 30min 📚", "Clean Room 🧹", "Write Self Review ✍️"]

                        for e in extra:
                            if e not in data["punishments"][tomorrow_str]:
                                data["punishments"][tomorrow_str].append(e)

                if punishment_tasks_today:
                    data.setdefault("punishment_done", {})[today_str] = True
                    data["xp"] += 50
                    data["points"] += 50

                data["xp"] = max(0, data["xp"])
                data["points"] = max(0, data["points"])

                data["reasons"][today_str] = {
                    "time": datetime.now().strftime("%H:%M"),
                    "tasks": final_reasons
                }

                if today_str not in data["locked_days"]:
                    data["locked_days"].append(today_str)

                data["streak"] = compute_streak(data["history"])
                data["best_streak"] = max(data["best_streak"], data["streak"])

                save(data)
                st.success("🔥 FINAL SAVE DONE! Locked for today 🔒")

                for k in ["captcha_q", "captcha_ans"]:
                    if k in st.session_state:
                        del st.session_state[k]

                st.rerun()

# STATS
elif choice == "📊 Stats":
    st.title("📊 Stats")

    MAX_XP = 10000
    data["xp"] = max(0, data["xp"])
    save(data)

    col1, col2, col3 = st.columns(3)
    col1.metric("🔥 XP", f"{data['xp']} / {MAX_XP}")
    col2.metric("⚡ Current Streak", data["streak"])
    col3.metric("🏆 Best Streak", data["best_streak"])

    st.progress(safe_progress(data["xp"] / MAX_XP))

    history = data.get("history", {})

    if history:
        dates = list(history.keys())
        scores = list(history.values())

        st.subheader("📈 All Time Growth")
        st.plotly_chart(px.line(x=dates, y=scores, title="Growth Score"), use_container_width=True)

        last_7 = []
        for i in range(6, -1, -1):
            d = str(today - timedelta(days=i))
            last_7.append({"date": d, "score": history.get(d, 0)})

        st.subheader("📊 Weekly Report")
        st.plotly_chart(px.bar(last_7, x="date", y="score", title="Last 7 Days Score"), use_container_width=True)

        avg = sum(x["score"] for x in last_7) / 7
        best = max(last_7, key=lambda x: x["score"])
        worst = min(last_7, key=lambda x: x["score"])

        st.write(f"✅ Weekly Average: {avg:.1f}%")
        st.write(f"🏆 Best Day: {best['date']} → {best['score']}%")
        st.write(f"⚠️ Worst Day: {worst['date']} → {worst['score']}%")

        today_score = history.get(today_str, 0)
        st.subheader("Daily Performance")
        st.plotly_chart(px.pie(values=[today_score, 100 - today_score], names=["Completed", "Pending"]), use_container_width=True)

# CALENDAR
elif choice == "📅 Calendar":
    st.title("📅 Monthly Calendar View")

    history = data.get("history", {})
    first_day = today.replace(day=1)

    days = []
    d = first_day
    while d.month == today.month:
        score = history.get(str(d), None)

        if score is None:
            status = "⚪ Not Submitted"
        elif score >= 80:
            status = "🟢 Good"
        elif score >= 50:
            status = "🟡 Average"
        else:
            status = "🔴 Poor"

        days.append({"Date": str(d), "Day": d.strftime("%A"), "Score": "-" if score is None else score, "Status": status})
        d += timedelta(days=1)

    st.table(days)

# HISTORY
elif choice == "📜 History":
    st.title("📜 History")

    if not data["history"]:
        st.warning("No history yet.")
    else:
        for d, s in sorted(data["history"].items(), reverse=True):
            st.markdown(f"<div class='card'>{d} - Score: {s}%</div>", unsafe_allow_html=True)
            if d in data["reasons"]:
                r = data["reasons"][d]
                st.write("Time:", r.get("time", ""))
                for t, rs in r.get("tasks", {}).items():
                    st.write(f"{t} → {rs}")

# REPORT
elif choice == "📄 Report":
    st.title("📄 Daily / Monthly Report")

    if today_str in data["history"]:
        score = data["history"][today_str]
        reasons = data["reasons"].get(today_str, {})

        report = f"""
Name: {data['name']}
Date: {today_str}
Level: {level}
Points: {data['points']}
XP: {data['xp']}
Streak: {data['streak']}

Score: {score}

Motivation:
{motivation(score)}

"""

        if "tasks" in reasons:
            report += "Missed Tasks:\n"
            for t, r in reasons["tasks"].items():
                report += f"{t} → {r}\n"

        st.text_area("Daily Report", report, height=350, key="report_area")
        st.download_button("Download Daily Report", report, f"report_{today_str}.txt", key="download_report")
    else:
        st.warning("Today final save pannala. Report available after final save.")

    st.subheader("📅 Monthly Report")
    month_report = "Monthly Report\n\n"
    month_scores = []
    for d, s in sorted(data.get("history", {}).items()):
        if d.startswith(today.strftime("%Y-%m")):
            month_scores.append(s)
            month_report += f"{d} → {s}%\n"

    if month_scores:
        month_report += f"\nAverage: {sum(month_scores)/len(month_scores):.1f}%"
        st.download_button("Download Monthly Report", month_report, f"monthly_report_{today.strftime('%Y_%m')}.txt")
    else:
        st.info("This month no submitted data.")

# DREAM
elif choice == "🎯 Dream":
    st.title("🎯 Dream Progress")

    dream = st.text_input("Your Dream", value=data.get("dream", ""), key="dream_input")
    st.subheader("Dream Small Steps")
    new_step = st.text_input("Add dream step", key="new_dream_step")

    if st.button("Add Step", key="add_dream_step"):
        if new_step.strip():
            data["dream_steps"].append(new_step.strip())
            data["dream"] = dream
            save(data)
            st.success("Dream step added ✅")
            st.rerun()

    if st.button("Save Dream", key="save_dream"):
        data["dream"] = dream
        save(data)
        st.success("Dream saved ✅")

    if data.get("dream_steps"):
        for i, step in enumerate(data["dream_steps"]):
            col1, col2 = st.columns([4, 1])
            col1.write(f"✅ {step}")
            if col2.button("Remove", key=f"remove_dream_{i}"):
                data["dream_steps"].pop(i)
                save(data)
                st.rerun()
    else:
        st.info("Dream steps add pannunga. It will show inside Missions.")

# PROFILE
elif choice == "🧑 Profile":
    st.title("🧑 Profile")

    avatar_list = ["😎", "🔥", "👑", "💪", "🧠", "⚡"]
    name = st.text_input("Name", value=data["name"], key="profile_name")
    avatar = st.selectbox("Avatar", avatar_list, index=avatar_list.index(data["avatar"]) if data["avatar"] in avatar_list else 0, key="profile_avatar")
    dream = st.text_input("Dream", value=data.get("dream", ""), key="profile_dream")

    st.markdown(f"### Preview: {avatar} {name}")

    if st.button("SAVE", key="profile_save"):
        data["name"] = name
        data["avatar"] = avatar
        data["dream"] = dream
        save(data)
        st.success("Profile Saved ✅")

    st.subheader("🔥 XP Progress")
    st.write(f"Total XP: {data['xp']}")
    st.progress(safe_progress(max(0, data["xp"]) / 1000))

# BADGES
elif choice == "🏆 Badges":
    st.title("🏆 Your Badges")

    if not data["badges"]:
        st.warning("🔒 All badges are LOCKED. Level up to unlock!")

    for lvl, (icon, name, reward) in BADGE_RULES.items():
        status = "UNLOCKED ✅" if name in data["badges"] else "LOCKED 🔒"
        color = "lightgreen" if name in data["badges"] else "orange"

        st.markdown(f"""
        <div class='card'>
        <h2>{icon} {name} (Level {lvl})</h2>
        <p style='color:{color};'>{status}</p>
        <p>🎁 Reward: +{reward}</p>
        </div>
        """, unsafe_allow_html=True)

# SHOP
elif choice == "🛒 Shop":
    st.title("🛒 Rewards Shop")

    shop = [
        {"name": "🔥 Fire Theme", "cost": 300},
        {"name": "👑 King Title", "cost": 500},
        {"name": "💎 Diamond Avatar", "cost": 800},
        {"name": "⚡ Beast Mode Tag", "cost": 1000}
    ]

    st.write(f"💰 Your Points: {data['points']}")

    for item in shop:
        bought = item["name"] in data.get("unlocked_shop", [])
        col1, col2 = st.columns([3, 1])
        col1.write(f"{item['name']} — {item['cost']} points")

        if bought:
            col2.success("Unlocked")
        else:
            if col2.button("Buy", key=f"buy_{item['name']}"):
                if data["points"] >= item["cost"]:
                    data["points"] -= item["cost"]
                    data.setdefault("unlocked_shop", []).append(item["name"])
                    save(data)
                    st.success("Purchased ✅")
                    st.rerun()
                else:
                    st.error("Not enough points ❌")

# CONTROL TRACKER
elif choice == "🚫 Control Tracker":
    st.title("🚫 Control Tracker")

    st.info("MA001 / PN002 control progress inga track aagum.")

    for habit, info in data.get("control_tracker", {}).items():
        st.markdown(f"""
        <div class='card'>
        <h2>{habit}</h2>
        <p>🔥 Current Clean Streak: {info.get("current_clean", 0)} days</p>
        <p>🏆 Best Clean Streak: {info.get("best_clean", 0)} days</p>
        <p>❌ Fail Count: {info.get("fail_count", 0)}</p>
        <p>📅 Last Fail: {info.get("last_fail", "Never")}</p>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("⚠️ Pending Punishments")
    pending = False
    for d, tasks in data.get("punishments", {}).items():
        if not data.get("punishment_done", {}).get(d, False):
            pending = True
            st.warning(f"{d}: {', '.join(tasks)}")

    if not pending:
        st.success("No pending punishment missions ✅")

# WATER TRACKER
elif choice == "💧 Water Tracker":
    st.title("💧 Advanced Water Tracker")

    data.setdefault("water_logs", {})
    data["water_logs"].setdefault(today_str, 0)

    goal = 8
    current_glass = data["water_logs"][today_str]

    col1, col2, col3 = st.columns(3)
    col1.metric("Today Glass", current_glass)
    col2.metric("Goal", goal)
    col3.metric("Progress", f"{int((current_glass / goal) * 100)}%")

    st.progress(safe_progress(current_glass / goal))

    c1, c2 = st.columns(2)
    if c1.button("➕ Add 1 Glass"):
        data["water_logs"][today_str] += 1
        save(data)
        st.rerun()

    if c2.button("➖ Remove 1 Glass"):
        data["water_logs"][today_str] = max(0, data["water_logs"][today_str] - 1)
        save(data)
        st.rerun()

    if data["water_logs"][today_str] >= goal:
        st.success("💧 Water goal completed today!")

    st.subheader("Last 7 Days Water")
    water_rows = []
    for i in range(6, -1, -1):
        d = str(today - timedelta(days=i))
        water_rows.append({"date": d, "glass": data["water_logs"].get(d, 0)})

    st.plotly_chart(px.bar(water_rows, x="date", y="glass", title="Water Glass Count"), use_container_width=True)

# MONEY TRACKER
elif choice == "💸 Money Tracker":
    st.title("💸 Money Tracker")

    data.setdefault("money", {"balance": 0, "income": [], "expense": []})
    money = data["money"]

    total_income = sum(x["amount"] for x in money.get("income", []))
    total_expense = sum(x["amount"] for x in money.get("expense", []))
    balance = total_income - total_expense
    money["balance"] = balance

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Income", f"₹{total_income}")
    col2.metric("💸 Total Expense", f"₹{total_expense}")
    col3.metric("🏦 Balance", f"₹{balance}")

    st.markdown("---")
    st.subheader("➕ Add Income")
    inc_amount = st.number_input("Income Amount", min_value=0, value=0, key="inc_amount")
    inc_note = st.text_input("Income Note", key="inc_note")
    if st.button("Add Income"):
        if inc_amount > 0:
            money["income"].append({
                "date": today_str,
                "amount": int(inc_amount),
                "note": inc_note
            })
            save(data)
            st.success("Income added ✅")
            st.rerun()

    st.subheader("➖ Add Expense")
    exp_amount = st.number_input("Expense Amount", min_value=0, value=0, key="exp_amount")
    exp_note = st.text_input("Expense Note", key="exp_note")
    if st.button("Add Expense"):
        if exp_amount > 0:
            money["expense"].append({
                "date": today_str,
                "amount": int(exp_amount),
                "note": exp_note
            })
            save(data)
            st.success("Expense added ✅")
            st.rerun()

    st.markdown("---")
    st.subheader("📜 Money History")

    rows = []
    for x in money.get("income", []):
        rows.append({"date": x["date"], "type": "Income", "amount": x["amount"], "note": x.get("note", "")})
    for x in money.get("expense", []):
        rows.append({"date": x["date"], "type": "Expense", "amount": x["amount"], "note": x.get("note", "")})

    if rows:
        st.table(sorted(rows, key=lambda x: x["date"], reverse=True))
        st.plotly_chart(px.pie(rows, values="amount", names="type", title="Income vs Expense"), use_container_width=True)
    else:
        st.info("No money records yet.")

# LIFE WHEEL
elif choice == "⚖️ Life Wheel":
    st.title("⚖️ Life Wheel Mission Analysis")

    st.info("Ithu unga daily mission performance ah automatic analyze panni Life Wheel chart ah kaamikum.")

    saved_temp = data.get("temp_progress", {}).get(today_str, {})
    history_score = data.get("history", {}).get(today_str, None)

    analysis = {}

    mapping = {
        "Health": ["Water 2L 🌊", "No Junk Food 🌮", "Bath"],
        "Study": ["Python (30min)", "English (15min)", "Reading (1hr)"],
        "Fitness": ["Walking (40min) 🚶", "Exercise (30min) 🏋️", "Breathing 🌬️"],
        "Discipline": ["Wake 5:30", "Prayer", "Washing"],
        "Control": ["MA001", "PN002"],
        "Dream": data.get("dream_steps", []),
        "Mind": ["Kegel Exercise 🧠", "Breathing 🌬️"],
        "Money": []
    }

    money = data.get("money", {})
    total_income = sum(x["amount"] for x in money.get("income", []))
    total_expense = sum(x["amount"] for x in money.get("expense", []))
    balance = total_income - total_expense

    for area, tasks in mapping.items():
        if area == "Money":
            if total_income == 0 and total_expense == 0:
                analysis[area] = 5
            elif balance > 0:
                analysis[area] = 8
            elif balance == 0:
                analysis[area] = 6
            else:
                analysis[area] = 3
        elif not tasks:
            analysis[area] = 5
        else:
            done = 0
            total = len(tasks)

            for t in tasks:
                if saved_temp.get(t, False):
                    done += 1

            score_10 = int((done / total) * 10) if total else 5
            analysis[area] = score_10

    rows = [{"Area": k, "Score": v} for k, v in analysis.items()]

    col1, col2, col3 = st.columns(3)
    col1.metric("Today Final Score", "-" if history_score is None else f"{history_score}%")
    col2.metric("Money Balance", f"₹{balance}")
    col3.metric("Mission Data", "Final Saved" if history_score is not None else "Live Preview")

    st.subheader("📈 Life Wheel Chart")
    st.plotly_chart(
        px.line_polar(
            rows,
            r="Score",
            theta="Area",
            line_close=True,
            title="Life Balance Based on Missions"
        ),
        use_container_width=True
    )

    st.subheader("📊 Area Wise Score")
    st.plotly_chart(
        px.bar(
            rows,
            x="Area",
            y="Score",
            title="Mission Area Score / 10"
        ),
        use_container_width=True
    )

    weak = min(rows, key=lambda x: x["Score"])
    strong = max(rows, key=lambda x: x["Score"])

    st.warning(f"⚠️ Weak Area: {weak['Area']} → {weak['Score']}/10")
    st.success(f"🔥 Strong Area: {strong['Area']} → {strong['Score']}/10")

    st.markdown("---")
    st.subheader("🧠 Analysis")

    for r in rows:
        if r["Score"] >= 8:
            st.success(f"{r['Area']}: Strong ah irukku ✅")
        elif r["Score"] >= 5:
            st.info(f"{r['Area']}: Average. Innum improve pannalam.")
        else:
            st.error(f"{r['Area']}: Weak. Next focus inga venum ⚠️")

# SETTINGS
elif choice == "⚙️ Settings":
    st.title("⚙️ Settings")

    st.subheader("🎨 Theme Settings")
    theme = st.selectbox("Theme", ["Dark", "Light", "Purple", "Green"], index=["Dark", "Light", "Purple", "Green"].index(data.get("theme", "Dark")))
    quote_mode = st.toggle("Motivation Quote ON/OFF", value=data.get("quote_mode", True))
    mobile_nav = st.toggle("Mobile Friendly Navigation", value=data.get("mobile_nav", False))
    difficulty = st.selectbox("Penalty Mode", ["Soft", "Normal", "Hard"], index=["Soft", "Normal", "Hard"].index(data.get("difficulty", "Normal")))

    if st.button("Save Settings"):
        data["theme"] = theme
        data["quote_mode"] = quote_mode
        data["mobile_nav"] = mobile_nav
        data["difficulty"] = difficulty
        save(data)
        st.success("Settings saved ✅")
        st.rerun()

    st.markdown("---")
    st.subheader("➕ Custom Tasks")

    new_task = st.text_input("New Custom Task")
    new_task_xp = st.number_input("Task XP", min_value=1, max_value=100, value=10)

    if st.button("Add Custom Task"):
        if new_task.strip():
            data["custom_tasks"].append(new_task.strip())
            data["custom_task_xp"][new_task.strip()] = int(new_task_xp)
            save(data)
            st.success("Custom task added ✅")
            st.rerun()

    if data.get("custom_tasks"):
        for i, t in enumerate(data["custom_tasks"]):
            col1, col2 = st.columns([4, 1])
            col1.write(f"{t} — XP: {data.get('custom_task_xp', {}).get(t, 5)}")
            if col2.button("Remove", key=f"remove_custom_{i}"):
                data["custom_task_xp"].pop(t, None)
                data["custom_tasks"].pop(i)
                save(data)
                st.rerun()

    st.markdown("---")
    st.subheader("💾 Backup / Restore")

    backup_json = json.dumps(data, indent=2)
    st.download_button("Download Backup data.json", backup_json, "data_backup.json", "application/json")

    uploaded = st.file_uploader("Restore Backup JSON", type=["json"])
    if uploaded is not None:
        try:
            restored = json.load(uploaded)
            if st.button("Confirm Restore"):
                save(restored)
                st.success("Backup restored ✅")
                st.rerun()
        except:
            st.error("Invalid JSON file ❌")

    st.markdown("---")
    st.subheader("🚨 Reset Data")

    st.warning("Money reset separate checkbox irukku. Tick pannalana money data safe ah irukkum.")

    reset_input = st.text_input("Enter reset password", type="password")
    reset_money = st.checkbox("Also reset Money Tracker data")

    if st.button("RESET ALL DATA"):
        if reset_input == RESET_PASS:
            old_money = data.get("money", {"balance": 0, "income": [], "expense": []})
            new_data = default_data()

            if not reset_money:
                new_data["money"] = old_money

            save(new_data)
            st.success("Data reset completed ✅")
            if not reset_money:
                st.info("Money data reset agala. Safe ah irukku ✅")
            st.rerun()
        else:
            st.error("Wrong reset password ❌")
