import streamlit as st
import json, os
import random
from datetime import date, datetime, timedelta
import plotly.express as px
st.set_page_config(page_title="Life Game GOD MODE ðŸ˜ˆ", layout="wide")

# ---------- LOGIN ----------
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("ðŸ” Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("LOGIN"):
        if user == "hari" and pwd == "9442176514":
            st.session_state.login = True
            st.success("Login Success â›“ï¸â€ðŸ’¥")
        else:
            st.error("Wrong credentials ðŸ”—")
    st.stop()

# ---------- DATA ----------
DATA_FILE = "data.json"

def load():
    default = {
        "points": 0,
        "xp": 0,
        "ma001_last": "",
        "ma001_strict": True,
        "streak": 0,
        "last": "",
        "avatar": "ðŸ˜Ž",
        "name": "Player",
        "dream": "",
        "history": {},
        "badges": [],
        "reasons": {},
        "start_date": str(date.today()),
        "final_submitted": {},
        "locked_days": [],
    }

    if not os.path.exists(DATA_FILE):
        return default

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except:
        # ðŸ”¥ if file corrupted â†’ reset safely
        return default

    # missing keys fix
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
    10: ("ðŸªµ", "Marakattai", 50),
    20: ("ðŸ¥ˆ", "Silver", 100),
    30: ("ðŸ¥ˆ", "Silver II", 150),
    40: ("ðŸ’Ž", "Platinum", 200),
    50: ("ðŸ’Ž", "Platinum II", 250),
    60: ("ðŸ”·", "Diamond", 300),
    70: ("ðŸ‘‘", "Master", 400),
    80: ("ðŸ§ ", "Elite", 500),
    90: ("âš¡", "Elite Master", 700),
    100: ("ðŸ”¥", "GOD MODE", 1000)
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
        st.success(f"ðŸŽ‰ {icon} {name} UNLOCKED!")
        st.info(f"ðŸ’° Reward: +{reward} XP & Points ðŸ”¥")

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
menu = ["ðŸ  Dashboard","ðŸŽ® Missions","ðŸ“Š Stats","ðŸ“œ History","ðŸ“„ Report","ðŸ§‘ Profile","ðŸ† Badges","âš™ï¸ Settings"]
choice = st.sidebar.radio("Navigation", menu)

# ---------- TASKS ----------
weekday = today.strftime("%A")

task_groups = {
    "Morning": ["Wake 5:30","Brush","Bath","Prayer","Washing"],

    "Workout ðŸ’ª": [
        "Walking (40min) ðŸš¶",
        "Exercise (30min) ðŸ‹ï¸",
        "Kegel Exercise ðŸ§ ",
        "Breathing ðŸŒ¬ï¸"
    ],

    "Learning ðŸ“š": [
        "Python (30min)",
        "English (15min)",
        "Reading (1hr)"
    ],

    "Health ðŸ¥—": [
        "Water 2L ðŸŒŠ",
        "No Junk Food ðŸŒ®"
    ],

    "Control ðŸŽ¯": [
        "MA001",
        "PN002"
    ],

    "Limited Control â³": [
        "Instagram (20min)",
        "YouTube (20min)"
    ]
}

if weekday == "Saturday":
    task_groups["Weekend"] = ["Movie ðŸŽ¬"]

if weekday == "Sunday":
    task_groups["Weekend"] = ["Oil Bath ðŸ›"]
    
# ---------- MA001 CONTROL ----------
def is_ma001_allowed():
    if days_passed < 30:
        return False

    last_done = data.get("ma001_last", "")

    if last_done:
        last_date = datetime.strptime(last_done, "%Y-%m-%d").date()
        diff = (today - last_date).days
        return diff >= 4
    return True
    
# ---------- TASK XP VALUES ----------
task_xp = {
    "Wake 5:30": 10,
    "Brush": 5,
    "Bath": 5,
    "Prayer": 10,

    "Walking (40min) ðŸš¶": 20,
    "Exercise (30min) ðŸ‹ï¸": 25,
    "Kegel Exercise ðŸ§ ": 15,
    "Breathing ðŸŒ¬ï¸": 10,

    "Python": 20,
    "English": 15,
    "Reading": 15,

    "Water 2L": 10,
    "No Junk": 20
}

# ---------- NAVIGATION HANDLER (Corrected Order) ----------
if choice == "ðŸ  Dashboard":

    st.title("ðŸŽ¯ LIFE GAME")

    st.markdown(f"""
    <div class='card'>
    <h1 style='text-align:center;font-size:70px;animation:float 3s infinite;'>{data['avatar']}</h1>
    <h2 style='text-align:center;'>{data['name']}</h2>
    <h3 style='text-align:center;'>Level {level}/100</h3>
    <p style='text-align:center;'>ðŸŽ¯ Remaining Days: {remaining_days}</p>
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
        ðŸ“… {current_day} | {current_date}
    </div>
    """, unsafe_allow_html=True)

elif choice == "ðŸŽ® Missions":

    st.title("ðŸŽ® Missions")

    done = 0
    total = 0
    missed = []

    locked = today_str in data.get("locked_days", [])
    
    workout_tasks = [
        "Walking (40min) ðŸš¶",
        "Exercise (30min) ðŸ‹ï¸",
        "Kegel Exercise ðŸ§ ",
        "Breathing ðŸŒ¬ï¸"
    ]

    workout_done = 0
    completed=[]
    
    # ---------- WORKOUT TASK LIST ----------
    workout_tasks = [
        "Walking (40min) ðŸš¶",
        "Exercise (30min) ðŸ‹ï¸",
        "Kegel Exercise ðŸ§ ",
        "Breathing ðŸŒ¬ï¸"
    ]

    workout_done = 0

    for g, tasks in task_groups.items():
        st.subheader(g)

        for t in tasks:
            total += 1
            
            if t == "MA001":

                allowed = is_ma001_allowed()

                if days_passed < 30:
                    st.warning("âš ï¸ First 30 days avoid (but you can track)")

                else:
                    st.info("â³ Allowed once every 4 days")

                if st.checkbox("MA001", key=f"{today_str}_{t}", disabled=locked):
                    done += 1

                    if allowed:
                        data["ma001_last"] = today_str
                else:
                    missed.append(t)

            else:
                # âœ… normal tasks
                if st.checkbox(t, key=f"{today_str}_{t}", disabled=locked):
                    done += 1

                    # ðŸ’ª workout tracking
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

        st.success("âœ… Progress Saved (Temporary)")

        st.session_state.temp_score = score
        st.session_state.temp_done = done
        st.session_state.temp_missed = missed   
      
    st.markdown("---")
    st.subheader("ðŸ”’ Final Submit")

    locked = today_str in data.get("locked_days", [])

    if locked:
        st.error("ðŸ”’ Today already FINAL SAVED! Editing disabled âŒ")
    else:
        st.write(f"ðŸ§  Solve this CAPTCHA to FINAL SAVE: {st.session_state.captcha_q}")
        captcha_input = st.text_input("Enter Answer")

        if st.button("FINAL SAVE ðŸ’€"):

            # âŒ Wrong captcha
            if captcha_input != st.session_state.captcha_ans:
                st.error("âŒ Wrong Answer! Try again ðŸ˜ˆ")

            # âœ… Correct captcha â†’ FINAL SAVE
            else:
                final_score = st.session_state.get("temp_score", score)
                final_missed = st.session_state.get("temp_missed", missed)

                # save history
                data["history"][today_str] = final_score

                # XP
                data["xp"] += final_score
                data["points"] += final_score

                # workout bonus
                if workout_done == len(workout_tasks):
                    data["xp"] += 50
                    data["points"] += 50

                # perfect day
                if final_score == 100:
                    data["xp"] += 100
                    data["points"] += 100

                # penalty
                penalty = 0
                for t in final_missed:
                    penalty += task_xp.get(t, 5)

                data["xp"] -= penalty
                data["points"] -= penalty

                # MA001
                if "MA001" not in final_missed:
                    data["xp"] += 30
                    data["points"] += 30
                else:
                    data["xp"] -= 30
                    data["points"] -= 30

                # reasons
                data["reasons"][today_str] = {
                    "time": datetime.now().strftime("%H:%M"),
                    "tasks": reasons_today
                }

                # ðŸ”’ lock day
                data["locked_days"].append(today_str)

                save(data)

                st.success("ðŸ”¥ FINAL SAVE DONE! Locked for today ðŸ”’")

                # reset captcha
                del st.session_state["captcha_q"]
                del st.session_state["captcha_ans"]

                st.rerun()

                st.success("ðŸ”¥ FINAL SAVE DONE! Locked for today ðŸ”’")

                # Reset captcha for next day
                del st.session_state["captcha_q"]
                del st.session_state["captcha_ans"]

                st.rerun()

elif choice == "ðŸ“Š Stats":
    
    st.title("ðŸ“Š Stats")

    # ðŸ”¥ XP DISPLAY FORMAT
    MAX_XP = 10000
    st.write(f"ðŸ”¥ XP: {data['xp']} / {MAX_XP}")

    # progress bar
    MAX_XP = 10000

    # âŒ prevent negative XP
    data["xp"] = max(0, data["xp"])

    # âœ… safe progress calculation
    progress_value = data["xp"] / MAX_XP
    progress_value = max(0.0, min(progress_value, 1.0))

    st.progress(progress_value)

    history=data.get("history",{})

    if history:
        dates=list(history.keys())
        scores=list(history.values())

        st.plotly_chart(px.line(x=dates,y=scores,title="ðŸ“ˆ Growth"))

        today_score = history.get(today_str,0)

        st.subheader("Daily Performance")
        st.plotly_chart(px.pie(
            values=[today_score,100-today_score],
            names=["Completed","Pending"]
        ))

elif choice == "ðŸ“œ History":

    for d,s in data["history"].items():
        st.markdown(f"<div class='card'>{d} - Score: {s}</div>",unsafe_allow_html=True)

        if d in data["reasons"]:
            r=data["reasons"][d]
            st.write("Time:",r["time"])

            for t,rs in r["tasks"].items():
                st.write(f"{t} â†’ {rs}")

elif choice == "ðŸ“„ Report":

    st.title("ðŸ“„ ðŸ“Š Daily Report ðŸ“ˆ")

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
                report+=f"{t} â†’ {r}\n"

        st.text_area("Report",report,height=300)
        st.download_button("Download Report",report,f"report_{today_str}.txt")

elif choice == "ðŸ§‘ Profile":

    st.title("ðŸ§‘ Profile")

    name=st.text_input("Name",value=data["name"])
    avatar=st.selectbox("Avatar",["ðŸ˜Ž","ðŸ”¥","ðŸ‘‘","ðŸ’ª"])
    dream=st.text_input("Dream",value=data.get("dream",""))

    st.markdown(f"### Preview: {avatar} {name}")

    if st.button("SAVE"):
        data["name"]=name
        data["avatar"]=avatar
        data["dream"]=dream
        save(data)
        st.success("Profile Saved âœ…")
    st.subheader("ðŸ† Your Badges")

    if data["badges"]:
        for b in data["badges"]:
            st.write(f"ðŸ… {b}")
    else:
        st.write("No badges unlocked yet ðŸ”’")

    st.subheader("ðŸ”¥ XP Progress")

    st.write(f"Total XP: {data['xp']}")
    xp = max(0, data["xp"])  # âŒ negative avoid
    progress = xp / 1000

    # âœ… clamp between 0 and 1
    progress = max(0.0, min(progress, 1.0))

    st.progress(progress)

    st.markdown("---")
    st.subheader("ðŸ“… Progress Info")

    st.write(f"ðŸ”¥ Total Days Tracked: {len(data.get('history', {}))}")
    st.write(f"ðŸ”’ Locked Days: {len(data.get('locked_days', []))}")
    st.write(f"â³ Remaining Days: {365 - (len(data.get('history', {})))}")
    
elif choice == "ðŸ† Badges":

    st.title("ðŸ† Your Badges")

    if not data["badges"]:
        st.warning("ðŸ”’ All badges are LOCKED. Level up to unlock!")

    for lvl, (icon, name, reward) in BADGE_RULES.items():

        if name in data["badges"]:
            st.markdown(f"""
            <div class='card'>
            <h2>{icon} {name} (Level {lvl})</h2>
            <p style='color:lightgreen;'>UNLOCKED âœ…</p>
            <p>ðŸŽ Reward Earned: +{reward}</p>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown(f"""
            <div class='card'>
            <h2>ðŸ”’ Locked Badge</h2>
            <p>Unlock at Level {lvl}</p>
            <p>ðŸŽ Reward: +{reward}</p>
            </div>
            """, unsafe_allow_html=True)
            
elif choice == "âš™ï¸ Settings":

    st.markdown("<div class='card'>âš™ï¸ Settings Panel</div>", unsafe_allow_html=True)

    pwd = st.text_input("Enter Password", type="password")

    # âš ï¸ CONFIRM CHECKBOX (NEW ADD)
    confirm = st.checkbox("âš ï¸ Are you sure you want to reset ALL data?")

    if st.button("RESET ALL DATA ðŸ’€"):

        if not confirm:
            st.warning("âš ï¸ Please confirm reset")
        
        elif pwd == "h1a2r3i4s5h6":

            # ðŸ”¥ FULL RESET DATA
            reset_data = {
                "points": 0,
                "xp": 0,
                "ma001_last": "",
                "ma001_strict": True,
                "streak": 0,
                "last": "",
                "avatar": "ðŸ˜Ž",
                "name": "Player",
                "dream": "",
                "history": {},
                "badges": [],
                "reasons": {},
                "start_date": str(date.today()),
                "locked_days": [],
                "final_submitted": {},
            }

            # ðŸ’¾ SAVE CLEAN FILE
            with open(DATA_FILE, "w") as f:
                json.dump(reset_data, f)

            # ðŸ”¥ CLEAR SESSION
            st.session_state.clear()

            st.success("ðŸ’€ FULL RESET DONE")
            st.warning("ðŸ”„ Reloading App...")

            st.rerun()

        else:
            st.error("âŒ Wrong Password")
