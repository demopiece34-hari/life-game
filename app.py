import streamlit as st
import json, os
from datetime import date
import plotly.express as px

st.set_page_config(page_title="Life Game GOD MODE 😈", layout="wide")

# ---------- DATA ----------
DATA_FILE = "data.json"

def load():
    default = {
        "points": 0, "streak": 0, "last": "", "xp": 0,
        "avatar": "😎", "history": {}, "badges": []
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

# ---------- NAV ----------
menu = ["🏠 Dashboard","🎮 Missions","📊 Stats","🧑 Profile","⚙️ Settings"]
choice = st.sidebar.radio("Navigation", menu)

# ---------- SIDEBAR ----------
level = data["xp"] // 100
st.sidebar.markdown(f"# {data['avatar']} LEVEL {level}")
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

# ---------- DASHBOARD ----------
if choice == "🏠 Dashboard":
    st.title("🎯 LIFE GAME GOD MODE")

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

    for group, tasks in task_groups.items():
        with st.expander(group):
            for t in tasks:
                total += 1
                key = f"{today}_{t}"
                if st.checkbox(t, key=key):
                    done += 1

    score = int((done/total)*100)

    st.progress(score/100)
    st.write(f"🎯 Score: {score}")

    # ---------- BADGES ----------
    if score == 100 and "PERFECT" not in data["badges"]:
        data["badges"].append("🏆 PERFECT DAY")

    if score >= 70 and "CONSISTENT" not in data["badges"]:
        data["badges"].append("🔥 CONSISTENT")

    if st.button("💾 SAVE"):
        earn = done * 10
        data["xp"] += earn
        data["points"] += earn
        data["last"] = today
        data["history"][today] = score
        save(data)

        st.success(f"🔥 +{earn} XP!")

# ---------- STATS ----------
elif choice == "📊 Stats":

    st.title("📊 Weekly Stats")

    history = data.get("history", {})

    if history:
        dates = list(history.keys())[-7:]
        scores = [history[d] for d in dates]

        fig = px.line(x=dates, y=scores, markers=True)
        st.plotly_chart(fig)
    else:
        st.info("No data")

# ---------- PROFILE ----------
elif choice == "🧑 Profile":

    st.title("🧑 Profile")

    avatars = ["😎","🔥","👑","💪","🤖"]

    selected = st.selectbox("Choose Avatar", avatars)

    if st.button("SAVE AVATAR"):
        data["avatar"] = selected
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

    st.title("⚙️ Settings - Reset System")

    password = st.text_input("Enter Password", type="password")

    if st.button("RESET ALL DATA"):
        if password == "h1a2r3i4s5h6":

            reset_data = {
                "points": 0,
                "streak": 0,
                "last": "",
                "xp": 0,
                "avatar": "😎",
                "history": {},
                "badges": []
            }

            save(reset_data)

            st.success("✅ FULL RESET DONE")
            st.warning("Restart App 🔄")

        else:
            st.error("❌ Wrong Password")
