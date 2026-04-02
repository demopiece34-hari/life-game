import streamlit as st
import json, os
import random
from datetime import date, datetime, timedelta
import plotly.express as px
st.set_page_config(page_title="Life Game GOD MODE 😈", layout="wide")

# ---------- LOGIN ----------
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("LOGIN"):
        if user == "hari" and pwd == "9442176514":
            st.session_state.login = True
            st.success("Login Success ⛓️‍💥")
        else:
            st.error("Wrong credentials 🔗")
    st.stop()

# ---------- DATA ----------
DATA_FILE = "data.json"

def load():
    default = {
    "points": 0,
    "xp": 0,
    "streak": 0,
    "last": "",
    "avatar": "😎",
    "name": "Player",
    "dream": "",
    "history": {},
    "reasons": {},
    "start_date": str(date.today()),
    "final_submitted": {},
    "locked_days": [],
    }
    if not os.path.exists(DATA_FILE):
        return default
    data = json.load(open(DATA_FILE))
    for k in default:
        if k not in data:
            data[k] = default[k]
    return data

def save(d):
    json.dump(d, open(DATA_FILE, "w"))

data = load()
today = date.today()
today_str = str(today)

# ---------- STRONG CAPTCHA ----------
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

# ---------- LEVEL ----------
days_passed = (today - datetime.strptime(data["start_date"], "%Y-%m-%d").date()).days
level = min(100, int((days_passed / 365) * 100))
remaining_days = max(0, 365 - days_passed)

# ---------- BADGES SYSTEM ----------
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

# ---------- BADGE UNLOCK ----------
new_badges = check_badges()

if new_badges:
    save(data)

    for icon, name, reward in new_badges:
        st.balloons()
        st.success(f"🎉 {icon} {name} UNLOCKED!")
        st.info(f"💰 Reward: +{reward} XP & Points 🔥")

# ---------- UI STYLE ----------
st.markdown("""
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
</style>
""", unsafe_allow_html=True)

# ---------- NAV ----------
menu = ["🏠 Dashboard","🎮 Missions","📊 Stats","📜 History","📄 Report","🧑 Profile","🏆 Badges","⚙️ Settings"]
choice = st.sidebar.radio("Navigation", menu)

# ---------- TASKS ----------
weekday = today.strftime("%A")

task_groups = {
    "Morning": ["Wake 5:30","Brush","Bath","Prayer","Washing"],

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

if weekday == "Saturday":
    task_groups["Weekend"] = ["Movie 🎬"]

if weekday == "Sunday":
    task_groups["Weekend"] = ["Oil Bath 🛁"]

# ---------- TASK XP VALUES ----------
task_xp = {
    "Wake 5:30": 10,
    "Brush": 5,
    "Bath": 5,
    "Prayer": 10,

    "Walking (40min) 🚶": 20,
    "Exercise (30min) 🏋️": 25,
    "Kegel Exercise 🧠": 15,
    "Breathing 🌬️": 10,

    "Python": 20,
    "English": 15,
    "Reading": 15,

    "Water 2L": 10,
    "No Junk": 20
}

# ---------- NAVIGATION HANDLER (Corrected Order) ----------
if choice == "🏠 Dashboard":

    st.title("🎯 LIFE GAME")

    st.markdown(f"""
    <div class='card'>
    <h1 style='text-align:center;font-size:70px;animation:float 3s infinite;'>{data['avatar']}</h1>
    <h2 style='text-align:center;'>{data['name']}</h2>
    <h3 style='text-align:center;'>Level {level}/100</h3>
    <p style='text-align:center;'>🎯 Remaining Days: {remaining_days}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ---------- DATE & DAY (BOTTOM CENTER) ----------
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

elif choice == "🎮 Missions":

    st.title("🎮 Missions")

    done = 0
    total = 0
    missed = []

    workout_tasks = [
        "Walking (40min) 🚶",
        "Exercise (30min) 🏋️",
        "Kegel Exercise 🧠",
        "Breathing 🌬️"
    ]

    workout_done = 0
    completed=[]
    
    # ---------- WORKOUT TASK LIST ----------
    workout_tasks = [
        "Walking (40min) 🚶",
        "Exercise (30min) 🏋️",
        "Kegel Exercise 🧠",
        "Breathing 🌬️"
    ]

    workout_done = 0

    for g, tasks in task_groups.items():
        st.subheader(g)
        for t in tasks:
            total += 1
            locked = today_str in data.get("locked_days", [])

            if st.checkbox(t, key=f"{today_str}_{t}", disabled=locked):
                done += 1
                # 💪 workout track
                if t in workout_tasks:
                    workout_done += 1
                completed.append(t)
            else:
                missed.append(t)

    # Score calculation
    score = int((done / total) * 100) if total else 0
    st.progress(score / 100)
    st.write(f"Score: {score}%")

    reasons_today={}
    if missed:
        st.subheader("Missed Reasons")
        for t in missed:
            r=st.text_input(f"{t}")
            if r:
                reasons_today[t]=r

        
    if st.button("SAVE"):

        data["history"][today_str] = score

        # ✅ BASE XP
        data["points"] += score
        data["xp"] += score

        st.success(f"📈 Base XP +{score}")

        # 💪 WORKOUT BONUS
        if workout_done == len(workout_tasks):
            st.balloons()
            st.success("💪 FULL WORKOUT DONE!")
            st.info("🔥 +50 XP BONUS")
            data["xp"] += 50
            data["points"] += 50

        # 💯 FULL DAY BONUS
        if score == 100:
            st.balloons()
            st.success("🏆 PERFECT DAY!")
            st.info("🚀 +100 XP BONUS")
            data["xp"] += 100
            data["points"] += 100

        # ❌ SMART PENALTY (task-based)
        penalty = 0

        for t in missed:
            penalty += task_xp.get(t, 5)  # default 5

        if penalty > 0:
            data["xp"] -= penalty
            data["points"] -= penalty

            st.warning(f"⚠️ Missed Tasks: {len(missed)}")
            st.error(f"❌ -{penalty} XP (based on tasks)")
        # ❌ prevent negative XP
        if data["xp"] < 0:
            data["xp"] = 0
            
        save(data)

        st.info(f"🔥 TOTAL XP: {data['xp']}")
        data["reasons"][today_str]={
            "time":datetime.now().strftime("%H:%M"),
            "tasks":reasons_today
          }
        save(data)
        st.success(f"Successfully Saved +{score} Points 🔥")
        
    st.markdown("---")
    st.subheader("🔒 Final Submit")

    locked = today_str in data.get("locked_days", [])

    if locked:
        st.error("🔒 Today already FINAL SAVED! Editing disabled ❌")
    else:
        st.write(f"🧠 Solve this CAPTCHA to FINAL SAVE: {st.session_state.captcha_q}")
        captcha_input = st.text_input("Enter Answer")

        if st.button("FINAL SAVE 💀"):

            if captcha_input != st.session_state.captcha_ans:
                st.error("❌ Wrong Answer! Try again 😈")
            else:
                # Final save
                data["history"][today_str] = score
                data["final_submitted"][today_str] = True
                data["locked_days"].append(today_str)

                save(data)

                st.success("🔥 FINAL SAVE DONE! Locked for today 🔒")

                # Reset captcha for next day
                del st.session_state["captcha_q"]
                del st.session_state["captcha_ans"]

                st.rerun()

elif choice == "📊 Stats":
    
    st.title("📊 Stats")

    # 🔥 XP DISPLAY FORMAT
    MAX_XP = 10000
    st.write(f"🔥 XP: {data['xp']} / {MAX_XP}")

    # progress bar
    MAX_XP = 10000

    # ❌ prevent negative XP
    data["xp"] = max(0, data["xp"])

    # ✅ safe progress calculation
    progress_value = data["xp"] / MAX_XP
    progress_value = max(0.0, min(progress_value, 1.0))

    st.write(f"🔥 XP: {data['xp']} / {MAX_XP}")
    st.progress(progress_value)

    history=data.get("history",{})

    if history:
        dates=list(history.keys())
        scores=list(history.values())

        st.plotly_chart(px.line(x=dates,y=scores,title="📈 Growth"))

        today_score = history.get(today_str,0)

        st.subheader("Daily Performance")
        st.plotly_chart(px.pie(
            values=[today_score,100-today_score],
            names=["Completed","Pending"]
        ))

elif choice == "📜 History":

    for d,s in data["history"].items():
        st.markdown(f"<div class='card'>{d} - Score: {s}</div>",unsafe_allow_html=True)

        if d in data["reasons"]:
            r=data["reasons"][d]
            st.write("Time:",r["time"])

            for t,rs in r["tasks"].items():
                st.write(f"{t} → {rs}")

elif choice == "📄 Report":

    st.title("📄 📊 Daily Report 📈")

    if today_str in data["history"]:
        score=data["history"][today_str]
        reasons=data["reasons"].get(today_str,{})

        report=f"""
Name: {data['name']}
Date: {today_str}
Level: {level}
Points: {data['points']}

Score: {score}

"""

        if "tasks" in reasons:
            report+="Missed Tasks:\n"
            for t,r in reasons["tasks"].items():
                report+=f"{t} → {r}\n"

        st.text_area("Report",report,height=300)
        st.download_button("Download Report",report,f"report_{today_str}.txt")

elif choice == "🧑 Profile":

    st.title("🧑 Profile")

    name=st.text_input("Name",value=data["name"])
    avatar=st.selectbox("Avatar",["😎","🔥","👑","💪"])
    dream=st.text_input("Dream",value=data.get("dream",""))

    st.markdown(f"### Preview: {avatar} {name}")

    if st.button("SAVE"):
        data["name"]=name
        data["avatar"]=avatar
        data["dream"]=dream
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
    st.progress(min(data["xp"] / 1000, 1.0))

    st.markdown("---")
    st.subheader("📅 Progress Info")

    st.write(f"🔥 Total Days Tracked: {len(data.get('history', {}))}")
    st.write(f"🔒 Locked Days: {len(data.get('locked_days', []))}")
    st.write(f"⏳ Remaining Days: {365 - (len(data.get('history', {})))}")
    
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

        else:
            st.markdown(f"""
            <div class='card'>
            <h2>🔒 Locked Badge</h2>
            <p>Unlock at Level {lvl}</p>
            <p>🎁 Reward: +{reward}</p>
            </div>
            """, unsafe_allow_html=True)
            
elif choice == "⚙️ Settings":

    st.markdown("<div class='card'>⚙️ Settings Panel</div>", unsafe_allow_html=True)

    pwd = st.text_input("Enter Password", type="password")

    # ⚠️ CONFIRM CHECKBOX (NEW ADD)
    confirm = st.checkbox("⚠️ Are you sure you want to reset ALL data?")

    if st.button("RESET ALL DATA 💀"):

        if not confirm:
            st.warning("⚠️ Please confirm reset")
        
        elif pwd == "h1a2r3i4s5h6":

            # 🔥 FULL RESET DATA
            reset_data = {
                "points": 0,
                "xp": 0,
                "streak": 0,
                "last": "",
                "avatar": "😎",
                "name": "Player",
                "dream": "",
                "history": {},
                "reasons": {},
                "start_date": str(date.today()),
                "locked_days": []
            }

            # 💾 SAVE CLEAN FILE
            with open(DATA_FILE, "w") as f:
                json.dump(reset_data, f)

            # 🔥 CLEAR SESSION
            st.session_state.clear()

            st.success("💀 FULL RESET DONE")
            st.warning("🔄 Reloading App...")

            st.rerun()

        else:
            st.error("❌ Wrong Password")
