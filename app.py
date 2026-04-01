import streamlit as st
import json, os
from datetime import date, datetime, timedelta
import plotly.express as px

st.set_page_config(page_title="Life Game GOD MODE 😈", layout="wide")

# ---------- DATA ----------
DATA_FILE = "data.json"

def load():
    default = {
        "points": 0,
        "streak": 0,
        "last": "",
        "xp": 0,
        "avatar": "😎",
        "name": "Player",
        "history": {},
        "badges": []
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
today = str(date.today())

# ---------- UI STYLE ----------
st.markdown("""
<style>
body {background-color:#0f172a; color:white;}
</style>
""", unsafe_allow_html=True)

# ---------- NAV ----------
menu = ["🏠 Dashboard","🎮 Missions","📊 Stats","🧑 Profile","⚙️ Settings"]
choice = st.sidebar.radio("Navigation", menu)

# ---------- SIDEBAR ----------
level = data["xp"] // 100
xp_current = data["xp"] % 100

st.sidebar.markdown(f"# {data['avatar']} {data['name']}")
st.sidebar.write(f"🏆 Level: {level}")
st.sidebar.progress(xp_current / 100)
st.sidebar.write(f"⚡ XP: {data['xp']}")
st.sidebar.write(f"💯 Points: {data['points']}")
st.sidebar.write(f"🔥 Streak: {data['streak']}")

# ---------- TASKS ----------
task_groups = {
    "Morning": ["Wake 5:30","Brush","Bath","Prayer","Washing"],
    "Learning": ["Reading","English","Python"],
    "Health": ["Water 2L","No Junk"],
    "Workout": ["Walking","Exercise","Kegel"],
    "Control": ["MA001","PN002"],
    "Entertainment": ["YouTube","Instagram","Movie"],
    "Weekend": ["Oil Bath"]
}

# Task XP weight
task_points = {
    "Wake 5:30": 20,
    "Python": 25,
    "Exercise": 20,
    "No Junk": 15
}

# ---------- DASHBOARD ----------
if choice == "🏠 Dashboard":

    st.title("🎯 LIFE GAME GOD MODE 😈")

    st.markdown(f"""
    <h1 style='font-size:80px; text-align:center; animation: float 2s infinite;'>
    {data['avatar']}
    </h1>
    <style>
    @keyframes float {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-20px); }}
        100% {{ transform: translateY(0px); }}
    }}
    </style>
    """, unsafe_allow_html=True)

    st.success("🔥 Stay Consistent!")

# ---------- MISSIONS ----------
elif choice == "🎮 Missions":

    st.title("🎮 Daily Missions")

    done = 0
    total = 0
    completed_tasks = []

    for group, tasks in task_groups.items():
        with st.expander(group):
            for t in tasks:
                total += 1
                key = f"{today}_{t}"
                if st.checkbox(t, key=key):
                    done += 1
                    completed_tasks.append(t)

    score = int((done/total)*100)
    st.progress(score/100)
    st.write(f"🎯 Score: {score}")

    # ---------- FEEDBACK ----------
    if score == 100:
        st.balloons()
        st.success("😈 GOD MODE PERFECT!")
    elif score >= 70:
        st.info("🔥 Good consistency!")
    elif score >= 40:
        st.warning("⚠️ Improve tomorrow!")
    else:
        st.error("💀 Focus bro!")

    # ---------- SAVE ----------
    if st.button("💾 SAVE"):

        # XP calculation
        earn = sum(task_points.get(t, 10) for t in completed_tasks)

        data["xp"] += earn
        data["points"] += earn
        data["history"][today] = score

        # ---------- STREAK ----------
        last = data.get("last", "")
        if last:
            last_date = datetime.strptime(last, "%Y-%m-%d").date()
            if date.today() == last_date + timedelta(days=1):
                data["streak"] += 1
            elif date.today() != last_date:
                data["streak"] = 1
        else:
            data["streak"] = 1

        data["last"] = today

        # ---------- BADGES ----------
        if score == 100 and "🏆 PERFECT DAY" not in data["badges"]:
            data["badges"].append("🏆 PERFECT DAY")

        if score >= 70 and "🔥 CONSISTENT" not in data["badges"]:
            data["badges"].append("🔥 CONSISTENT")

        if data["streak"] >= 7 and "🔥 7 DAY STREAK" not in data["badges"]:
            data["badges"].append("🔥 7 DAY STREAK")

        if data["xp"] >= 1000 and "👑 ELITE" not in data["badges"]:
            data["badges"].append("👑 ELITE")

        save(data)
        st.success(f"🔥 +{earn} XP Saved!")

# ---------- STATS ----------
elif choice == "📊 Stats":

    st.title("📊 Weekly Stats")

    history = data.get("history", {})

    if history:
        dates = list(history.keys())[-7:]
        scores = [history[d] for d in dates]

        fig = px.area(x=dates, y=scores, title="Performance Trend")
        st.plotly_chart(fig, use_container_width=True)

        avg = sum(scores) / len(scores)

        if avg < 50:
            st.error("⚠️ Low performance")
        elif avg > 80:
            st.success("🔥 Elite consistency!")
    else:
        st.info("No data")

# ---------- PROFILE ----------
elif choice == "🧑 Profile":

    st.title("🧑 Profile")

    name = st.text_input("Enter Name", value=data["name"])

    avatars = ["😎","🔥","👑","💪","🤖"]
    selected = st.selectbox("Choose Avatar", avatars)

    if st.button("SAVE PROFILE"):
        data["avatar"] = selected
        data["name"] = name
        save(data)
        st.success("Updated!")

    st.subheader("🏆 Badges")
    if data["badges"]:
        for b in data["badges"]:
            st.success(b)
    else:
        st.info("No badges yet")

# ---------- SETTINGS ----------
elif choice == "⚙️ Settings":

    st.title("⚙️ Settings")

    password = st.text_input("Enter Password", type="password")

    if st.button("RESET ALL DATA"):
        if password == "h1a2r3i4s5h6":
            reset_data = {
                "points": 0,
                "streak": 0,
                "last": "",
                "xp": 0,
                "avatar": "😎",
                "name": "Player",
                "history": {},
                "badges": []
            }
            save(reset_data)
            st.success("✅ FULL RESET DONE")
        else:
            st.error("❌ Wrong Password")
