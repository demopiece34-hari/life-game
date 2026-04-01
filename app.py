import streamlit as st
import json, os
from datetime import date
import plotly.express as px

st.set_page_config(page_title="Life Game LEGEND 👑", layout="wide")

# ---------- CSS (APP FEEL) ----------
st.markdown("""
<style>
/* Glow animation */
@keyframes glow {
  from { box-shadow: 0 0 5px #22c55e; }
  to { box-shadow: 0 0 20px #22c55e; }
}

/* Floating profile button */
.profile-btn {
    position: fixed;
    top: 20px;
    right: 20px;
    background: #22c55e;
    border-radius: 50%;
    width: 60px;
    height: 60px;
    text-align: center;
    font-size: 30px;
    line-height: 60px;
    cursor: pointer;
    animation: glow 1s infinite alternate;
}

/* Card */
.card {
    padding: 15px;
    border-radius: 15px;
    background: #1e293b;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# ---------- DATA ----------
DATA_FILE = "data.json"

def load():
    default = {
        "points":0,"streak":0,"last":"","xp":0,
        "avatar":"😎","name":"Player","history":{},"badges":[]
    }
    if not os.path.exists(DATA_FILE):
        return default
    data = json.load(open(DATA_FILE))
    for k in default:
        if k not in data:
            data[k]=default[k]
    return data

def save(d):
    json.dump(d, open(DATA_FILE,"w"))

data = load()
today = str(date.today())

# ---------- PROFILE BUTTON ----------
if "show_profile" not in st.session_state:
    st.session_state.show_profile = False

if st.button(f"{data['avatar']}", key="profile"):
    st.session_state.show_profile = not st.session_state.show_profile

# ---------- PROFILE POPUP ----------
if st.session_state.show_profile:
    st.markdown("### 🧑 Profile Panel")
    st.write(f"👤 Name: {data['name']}")
    st.write(f"🎮 Level: {data['xp']//100}")
    st.write(f"⚡ XP: {data['xp']}")
    st.write(f"💯 Points: {data['points']}")
    st.write(f"🔥 Streak: {data['streak']}")

# ---------- NAV (APP STYLE) ----------
page = st.selectbox("📱 Menu", ["🏠 Dashboard","🎮 Missions","📊 Stats","⚙️ Settings"])

# ---------- DASHBOARD ----------
if page == "🏠 Dashboard":
    st.title("👑 LIFE GAME LEGEND")

    st.markdown(f"""
    <div class="card">
    <h1 style='text-align:center'>{data['avatar']}</h1>
    <h3 style='text-align:center'>Welcome {data['name']}</h3>
    </div>
    """, unsafe_allow_html=True)

# ---------- MISSIONS ----------
elif page == "🎮 Missions":

    st.title("🎮 Missions")

    groups = {
        "Morning":["Wake","Brush","Bath","Prayer","Washing"],
        "Learning":["Reading","English","Python"],
        "Workout":["Walking","Exercise","Kegel"]
    }

    done=0
    total=0

    for g,tasks in groups.items():
        with st.expander(g):
            for t in tasks:
                total+=1
                if st.checkbox(t):
                    st.success(f"✅ {t}")
                    done+=1

    score=int((done/total)*100)
    st.progress(score/100)

    if st.button("SAVE"):
        earn=done*10
        data["xp"]+=earn
        data["points"]+=earn
        save(data)
        st.success(f"+{earn} XP 🔥")

# ---------- STATS ----------
elif page == "📊 Stats":
    st.title("📊 Stats")

    if data["history"]:
        fig=px.line(x=list(data["history"].keys()),
                    y=list(data["history"].values()))
        st.plotly_chart(fig)

# ---------- SETTINGS ----------
elif page == "⚙️ Settings":

    st.title("⚙️ Settings")

    name = st.text_input("Enter Name", data["name"])

    if st.button("Save Name"):
        data["name"]=name
        save(data)
        st.success("Saved!")

    st.subheader("Reset")

    pwd = st.text_input("Password", type="password")

    if st.button("RESET"):
        if pwd=="h1a2r3i4s5h6":
            save({
                "points":0,"streak":0,"last":"",
                "xp":0,"avatar":"😎","name":"Player",
                "history":{},"badges":[]
            })
            st.success("Reset Done 🔄")
        else:
            st.error("Wrong Password ❌")
