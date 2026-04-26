import streamlit as st
import json, os, random
from datetime import date, datetime, timedelta
import plotly.express as px

st.set_page_config(page_title="Life Game GOD MODE 😈", layout="wide")

DATA_FILE = "data.json"
LOGIN_USER = "hari"
LOGIN_PASS = "9442176514"
RESET_PASS = "h1a2r3i4s5h6"


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
        "theme": "Dark",
        "quote_mode": True
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
    if not history:
        return 0

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
    else:
        return "🚨 Reset your focus. One bad day is not the end."


def get_theme_css(theme):
    if theme == "Light":
        return """
        <style>
        body {background:#f8fafc;color:#0f172a;}
        .card {
            background:rgba(0,0,0,0.06);
            padding:20px;
            border-radius:20px;
            margin-bottom:15px;
            animation:fade 0.6s;
        }
        </style>
        """
    return """
    <style>
    body {background:linear-gradient(135deg,#0f172a,#1e293b);color:white;}
    .card {
        background:rgba(255,255,255,0.08);
        padding:20px;
        border-radius:20px;
        backdrop-filter:blur(12px);
        margin-bottom:15px;
        animation:fade 0.6s;
    }
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

# CAPTCHA
if "captcha_q" not in st.session_state:
    a = random.randint(10, 50)
    b = random.randint(10, 50)
    op = random.choice(["+", "-", "*"])

    if op == "+":
        ans = a + b
    elif op == "-":
        ans = a - b
    else:
        ans = a * b

    st.session_state.captcha_q = f"{a} {op} {b}"
    st.session_state.captcha_ans = str(ans)

# LEVEL
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

# STYLE
st.markdown(get_theme_css(data.get("theme", "Dark")), unsafe_allow_html=True)
st.markdown("""
<style>
@keyframes fade {
    from{opacity:0;transform:translateY(20px);}
    to{opacity:1;}
}
@keyframes float {
    0%{transform:translateY(0)}
    50%{transform:translateY(-12px)}
    100%{transform:translateY(0)}
}
.stButton button {
    background:linear-gradient(45deg,#6366f1,#8b5cf6);
    color:white;
    border-radius:10px;
    transition:0.3s;
}
.stButton button:hover {
    transform:scale(1.05);
}
@media(max-width:768px){
    .block-container{padding:1rem;}
    h1{font-size:28px!important;}
    h2{font-size:22px!important;}
    h3{font-size:18px!important;}
    .card{padding:14px!important;border-radius:14px!important;}
}
</style>
""", unsafe_allow_html=True)

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
    "⚙️ Settings"
]

choice = st.sidebar.radio("Navigation", menu, key="main_navigation")

weekday = today.strftime("%A")

task_groups = {
    "Morning": ["Wake 5:30", "Brush", "Bath", "Prayer", "Washing"],
    "Workout 💪": [
        "Walking (40min) 🚶",
        "Exercise (30min) 🏋️",
        "Kegel Exercise 🧠",
        "Breathing 🌬️"
    ],
    "Learning 📚": [
        "Python (30min)",
        "English (15min)",
        "Reading (1hr)"
    ],
    "Health 🥗": [
        "Water 2L 🌊",
        "No Junk Food 🌮"
    ],
    "Control 🎯": [
        "MA001",
        "PN002"
    ],
    "Limited Control ⏳": [
        "Instagram (20min)",
        "YouTube (20min)"
    ]
}

if data.get("custom_tasks"):
    task_groups["Custom ⭐"] = data["custom_tasks"]

if data.get("dream_steps"):
    task_groups["Dream Steps 🎯"] = data["dream_steps"]

if weekday == "Saturday":
    task_groups["Weekend"] = ["Movie 🎬"]

if weekday == "Sunday":
    task_groups["Weekend"] = ["Oil Bath 🛁"]

task_xp = {
    "Wake 5:30": 10,
    "Brush": 5,
    "Bath": 5,
    "Prayer": 10,
    "Washing": 5,
    "Walking (40min) 🚶": 20,
    "Exercise (30min) 🏋️": 25,
    "Kegel Exercise 🧠": 15,
    "Breathing 🌬️": 10,
    "Python (30min)": 20,
    "English (15min)": 15,
    "Reading (1hr)": 15,
    "Water 2L 🌊": 10,
    "No Junk Food 🌮": 20,
    "Instagram (20min)": 5,
    "YouTube (20min)": 5,
    "Movie 🎬": 5,
    "Oil Bath 🛁": 5,
    "MA001": 30,
    "PN002": 30,
}

# DASHBOARD
if choice == "🏠 Dashboard":
    st.title("🎯 LIFE GAME")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🔥 XP", data["xp"])
    col2.metric("💰 Points", data["points"])
    col3.metric("⚡ Streak", data["streak"])
    col4.metric("🏆 Best Streak", data["best_streak"])

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

    current_day = today.strftime("%A")
    current_date = today.strftime("%d-%m-%Y")

    st.markdown(f"""
    <div style='
        position:fixed;
        bottom:10px;
        left:50%;
        transform:translateX(-50%);
        background:rgba(255,255,255,0.08);
        padding:10px 20px;
        border-radius:15px;
        backdrop-filter:blur(10px);
        text-align:center;
        font-size:14px;
        animation:fade 1s;
    '>
        📅 {current_day} | {current_date}
    </div>
    """, unsafe_allow_html=True)

# MISSIONS
elif choice == "🎮 Missions":
    st.title("🎮 Missions")

    done = 0
    total = 0
    missed = []
    completed = []

    locked = today_str in data.get("locked_days", [])

    workout_tasks = [
        "Walking (40min) 🚶",
        "Exercise (30min) 🏋️",
        "Kegel Exercise 🧠",
        "Breathing 🌬️"
    ]

    workout_done = 0

    if locked:
        st.error("🔒 Today already FINAL SAVED! Editing disabled ❌")

    for g, tasks in task_groups.items():
        st.subheader(g)

        for t in tasks:
            total += 1

            if t in ["MA001", "PN002"]:
                st.error("🚫 STRICT WARNING: Avoid this habit completely.")

            checked = st.checkbox(
                t,
                key=f"task_{today_str}_{g}_{t}",
                disabled=locked
            )

            if checked:
                done += 1
                completed.append(t)
                if t in workout_tasks:
                    workout_done += 1
            else:
                missed.append(t)

    missed = list(dict.fromkeys(missed))
    score = int((done / total) * 100) if total else 0

    st.progress(score / 100)
    st.write(f"Score: {score}%")

    if data.get("quote_mode", True):
        st.info(motivation(score))

    reasons_today = {}

    if missed:
        st.subheader("Missed Reasons")
        for i, t in enumerate(missed):
            r = st.text_input(
                f"{t}",
                key=f"reason_input_{today_str}_{i}_{t}",
                disabled=locked
            )
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
    st.subheader("🔒 Final Submit")

    current_hour = datetime.now().hour
    anti_cheat_block = current_hour >= 23

    if locked:
        st.error("🔒 Today already FINAL SAVED!")
    elif anti_cheat_block:
        st.warning("⏰ Anti-cheat: Final save blocked after 11 PM.")
    else:
        st.write(f"🧠 Solve CAPTCHA: {st.session_state.captcha_q}")

        captcha_input = st.text_input(
            "Enter Answer",
            key=f"captcha_input_{today_str}"
        )

        if st.button("FINAL SAVE 💀", key="final_save_btn"):
            if captcha_input != st.session_state.captcha_ans:
                st.error("❌ Wrong Answer! Try again 😈")
            else:
                final_score = st.session_state.get("temp_score", score)
                final_missed = st.session_state.get("temp_missed", missed)
                final_reasons = st.session_state.get("temp_reasons", reasons_today)
                final_workout_done = st.session_state.get("temp_workout_done", workout_done)

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

                data["xp"] -= penalty
                data["points"] -= penalty

                if "MA001" not in final_missed:
                    data["xp"] += 30
                    data["points"] += 30
                else:
                    data["xp"] -= 30
                    data["points"] -= 30

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

                if "captcha_q" in st.session_state:
                    del st.session_state["captcha_q"]
                if "captcha_ans" in st.session_state:
                    del st.session_state["captcha_ans"]

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
        st.plotly_chart(
            px.bar(last_7, x="date", y="score", title="Last 7 Days Score"),
            use_container_width=True
        )

        avg = sum(x["score"] for x in last_7) / 7
        best = max(last_7, key=lambda x: x["score"])
        worst = min(last_7, key=lambda x: x["score"])

        st.write(f"✅ Weekly Average: {avg:.1f}%")
        st.write(f"🏆 Best Day: {best['date']} → {best['score']}%")
        st.write(f"⚠️ Worst Day: {worst['date']} → {worst['score']}%")

        today_score = history.get(today_str, 0)
        st.subheader("Daily Performance")
        st.plotly_chart(px.pie(
            values=[today_score, 100 - today_score],
            names=["Completed", "Pending"]
        ), use_container_width=True)

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

        days.append({
            "Date": str(d),
            "Day": d.strftime("%A"),
            "Score": "-" if score is None else score,
            "Status": status
        })

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
    st.title("📄 Daily Report")

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

        st.text_area("Report", report, height=350, key="report_area")
        st.download_button("Download Report", report, f"report_{today_str}.txt", key="download_report")
    else:
        st.warning("Today final save pannala. Report available after final save.")

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

    name = st.text_input("Name", value=data["name"], key="profile_name")
    avatar = st.selectbox("Avatar", ["😎", "🔥", "👑", "💪", "🧠", "⚡"], key="profile_avatar")
    dream = st.text_input("Dream", value=data.get("dream", ""), key="profile_dream")

    st.markdown(f"### Preview: {avatar} {name}")

    if st.button("SAVE", key="profile_save"):
        data["name"] = name
        data["avatar"] = avatar
        data["dream"] = dream
        save(data)
        st.success("Profile Saved ✅")

    st.subheader("🏆 Your Badges")

    if data["badges"]:
        for b in data["badges"]:
            st.write(f"🏅 {b}")
    else:
        st.write("No badges unlocked yet 🔒")

    st.subheader("🔥 XP Progress")
    st.write(f"Total XP: {data['xp']}")
    st.progress(safe_progress(max(0, data["xp"]) / 1000))

    st.markdown("---")
    st.subheader("📅 Progress Info")
    st.write(f"🔥 Total Days Tracked: {len(data.get('history', {}))}")
    st.write(f"🔒 Locked Days: {len(data.get('locked_days', []))}")
    st.write(f"⏳ Remaining Days: {365 - len(data.get('history', {}))}")
    st.write(f"⚡ Current Streak: {data['streak']}")
    st.write(f"🏆 Best Streak: {data['best_streak']}")

# BADGES
elif choice == "🏆 Badges":
    st.title("🏆 Your Badges")

    if not data["badges"]:
        st.warning("🔒 All badges are LOCKED. Level up to unlock!")

    for lvl, (icon, name, reward) in BADGE_RULES.items():
        if name in data["badges"]:
            st.markdown(f"""
            <div class='card'>
            <h2>{icon} {name} (Level {lvl})</h2>
            <p style='color:lightgreen;'>UNLOCKED ✅</p>
            <p>🎁 Reward Earned: +{reward}</p>
            </div>
            """, unsafe_allow_html=True)
    
