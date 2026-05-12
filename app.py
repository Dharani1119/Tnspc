import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random, time, datetime

# ─────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TNPSC Coach — Smart Exam Preparation",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html,body,[class*="css"],.stApp{
  font-family:'Inter',sans-serif!important;
  background:#0C0E1A!important;color:#F1F5F9!important;
}
.stApp{background:#0C0E1A!important;}
.block-container{padding:1.5rem 2rem 4rem!important;max-width:1100px!important;}
#MainMenu,footer,.stDeployButton,[data-testid="stToolbar"]{visibility:hidden!important;}
header[data-testid="stHeader"]{background:rgba(12,14,26,.97)!important;border-bottom:1px solid rgba(255,255,255,.06)!important;}

/* sidebar */
section[data-testid="stSidebar"]{background:#0F1120!important;border-right:1px solid rgba(255,255,255,.06)!important;}
section[data-testid="stSidebar"] .block-container{padding:1rem 0.75rem 2rem!important;}

/* metrics */
[data-testid="metric-container"]{background:#141626!important;border:1px solid rgba(255,255,255,.07)!important;border-radius:14px!important;padding:16px 18px!important;}
[data-testid="metric-container"] label{color:#475569!important;font-size:10px!important;font-weight:700!important;letter-spacing:.8px!important;text-transform:uppercase!important;}
[data-testid="stMetricValue"]{color:#F1F5F9!important;font-size:24px!important;font-weight:700!important;letter-spacing:-.5px!important;}
[data-testid="stMetricDelta"]{font-size:11px!important;}

/* buttons */
.stButton>button{
  background:linear-gradient(135deg,#4F46E5,#7C3AED)!important;
  color:#fff!important;border:none!important;border-radius:12px!important;
  font-weight:600!important;font-size:13px!important;padding:10px 20px!important;
  font-family:'Inter',sans-serif!important;
  box-shadow:0 4px 16px rgba(79,70,229,.3)!important;
}
.stButton>button:hover{opacity:.88!important;}

/* tabs */
.stTabs [data-baseweb="tab-list"]{background:#141626!important;border-radius:12px!important;padding:4px!important;gap:3px!important;border:1px solid rgba(255,255,255,.06)!important;}
.stTabs [data-baseweb="tab"]{background:transparent!important;color:#6B7280!important;border-radius:9px!important;font-size:12px!important;font-weight:500!important;padding:7px 13px!important;}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,#4F46E5,#7C3AED)!important;color:#fff!important;}

/* inputs */
.stTextInput>div>div,.stSelectbox>div>div,.stNumberInput>div>div{background:#141626!important;border:1px solid rgba(255,255,255,.1)!important;border-radius:12px!important;}
.stTextInput input,.stNumberInput input{color:#F1F5F9!important;font-family:'Inter',sans-serif!important;font-size:13px!important;}
.stSelectbox select{color:#F1F5F9!important;}
.stTextInput input::placeholder{color:#374151!important;}

/* radio */
.stRadio>div{gap:8px!important;}
.stRadio label{font-size:13px!important;}

/* progress */
.stProgress>div>div{background:linear-gradient(90deg,#4F46E5,#06B6D4)!important;border-radius:4px!important;}

/* expander */
details{background:#141626!important;border:1px solid rgba(255,255,255,.07)!important;border-radius:12px!important;padding:4px 8px!important;}
summary{color:#F1F5F9!important;font-weight:500!important;font-size:13px!important;}

/* checkbox */
.stCheckbox label{font-size:13px!important;color:#94A3B8!important;}

hr{border-color:rgba(255,255,255,.06)!important;margin:6px 0!important;}
.stAlert{border-radius:12px!important;}
.stSpinner>div{border-top-color:#4F46E5!important;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  PALETTE + PLOTLY BASE
# ─────────────────────────────────────────────────────────────
IND  = "#4F46E5"   # indigo primary
VIO  = "#7C3AED"   # violet
CYN  = "#06B6D4"   # cyan accent
GRN  = "#10B981"   # success / correct
RED  = "#EF4444"   # danger / wrong
AMB  = "#F59E0B"   # warning
SURF = "#141626"
SURF2= "#1A1D30"
MUTE = "#475569"

PL = dict(
    paper_bgcolor=SURF, plot_bgcolor=SURF,
    font=dict(family="Inter", color="#94A3B8", size=11),
    margin=dict(l=10,r=10,t=28,b=10),
    xaxis=dict(gridcolor="rgba(255,255,255,.04)", zerolinecolor="rgba(255,255,255,.04)"),
    yaxis=dict(gridcolor="rgba(255,255,255,.04)", zerolinecolor="rgba(255,255,255,.04)"),
)

# ─────────────────────────────────────────────────────────────
#  HTML HELPERS
# ─────────────────────────────────────────────────────────────
def H(s): st.markdown(s, unsafe_allow_html=True)
def gap(px=14): H(f"<div style='height:{px}px'></div>")

def watermark():
    H("""
    <div style="position:fixed;bottom:16px;right:18px;z-index:9999;
                background:rgba(12,14,26,.9);backdrop-filter:blur(10px);
                border:1px solid rgba(79,70,229,.25);border-radius:28px;
                padding:6px 14px 6px 9px;display:flex;align-items:center;gap:7px;
                pointer-events:none;user-select:none;">
        <div style="width:20px;height:20px;background:linear-gradient(135deg,#4F46E5,#7C3AED);
                    border-radius:6px;display:flex;align-items:center;justify-content:center;
                    font-size:10px;flex-shrink:0;">🎯</div>
        <div>
            <div style="font-size:11px;font-weight:700;color:#818CF8;line-height:1.2;">TNPSC Coach</div>
            <div style="font-size:9px;color:#374151;line-height:1.2;">Smart Exam Prep</div>
        </div>
    </div>""")

def page_header(icon, title, sub=""):
    H(f"""
    <div style="margin-bottom:18px;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
            <span style="font-size:22px;">{icon}</span>
            <span style="font-size:20px;font-weight:700;color:#F1F5F9;letter-spacing:-.3px;">{title}</span>
        </div>
        {"" if not sub else f'<div style="font-size:12px;color:#475569;margin-left:32px;">{sub}</div>'}
    </div>""")

def sec(label, mt=22):
    H(f"""<div style="font-size:10px;font-weight:700;letter-spacing:1px;color:#374151;
               text-transform:uppercase;margin:{mt}px 0 10px;">{label}</div>""")

def stat_card(icon, label, value, delta="", delta_color=GRN, accent=IND):
    H(f"""
    <div style="background:{SURF};border:1px solid rgba(255,255,255,.07);border-radius:14px;
                padding:16px 18px;height:100%;">
        <div style="display:flex;align-items:center;gap:7px;margin-bottom:10px;">
            <div style="width:28px;height:28px;border-radius:9px;
                        background:rgba(79,70,229,.15);color:{accent};
                        display:flex;align-items:center;justify-content:center;font-size:14px;">{icon}</div>
            <span style="font-size:10px;font-weight:700;color:{MUTE};text-transform:uppercase;letter-spacing:.6px;">{label}</span>
        </div>
        <div style="font-size:24px;font-weight:700;color:#F1F5F9;line-height:1;margin-bottom:5px;">{value}</div>
        {"" if not delta else f'<div style="font-size:11px;color:{delta_color};">{delta}</div>'}
    </div>""")

def xp_badge(xp, level, level_name, streak):
    H(f"""
    <div style="background:linear-gradient(145deg,#0E1022,#151828);
                border:1px solid rgba(79,70,229,.3);border-radius:16px;
                padding:18px 20px;margin-bottom:6px;position:relative;overflow:hidden;">
        <div style="position:absolute;top:-30px;right:-30px;width:130px;height:130px;
                    background:radial-gradient(circle,rgba(79,70,229,.12),transparent 70%);
                    border-radius:50%;pointer-events:none;"></div>
        <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">
            <div style="display:flex;align-items:center;gap:14px;">
                <div style="width:52px;height:52px;background:linear-gradient(135deg,#4F46E5,#7C3AED);
                            border-radius:14px;display:flex;align-items:center;justify-content:center;
                            font-size:22px;box-shadow:0 4px 16px rgba(79,70,229,.4);">🏆</div>
                <div>
                    <div style="font-size:11px;color:#475569;font-weight:600;letter-spacing:.5px;
                                text-transform:uppercase;margin-bottom:2px;">Level {level}</div>
                    <div style="font-size:18px;font-weight:700;color:#F1F5F9;">{level_name}</div>
                    <div style="font-size:12px;color:#818CF8;margin-top:2px;">{xp} XP total</div>
                </div>
            </div>
            <div style="display:flex;gap:14px;flex-wrap:wrap;">
                <div style="text-align:center;background:rgba(255,255,255,.05);
                            border-radius:12px;padding:10px 16px;">
                    <div style="font-size:24px;font-weight:800;color:{AMB};">🔥 {streak}</div>
                    <div style="font-size:10px;color:{MUTE};margin-top:2px;">Day Streak</div>
                </div>
                <div style="text-align:center;background:rgba(255,255,255,.05);
                            border-radius:12px;padding:10px 16px;">
                    <div style="font-size:24px;font-weight:800;color:{GRN};">82%</div>
                    <div style="font-size:10px;color:{MUTE};margin-top:2px;">Accuracy</div>
                </div>
                <div style="text-align:center;background:rgba(255,255,255,.05);
                            border-radius:12px;padding:10px 16px;">
                    <div style="font-size:24px;font-weight:800;color:{CYN};">1,450</div>
                    <div style="font-size:10px;color:{MUTE};margin-top:2px;">XP This Week</div>
                </div>
            </div>
        </div>
    </div>""")

def goal_card(done, total, subject, task):
    pct = int(done/total*100) if total else 0
    color = GRN if pct >= 100 else (CYN if pct >= 50 else IND)
    icon  = "✅" if pct >= 100 else "🔵"
    H(f"""
    <div style="background:{SURF};border:1px solid rgba(255,255,255,.07);border-radius:12px;
                padding:13px 16px;margin-bottom:8px;display:flex;align-items:center;gap:13px;">
        <div style="font-size:18px;">{icon}</div>
        <div style="flex:1;">
            <div style="font-size:13px;font-weight:600;color:#F1F5F9;margin-bottom:4px;">{task}</div>
            <div style="display:flex;align-items:center;gap:8px;">
                <div style="flex:1;height:4px;background:{SURF2};border-radius:2px;">
                    <div style="height:4px;width:{pct}%;background:{color};border-radius:2px;"></div>
                </div>
                <span style="font-size:11px;color:{MUTE};white-space:nowrap;">{done}/{total}</span>
            </div>
        </div>
        <div style="font-size:11px;font-weight:700;color:{color};">{pct}%</div>
    </div>""")

def question_card(qnum, question, options, correct_idx, explanation, show_answer=False, user_answer=None):
    H(f"""
    <div style="background:{SURF};border:1px solid rgba(255,255,255,.07);
                border-radius:16px;padding:20px 22px;margin-bottom:12px;">
        <div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:14px;">
            <div style="background:rgba(79,70,229,.15);color:#818CF8;font-size:11px;font-weight:700;
                        padding:3px 10px;border-radius:20px;white-space:nowrap;flex-shrink:0;">Q.{qnum}</div>
            <div style="font-size:14px;color:#F1F5F9;line-height:1.7;font-weight:500;">{question}</div>
        </div>
    """)
    for i, opt in enumerate(options):
        letter = ["A","B","C","D"][i]
        if show_answer:
            if i == correct_idx:
                bg = f"rgba(16,185,129,.12)"; border = GRN; col = GRN
            elif user_answer is not None and i == user_answer and i != correct_idx:
                bg = f"rgba(239,68,68,.1)"; border = RED; col = RED
            else:
                bg = "rgba(255,255,255,.03)"; border = "rgba(255,255,255,.07)"; col = MUTE
        else:
            bg = "rgba(255,255,255,.03)"; border = "rgba(255,255,255,.07)"; col = "#94A3B8"
        H(f"""
        <div style="background:{bg};border:1px solid {border};border-radius:10px;
                    padding:10px 14px;margin-bottom:7px;display:flex;align-items:center;gap:10px;">
            <div style="width:24px;height:24px;border-radius:7px;border:1px solid {border};
                        color:{col};font-size:11px;font-weight:700;display:flex;align-items:center;
                        justify-content:center;flex-shrink:0;">{letter}</div>
            <div style="font-size:13px;color:{col};">{opt}</div>
        </div>""")
    if show_answer:
        H(f"""
        <div style="margin-top:12px;background:rgba(6,182,212,.08);border-left:3px solid {CYN};
                    border-radius:0 10px 10px 0;padding:10px 14px;">
            <div style="font-size:10px;font-weight:700;color:{CYN};letter-spacing:.5px;
                        text-transform:uppercase;margin-bottom:4px;">Explanation</div>
            <div style="font-size:12px;color:#94A3B8;line-height:1.7;">{explanation}</div>
        </div>""")
    H("</div>")

def badge_chip(icon, name, desc, earned=True):
    opacity = "1" if earned else "0.35"
    H(f"""
    <div style="opacity:{opacity};background:{SURF};border:1px solid rgba(255,255,255,.07);
                border-radius:12px;padding:13px 14px;text-align:center;">
        <div style="font-size:28px;margin-bottom:6px;">{icon}</div>
        <div style="font-size:12px;font-weight:600;color:#F1F5F9;margin-bottom:3px;">{name}</div>
        <div style="font-size:10px;color:{MUTE};">{desc}</div>
    </div>""")

def result_row(subject, score, total, color):
    pct = int(score/total*100)
    H(f"""
    <div style="display:flex;align-items:center;gap:12px;padding:10px 0;
                border-bottom:1px solid rgba(255,255,255,.05);">
        <div style="font-size:13px;color:#94A3B8;flex:1;">{subject}</div>
        <div style="font-size:13px;font-weight:600;color:#F1F5F9;">{score}/{total}</div>
        <div style="width:120px;height:5px;background:{SURF2};border-radius:3px;">
            <div style="height:5px;width:{pct}%;background:{color};border-radius:3px;"></div>
        </div>
        <div style="font-size:12px;font-weight:700;color:{color};width:36px;text-align:right;">{pct}%</div>
    </div>""")

def footer():
    H("""
    <div style="text-align:center;border-top:1px solid rgba(255,255,255,.05);
                padding-top:18px;margin-top:28px;">
        <div style="display:inline-flex;align-items:center;gap:7px;margin-bottom:4px;">
            <div style="background:linear-gradient(135deg,#4F46E5,#7C3AED);width:20px;height:20px;
                        border-radius:6px;display:inline-flex;align-items:center;justify-content:center;
                        font-size:10px;">🎯</div>
            <span style="font-size:13px;font-weight:700;color:#F1F5F9;">TNPSC Coach</span>
        </div>
        <div style="font-size:11px;color:#1F2937;">
            © 2025 TNPSC Coach · Smart Exam Preparation · All rights reserved
        </div>
    </div>""")

# ─────────────────────────────────────────────────────────────
#  DEMO QUESTION BANK
# ─────────────────────────────────────────────────────────────
QUESTIONS = [
    {"id":1,"subject":"Polity","topic":"Indian Constitution","year":2022,"difficulty":"Medium",
     "question":"Which article of the Indian Constitution deals with the election of the President?",
     "options":["Article 52","Article 54","Article 58","Article 60"],
     "correct":1,"explanation":"Article 54 deals with the election of the President of India by an Electoral College consisting of elected members of both Houses of Parliament and the Legislative Assemblies of States and UTs."},
    {"id":2,"subject":"History","topic":"Medieval India","year":2021,"difficulty":"Easy",
     "question":"The Battle of Panipat (First) was fought between Babur and:",
     "options":["Rana Sanga","Ibrahim Lodi","Hemu","Sher Shah Suri"],
     "correct":1,"explanation":"The First Battle of Panipat (1526) was fought between Babur, the founder of the Mughal Empire, and Ibrahim Lodi, the last ruler of the Delhi Sultanate. Babur's victory established Mughal rule in India."},
    {"id":3,"subject":"Geography","topic":"Tamil Nadu","year":2023,"difficulty":"Easy",
     "question":"Which river forms the boundary between Tamil Nadu and Kerala?",
     "options":["Cauvery","Tamiraparani","Bhavani","Shengottai Kallaru"],
     "correct":3,"explanation":"The Shengottai Kallaru (also known as Kallada River in Kerala) region forms part of the natural boundary. However, the more commonly tested answer is that the Tamiraparani and the Western Ghats form the boundary."},
    {"id":4,"subject":"Polity","topic":"Local Governance","year":2022,"difficulty":"Hard",
     "question":"The 73rd Constitutional Amendment relates to:",
     "options":["Urban Local Bodies","Panchayati Raj Institutions","Scheduled Tribes","Financial Emergency"],
     "correct":1,"explanation":"The 73rd Constitutional Amendment (1992) gives constitutional status to Panchayati Raj Institutions (PRIs). It added Part IX and the 11th Schedule to the Constitution, mandating elections and reservations for Panchayats."},
    {"id":5,"subject":"Science","topic":"General Science","year":2021,"difficulty":"Medium",
     "question":"Which of the following is not a greenhouse gas?",
     "options":["Carbon Dioxide","Methane","Nitrogen","Nitrous Oxide"],
     "correct":2,"explanation":"Nitrogen (N₂) is not a greenhouse gas. It makes up 78% of Earth's atmosphere but does not absorb infrared radiation. Greenhouse gases include CO₂, CH₄, N₂O, and water vapor."},
    {"id":6,"subject":"Economics","topic":"Tamil Nadu Economy","year":2023,"difficulty":"Medium",
     "question":"Which district has the highest number of Special Economic Zones (SEZs) in Tamil Nadu?",
     "options":["Coimbatore","Kancheepuram","Chennai","Tiruvallur"],
     "correct":1,"explanation":"Kancheepuram district has the highest concentration of SEZs in Tamil Nadu, largely due to its proximity to Chennai and strong infrastructure for manufacturing and export."},
    {"id":7,"subject":"History","topic":"Freedom Movement","year":2020,"difficulty":"Easy",
     "question":"The Quit India Movement was launched in the year:",
     "options":["1940","1941","1942","1943"],
     "correct":2,"explanation":"The Quit India Movement was launched on August 8, 1942, at the Bombay session of the All India Congress Committee. Mahatma Gandhi gave the 'Do or Die' call, demanding immediate independence from British rule."},
    {"id":8,"subject":"Aptitude","topic":"Number Series","year":2022,"difficulty":"Medium",
     "question":"Find the missing number: 2, 6, 12, 20, 30, ?",
     "options":["40","42","44","48"],
     "correct":1,"explanation":"The pattern: differences are 4,6,8,10,12. So next = 30+12 = 42. Alternatively: n(n+1) gives 1×2=2, 2×3=6, 3×4=12, 4×5=20, 5×6=30, 6×7=42."},
]

SUBJECTS = ["All Subjects","Polity","History","Geography","Science","Economics","Aptitude","Tamil","English"]
EXAM_TYPES = ["Group 1","Group 2","Group 2A","Group 4","VAO"]
TOPICS = {"Polity":["Indian Constitution","Local Governance","Fundamental Rights","Parliament"],
          "History":["Ancient India","Medieval India","Modern India","Freedom Movement","Tamil Nadu History"],
          "Geography":["India Geography","Tamil Nadu","World Geography","Physical Geography"],
          "Science":["General Science","Physics","Chemistry","Biology","Environment"],
          "Economics":["Indian Economy","Tamil Nadu Economy","Budget","Banking"],
          "Aptitude":["Number Series","Algebra","Percentage","Time & Work","Data Interpretation"],}

# ─────────────────────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────────────────────
defaults = {
    "page": "landing",
    "user_name": "",
    "exam_type": "Group 2",
    "target_date": "",
    "daily_hours": 3,
    "weak_subjects": [],
    "onboarded": False,
    "xp": 1450,
    "level": 5,
    "streak": 14,
    "practice_q_idx": 0,
    "practice_answered": False,
    "practice_user_ans": None,
    "practice_correct": 0,
    "practice_total": 0,
    "mock_active": False,
    "mock_q_idx": 0,
    "mock_answers": {},
    "mock_submitted": False,
    "mock_score": 0,
}
for k,v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

LEVEL_NAMES = {1:"Beginner",2:"Student",3:"Aspirant",4:"Learner",5:"VAO Officer",
               6:"Block Officer",8:"Circle Inspector",10:"Deputy Collector",15:"IAS Aspirant",20:"TNPSC Legend"}
def get_level_name(lvl):
    for k in sorted(LEVEL_NAMES.keys(),reverse=True):
        if lvl >= k: return LEVEL_NAMES[k]
    return "Beginner"

# ─────────────────────────────────────────────────────────────
#  SIDEBAR NAV
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    H("""
    <div style="display:flex;align-items:center;gap:9px;padding:4px 4px 18px;">
        <div style="background:linear-gradient(135deg,#4F46E5,#7C3AED);width:30px;height:30px;
                    border-radius:9px;display:flex;align-items:center;justify-content:center;
                    font-size:15px;flex-shrink:0;">🎯</div>
        <div>
            <div style="font-size:14px;font-weight:800;color:#F1F5F9;letter-spacing:-.3px;">TNPSC Coach</div>
            <div style="font-size:10px;color:#374151;">Smart Exam Preparation</div>
        </div>
    </div>""")

    pages = [
        ("🏠","Dashboard","dashboard"),
        ("📚","PYQ Practice","practice"),
        ("📝","Mock Tests","mock"),
        ("📅","Study Planner","planner"),
        ("🔁","Revision","revision"),
        ("📊","Analytics","analytics"),
        ("🏆","Achievements","achievements"),
        ("📰","Current Affairs","current_affairs"),
    ]
    for icon,label,key in pages:
        is_active = st.session_state.page == key
        style = "font-weight:600;color:#818CF8;" if is_active else "color:#6B7280;"
        if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key
            st.session_state.onboarded = True
            st.rerun()

    H("<hr>")
    # XP bar in sidebar
    xp = st.session_state.xp
    lvl = st.session_state.level
    next_xp = (lvl + 1) * 500
    pct_xp = min(100, int(xp % 500 / 500 * 100))
    H(f"""
    <div style="background:{SURF};border:1px solid rgba(255,255,255,.07);border-radius:11px;padding:11px 13px;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
            <div style="font-size:11px;font-weight:700;color:#818CF8;">Level {lvl} · {get_level_name(lvl)}</div>
            <div style="font-size:10px;color:{MUTE};">{xp} XP</div>
        </div>
        <div style="height:5px;background:{SURF2};border-radius:3px;">
            <div style="height:5px;width:{pct_xp}%;background:linear-gradient(90deg,#4F46E5,#06B6D4);border-radius:3px;"></div>
        </div>
        <div style="font-size:10px;color:{MUTE};margin-top:4px;">{500-xp%500} XP to Level {lvl+1}</div>
    </div>""")

# ─────────────────────────────────────────────────────────────
#  LANDING / ONBOARDING
# ─────────────────────────────────────────────────────────────
if st.session_state.page == "landing" and not st.session_state.onboarded:
    watermark()
    gap(36)
    H("""
    <div style="text-align:center;max-width:620px;margin:0 auto;">
        <div style="display:inline-flex;align-items:center;gap:7px;
                    background:rgba(79,70,229,.12);color:#818CF8;font-size:11px;
                    font-weight:700;padding:6px 16px;border-radius:30px;
                    border:1px solid rgba(79,70,229,.25);margin-bottom:26px;
                    letter-spacing:.7px;text-transform:uppercase;">
            🎯 TNPSC Coach — Smart Exam Preparation
        </div>
        <h1 style="font-size:clamp(28px,5vw,46px);font-weight:800;line-height:1.15;
                   color:#FFFFFF;margin-bottom:16px;letter-spacing:-.7px;">
            Crack TNPSC with a<br>
            <span style="background:linear-gradient(135deg,#4F46E5,#06B6D4);
                         -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
                structured AI system
            </span>
        </h1>
        <p style="color:#374151;font-size:15px;max-width:480px;margin:0 auto 36px;line-height:1.8;">
            Previous year questions, mock tests, spaced revision, gamification,
            and a personalized study plan — all built for Group 1, 2 & 4 aspirants.
        </p>
    </div>""")

    _,mid,_ = st.columns([1,2,1])
    with mid:
        H('<div style="background:{};border:1px solid rgba(255,255,255,.07);border-radius:18px;padding:24px;">'.format(SURF))
        user_name  = st.text_input("Your name","",placeholder="Enter your name",key="ob_name")
        exam_type  = st.selectbox("Target exam",EXAM_TYPES,key="ob_exam")
        daily_hrs  = st.selectbox("Daily study hours",["1 hour","2 hours","3 hours","4 hours","5+ hours"],index=2,key="ob_hrs")
        weak_subs  = st.multiselect("Your weak subjects (select all that apply)",
                                     ["Polity","History","Geography","Science","Economics","Aptitude","Tamil","English"],
                                     key="ob_weak")
        gap(4)
        c1,c2 = st.columns(2)
        with c1:
            if st.button("🚀  Start my journey",use_container_width=True):
                st.session_state.user_name    = user_name or "Aspirant"
                st.session_state.exam_type    = exam_type
                st.session_state.daily_hours  = int(daily_hrs[0])
                st.session_state.weak_subjects = weak_subs
                st.session_state.onboarded    = True
                st.session_state.page         = "dashboard"
                st.rerun()
        with c2:
            if st.button("👁️  View demo",use_container_width=True):
                st.session_state.user_name    = "Demo User"
                st.session_state.exam_type    = "Group 2"
                st.session_state.weak_subjects = ["History","Aptitude"]
                st.session_state.onboarded    = True
                st.session_state.page         = "dashboard"
                st.rerun()
        H('</div>')

    gap(28)
    H("""
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;max-width:700px;margin:0 auto;">
        <div style="text-align:center;background:{s};border:1px solid rgba(255,255,255,.07);border-radius:12px;padding:16px 10px;">
            <div style="font-size:24px;margin-bottom:6px;">📚</div>
            <div style="font-size:12px;font-weight:600;color:#F1F5F9;">5,000+ PYQs</div>
            <div style="font-size:11px;color:#475569;">All subjects</div>
        </div>
        <div style="text-align:center;background:{s};border:1px solid rgba(255,255,255,.07);border-radius:12px;padding:16px 10px;">
            <div style="font-size:24px;margin-bottom:6px;">🔥</div>
            <div style="font-size:12px;font-weight:600;color:#F1F5F9;">Daily Streaks</div>
            <div style="font-size:11px;color:#475569;">Stay consistent</div>
        </div>
        <div style="text-align:center;background:{s};border:1px solid rgba(255,255,255,.07);border-radius:12px;padding:16px 10px;">
            <div style="font-size:24px;margin-bottom:6px;">🧠</div>
            <div style="font-size:12px;font-weight:600;color:#F1F5F9;">Smart Revision</div>
            <div style="font-size:11px;color:#475569;">Spaced learning</div>
        </div>
        <div style="text-align:center;background:{s};border:1px solid rgba(255,255,255,.07);border-radius:12px;padding:16px 10px;">
            <div style="font-size:24px;margin-bottom:6px;">📊</div>
            <div style="font-size:12px;font-weight:600;color:#F1F5F9;">Analytics</div>
            <div style="font-size:11px;color:#475569;">Know your gaps</div>
        </div>
    </div>""".replace("{s}",SURF))
    footer()

# ─────────────────────────────────────────────────────────────
#  MAIN PAGES (post-onboarding)
# ─────────────────────────────────────────────────────────────
elif st.session_state.onboarded:
    watermark()
    page = st.session_state.page
    if page == "landing": page = "dashboard"
    user  = st.session_state.user_name
    exam  = st.session_state.exam_type
    xp    = st.session_state.xp
    lvl   = st.session_state.level
    streak= st.session_state.streak

    # ════════════════════════════════════════════
    #  DASHBOARD
    # ════════════════════════════════════════════
    if page == "dashboard":
        page_header("🏠","Dashboard",f"Welcome back, {user}! Ready for {exam}?")
        xp_badge(xp, lvl, get_level_name(lvl), streak)
        gap(4)

        c1,c2,c3,c4 = st.columns(4)
        with c1: stat_card("📚","Questions today","42/50","10 remaining",AMB)
        with c2: stat_card("✅","Accuracy","82%","+3% this week",GRN,GRN)
        with c3: stat_card("⏱️","Study today","2h 15m","Goal: 3h",CYN,CYN)
        with c4: stat_card("📝","Mock score","78/100","+5 vs last mock",IND)

        sec("Today's Goals")
        goal_card(20,20,"Polity","Polity PYQs — Constitutional Articles")
        goal_card(15,20,"History","History Practice — Medieval Period")
        goal_card(0, 1, "Mock","Evening Mock Test at 7 PM")
        goal_card(10,10,"Revision","Revise Geography — Rivers & Dams ✅")

        c1,c2 = st.columns([3,2])
        with c1:
            sec("Weekly study hours")
            days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
            hrs  = [2.5,3.1,2.0,3.5,2.8,4.0,2.2]
            goal = [3]*7
            fig = go.Figure()
            fig.add_trace(go.Bar(x=days,y=hrs,marker_color=IND,marker_line_width=0,name="Studied",
                                  hovertemplate="%{x}: %{y}h<extra></extra>"))
            fig.add_trace(go.Scatter(x=days,y=goal,mode="lines",line=dict(color=CYN,width=2,dash="dot"),name="Goal"))
            fig.update_layout(**PL,height=220,showlegend=False)
            fig.update_yaxes(ticksuffix="h")
            st.plotly_chart(fig,use_container_width=True)

        with c2:
            sec("Subject accuracy")
            subs_acc = {"Polity":88,"Geography":74,"Science":81,"History":65,"Aptitude":58,"Economics":77}
            for sub,acc in subs_acc.items():
                color = GRN if acc>=80 else (AMB if acc>=65 else RED)
                H(f"""
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
                    <div style="font-size:12px;color:#94A3B8;width:80px;flex-shrink:0;">{sub}</div>
                    <div style="flex:1;height:5px;background:{SURF2};border-radius:3px;">
                        <div style="height:5px;width:{acc}%;background:{color};border-radius:3px;"></div>
                    </div>
                    <div style="font-size:11px;font-weight:700;color:{color};width:32px;text-align:right;">{acc}%</div>
                </div>""")

        sec("Upcoming mock tests")
        H(f"""
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
            <div style="background:{SURF};border:1px solid rgba(79,70,229,.25);border-radius:12px;padding:14px 16px;">
                <div style="font-size:10px;color:{IND};font-weight:700;letter-spacing:.5px;text-transform:uppercase;margin-bottom:6px;">Tonight</div>
                <div style="font-size:14px;font-weight:600;color:#F1F5F9;margin-bottom:4px;">Full Mock Test #12</div>
                <div style="font-size:12px;color:{MUTE};">200 Questions · 3 Hours · 7:00 PM</div>
            </div>
            <div style="background:{SURF};border:1px solid rgba(255,255,255,.07);border-radius:12px;padding:14px 16px;">
                <div style="font-size:10px;color:{MUTE};font-weight:700;letter-spacing:.5px;text-transform:uppercase;margin-bottom:6px;">Sunday</div>
                <div style="font-size:14px;font-weight:600;color:#F1F5F9;margin-bottom:4px;">Polity Subject Test</div>
                <div style="font-size:12px;color:{MUTE};">50 Questions · 1 Hour · 10:00 AM</div>
            </div>
        </div>""")

    # ════════════════════════════════════════════
    #  PYQ PRACTICE
    # ════════════════════════════════════════════
    elif page == "practice":
        page_header("📚","PYQ Practice Hub","Previous Year Questions — all TNPSC exams")

        tab1,tab2,tab3 = st.tabs(["🎯 Practice","📋 Question Bank","🔖 Bookmarks"])

        with tab1:
            c1,c2,c3,c4 = st.columns(4)
            with c1: subj_filter = st.selectbox("Subject",SUBJECTS,key="pf_sub")
            with c2: mode = st.selectbox("Mode",["Quick Practice","Topic Practice","Timed Practice","Weak Topic"],key="pf_mode")
            with c3: diff = st.selectbox("Difficulty",["All","Easy","Medium","Hard"],key="pf_diff")
            with c4: yr   = st.selectbox("Year",["All","2023","2022","2021","2020","2019"],key="pf_yr")

            gap(6)
            c1,c2,c3 = st.columns([1,1,3])
            with c1:
                if st.button("▶  Start Practice",use_container_width=True):
                    st.session_state.practice_q_idx = 0
                    st.session_state.practice_answered = False
                    st.session_state.practice_user_ans = None
            with c2:
                if st.button("⏭  Next Question",use_container_width=True):
                    st.session_state.practice_q_idx = (st.session_state.practice_q_idx+1) % len(QUESTIONS)
                    st.session_state.practice_answered = False
                    st.session_state.practice_user_ans = None
                    st.rerun()

            gap(6)
            q = QUESTIONS[st.session_state.practice_q_idx]
            H(f"""
            <div style="display:flex;align-items:center;justify-content:space-between;
                        margin-bottom:10px;flex-wrap:wrap;gap:8px;">
                <div style="display:flex;gap:8px;flex-wrap:wrap;">
                    <span style="background:rgba(79,70,229,.12);color:#818CF8;font-size:10px;
                                 font-weight:700;padding:3px 9px;border-radius:20px;">{q['subject']}</span>
                    <span style="background:rgba(6,182,212,.1);color:{CYN};font-size:10px;
                                 font-weight:700;padding:3px 9px;border-radius:20px;">{q['topic']}</span>
                    <span style="background:rgba(255,255,255,.06);color:{MUTE};font-size:10px;
                                 font-weight:700;padding:3px 9px;border-radius:20px;">Year: {q['year']}</span>
                    <span style="background:rgba(255,255,255,.06);color:{MUTE};font-size:10px;
                                 font-weight:700;padding:3px 9px;border-radius:20px;">{q['difficulty']}</span>
                </div>
                <div style="font-size:12px;color:{MUTE};">Q {st.session_state.practice_q_idx+1} of {len(QUESTIONS)}</div>
            </div>""")

            question_card(
                st.session_state.practice_q_idx+1,
                q["question"], q["options"], q["correct"], q["explanation"],
                show_answer=st.session_state.practice_answered,
                user_answer=st.session_state.practice_user_ans
            )

            if not st.session_state.practice_answered:
                ans_cols = st.columns(4)
                for i,lbl in enumerate(["A","B","C","D"]):
                    with ans_cols[i]:
                        if st.button(f"Option {lbl}",key=f"ans_{i}",use_container_width=True):
                            st.session_state.practice_user_ans = i
                            st.session_state.practice_answered = True
                            if i == q["correct"]:
                                st.session_state.practice_correct += 1
                                st.session_state.xp += 10
                            st.session_state.practice_total += 1
                            st.rerun()
            else:
                correct = st.session_state.practice_user_ans == q["correct"]
                if correct:
                    st.success("✅ Correct! +10 XP earned.")
                else:
                    st.error(f"❌ Incorrect. Correct answer: Option {['A','B','C','D'][q['correct']]}.")

            if st.session_state.practice_total > 0:
                acc = int(st.session_state.practice_correct/st.session_state.practice_total*100)
                H(f"""
                <div style="background:{SURF};border:1px solid rgba(255,255,255,.07);border-radius:12px;
                            padding:12px 16px;display:flex;gap:24px;margin-top:10px;flex-wrap:wrap;">
                    <div><div style="font-size:10px;color:{MUTE};">Session Accuracy</div>
                         <div style="font-size:18px;font-weight:700;color:{GRN if acc>=70 else RED};">{acc}%</div></div>
                    <div><div style="font-size:10px;color:{MUTE};">Correct</div>
                         <div style="font-size:18px;font-weight:700;color:{GRN};">{st.session_state.practice_correct}</div></div>
                    <div><div style="font-size:10px;color:{MUTE};">Attempted</div>
                         <div style="font-size:18px;font-weight:700;color:#F1F5F9;">{st.session_state.practice_total}</div></div>
                    <div><div style="font-size:10px;color:{MUTE};">XP Earned</div>
                         <div style="font-size:18px;font-weight:700;color:#818CF8;">{st.session_state.practice_correct*10} XP</div></div>
                </div>""")

        with tab2:
            sec("All Questions")
            df_q = pd.DataFrame([{"#":q["id"],"Subject":q["subject"],"Topic":q["topic"],
                                   "Year":q["year"],"Difficulty":q["difficulty"],
                                   "Question":q["question"][:60]+"…"} for q in QUESTIONS])
            st.dataframe(df_q,use_container_width=True,hide_index=True)

        with tab3:
            st.info("📌 Bookmarked questions will appear here. Click the bookmark button while practicing to save questions.")

    # ════════════════════════════════════════════
    #  MOCK TESTS
    # ════════════════════════════════════════════
    elif page == "mock":
        page_header("📝","Mock Tests","Full-length & mini tests with analysis")

        if not st.session_state.mock_active and not st.session_state.mock_submitted:
            tab1,tab2 = st.tabs(["📋 Available Tests","📊 Past Results"])
            with tab1:
                sec("Choose a test")
                mocks = [
                    ("🏆","Full Mock Test #12","200 Q · 3 Hrs · All Subjects","Hard","Tonight 7PM"),
                    ("📘","Polity Mini Test","50 Q · 1 Hr · Polity Only","Medium","Anytime"),
                    ("📗","History + Geography","75 Q · 90 Min","Medium","Anytime"),
                    ("⚡","Daily Challenge","20 Q · 20 Min · Mixed","Easy","Today Only"),
                    ("🔴","Weak Topic Drill","30 Q · 45 Min · Your Weak Areas","Hard","Anytime"),
                ]
                for icon,name,meta,diff,time_tag in mocks:
                    diff_color = RED if diff=="Hard" else (AMB if diff=="Medium" else GRN)
                    H(f"""
                    <div style="background:{SURF};border:1px solid rgba(255,255,255,.07);border-radius:14px;
                                padding:16px 18px;margin-bottom:9px;display:flex;align-items:center;gap:14px;">
                        <div style="font-size:24px;flex-shrink:0;">{icon}</div>
                        <div style="flex:1;">
                            <div style="font-size:14px;font-weight:600;color:#F1F5F9;margin-bottom:3px;">{name}</div>
                            <div style="font-size:12px;color:{MUTE};">{meta}</div>
                        </div>
                        <div style="text-align:right;flex-shrink:0;">
                            <div style="background:{'rgba(239,68,68,.1)' if diff=='Hard' else 'rgba(245,158,11,.1)' if diff=='Medium' else 'rgba(16,185,129,.1)'};
                                        color:{diff_color};font-size:10px;font-weight:700;padding:3px 9px;
                                        border-radius:20px;margin-bottom:4px;">{diff}</div>
                            <div style="font-size:11px;color:{MUTE};">{time_tag}</div>
                        </div>
                    </div>""")

                gap(6)
                if st.button("▶  Start Daily Challenge (Demo)",use_container_width=False):
                    st.session_state.mock_active   = True
                    st.session_state.mock_q_idx    = 0
                    st.session_state.mock_answers  = {}
                    st.session_state.mock_submitted= False
                    st.rerun()

            with tab2:
                sec("Your past mock results")
                results = [
                    {"Test":"Full Mock #11","Score":"156/200","Accuracy":"78%","Date":"Dec 28","Rank":"Top 15%"},
                    {"Test":"Polity Mini #5","Score":"43/50","Accuracy":"86%","Date":"Dec 25","Rank":"Top 8%"},
                    {"Test":"Full Mock #10","Score":"148/200","Accuracy":"74%","Date":"Dec 21","Rank":"Top 22%"},
                    {"Test":"Daily Challenge","Score":"18/20","Accuracy":"90%","Date":"Dec 20","Rank":"Top 5%"},
                ]
                st.dataframe(pd.DataFrame(results),use_container_width=True,hide_index=True)

                sec("Score trend")
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=["Mock 8","Mock 9","Mock 10","Mock 11","Mock 12 (next)"],
                    y=[138,144,148,156,None],
                    mode="lines+markers",line=dict(color=IND,width=2),
                    marker=dict(size=7,color=IND),
                    hovertemplate="<b>%{x}</b>: %{y}/200<extra></extra>"
                ))
                fig.update_layout(**PL,height=200,showlegend=False)
                st.plotly_chart(fig,use_container_width=True)

        elif st.session_state.mock_active and not st.session_state.mock_submitted:
            mock_qs = QUESTIONS[:5]  # demo: 5 questions
            idx = st.session_state.mock_q_idx

            H(f"""
            <div style="background:{SURF};border:1px solid rgba(255,255,255,.07);border-radius:12px;
                        padding:12px 16px;margin-bottom:12px;display:flex;align-items:center;
                        justify-content:space-between;flex-wrap:wrap;gap:8px;">
                <div style="font-size:14px;font-weight:600;color:#F1F5F9;">⏱️ Daily Challenge Mock</div>
                <div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap;">
                    <div style="font-size:12px;color:{MUTE};">Question {idx+1} of {len(mock_qs)}</div>
                    <div style="font-size:12px;font-weight:700;color:{CYN};">
                        {len(st.session_state.mock_answers)} answered</div>
                </div>
            </div>""")

            nav_cols = st.columns(len(mock_qs))
            for i in range(len(mock_qs)):
                with nav_cols[i]:
                    col = GRN if i in st.session_state.mock_answers else (IND if i==idx else SURF2)
                    H(f"""<div style="text-align:center;background:{col};border-radius:8px;
                               padding:6px;font-size:12px;font-weight:700;color:#fff;
                               cursor:pointer;">{i+1}</div>""")

            if idx < len(mock_qs):
                q = mock_qs[idx]
                H(f"""<div style="background:{SURF};border:1px solid rgba(255,255,255,.07);
                               border-radius:16px;padding:20px 22px;margin:12px 0;">
                         <div style="font-size:14px;color:#F1F5F9;line-height:1.7;font-weight:500;
                                     margin-bottom:14px;">{idx+1}. {q['question']}</div>""")
                for i,opt in enumerate(q["options"]):
                    answered = idx in st.session_state.mock_answers
                    bg = f"rgba(79,70,229,.15)" if answered and st.session_state.mock_answers.get(idx)==i else "rgba(255,255,255,.03)"
                    H(f"""<div style="background:{bg};border:1px solid rgba(255,255,255,.08);
                                    border-radius:10px;padding:10px 14px;margin-bottom:6px;">
                               <span style="font-size:11px;font-weight:700;color:{IND};margin-right:8px;">
                               {['A','B','C','D'][i]}</span>
                               <span style="font-size:13px;color:#94A3B8;">{opt}</span></div>""")
                H("</div>")

                ac1,ac2,ac3,ac4 = st.columns(4)
                for ci,(col,lbl) in enumerate(zip([ac1,ac2,ac3,ac4],["A","B","C","D"])):
                    with col:
                        if st.button(f"Mark {lbl}",key=f"mock_ans_{ci}",use_container_width=True):
                            st.session_state.mock_answers[idx] = ci
                            if idx < len(mock_qs)-1:
                                st.session_state.mock_q_idx += 1
                            st.rerun()

            c1,c2 = st.columns([1,1])
            with c1:
                if idx > 0 and st.button("← Previous",use_container_width=True):
                    st.session_state.mock_q_idx -= 1; st.rerun()
            with c2:
                if st.button("✅ Submit Test",use_container_width=True):
                    score = sum(1 for qi,ans in st.session_state.mock_answers.items()
                                if ans == mock_qs[qi]["correct"])
                    st.session_state.mock_score    = score
                    st.session_state.mock_submitted= True
                    st.session_state.mock_active   = False
                    st.session_state.xp           += 50
                    st.rerun()

        elif st.session_state.mock_submitted:
            mock_qs = QUESTIONS[:5]
            score = st.session_state.mock_score
            total = len(mock_qs)
            acc   = int(score/total*100)

            H(f"""
            <div style="text-align:center;background:{SURF};border:1px solid rgba(255,255,255,.07);
                        border-radius:18px;padding:32px 24px;margin-bottom:16px;">
                <div style="font-size:48px;margin-bottom:10px;">{'🏆' if acc>=80 else '📊'}</div>
                <div style="font-size:32px;font-weight:800;color:#F1F5F9;margin-bottom:4px;">{score}/{total}</div>
                <div style="font-size:18px;font-weight:600;color:{GRN if acc>=70 else RED};margin-bottom:8px;">{acc}% Accuracy</div>
                <div style="font-size:13px;color:{MUTE};">+50 XP earned · Daily Challenge complete</div>
            </div>""")

            sec("Subject breakdown")
            result_row("Polity",2,2,GRN)
            result_row("History",1,2,AMB)
            result_row("Geography",1,1,GRN)
            result_row("Aptitude",0,1,RED)

            gap(8)
            sec("Detailed answers")
            for i,q in enumerate(mock_qs):
                user_ans = st.session_state.mock_answers.get(i)
                question_card(i+1,q["question"],q["options"],q["correct"],
                              q["explanation"],show_answer=True,user_answer=user_ans)

            gap(6)
            if st.button("🔄 Back to Mock Tests",use_container_width=False):
                st.session_state.mock_submitted = False
                st.session_state.mock_active    = False
                st.rerun()

    # ════════════════════════════════════════════
    #  STUDY PLANNER
    # ════════════════════════════════════════════
    elif page == "planner":
        page_header("📅","Study Planner","Your personalised daily & weekly schedule")

        tab1,tab2 = st.tabs(["📆 This Week","⚙️ Adjust Plan"])

        with tab1:
            sec("This week's plan")
            days_plan = {
                "Monday":   [("Polity","Constitutional Articles — Art. 1–50","1h",IND),
                             ("Aptitude","Number Series & Ratios","45m",CYN)],
                "Tuesday":  [("History","Ancient India — Mauryan Empire","1h",AMB),
                             ("Mock Test","Mini Test: Polity (20Q)","30m",GRN)],
                "Wednesday":[("Geography","Tamil Nadu Districts & Rivers","1h",IND),
                             ("Revision","Polity — Spaced Revision","45m",VIO)],
                "Thursday": [("Science","Physics & Chemistry basics","1h",CYN),
                             ("Aptitude","Percentage & Profit/Loss","45m",CYN)],
                "Friday":   [("History","Medieval India — Mughal Empire","1h",AMB),
                             ("Current Affairs","Weekly Capsule","30m",GRN)],
                "Saturday": [("Full Mock","Full Mock Test #12 — 3 hours","3h",RED),],
                "Sunday":   [("Revision","All weak topics — spaced revision","2h",VIO),
                             ("Planning","Next week planning","30m",MUTE)],
            }
            for day,tasks in days_plan.items():
                H(f"""
                <div style="background:{SURF};border:1px solid rgba(255,255,255,.07);
                            border-radius:14px;padding:14px 16px;margin-bottom:8px;">
                    <div style="font-size:12px;font-weight:700;color:#818CF8;margin-bottom:10px;
                                letter-spacing:.4px;">{day.upper()}</div>
                    <div style="display:flex;flex-direction:column;gap:6px;">""")
                for subj,task,dur,col in tasks:
                    H(f"""
                    <div style="display:flex;align-items:center;gap:10px;background:rgba(255,255,255,.03);
                                border-radius:9px;padding:8px 12px;">
                        <div style="width:8px;height:8px;border-radius:50%;background:{col};flex-shrink:0;"></div>
                        <div style="flex:1;font-size:13px;color:#94A3B8;">{task}</div>
                        <div style="font-size:11px;font-weight:600;color:{col};">{dur}</div>
                    </div>""")
                H("</div></div>")

        with tab2:
            sec("Adjust your plan")
            c1,c2 = st.columns(2)
            with c1:
                st.selectbox("Exam target",EXAM_TYPES,key="pl_exam")
                st.selectbox("Daily study hours",["1h","2h","3h","4h","5h+"],index=2,key="pl_hrs")
            with c2:
                st.multiselect("Focus subjects",SUBJECTS[1:],key="pl_focus")
                st.text_input("Exam date target","2025-06-15",key="pl_date")
            if st.button("🔄 Regenerate Plan",use_container_width=False):
                st.success("✅ Study plan updated for your preferences!")

    # ════════════════════════════════════════════
    #  REVISION SYSTEM
    # ════════════════════════════════════════════
    elif page == "revision":
        page_header("🔁","Revision System","Spaced repetition — never forget what you studied")

        c1,c2,c3 = st.columns(3)
        with c1: stat_card("📌","Due today","12 topics","3 overdue",RED,RED)
        with c2: stat_card("✅","Revised this week","28 topics","+8 vs last week",GRN)
        with c3: stat_card("🧠","Retention rate","74%","+5% this month",CYN,CYN)

        sec("Revision queue — due today")
        revisions = [
            ("Polity","Fundamental Rights (Art. 12–35)","1 day","🔴 Overdue"),
            ("History","Mauryan Empire — Key rulers","3 days","🟡 Due today"),
            ("Geography","Major Rivers of Tamil Nadu","7 days","🟢 Due today"),
            ("Science","Photosynthesis & Cell Biology","1 day","🔴 Overdue"),
            ("Aptitude","Profit & Loss formulas","15 days","🟢 Due today"),
        ]
        for subj,topic,interval,status in revisions:
            H(f"""
            <div style="background:{SURF};border:1px solid rgba(255,255,255,.07);border-radius:12px;
                        padding:13px 16px;margin-bottom:7px;display:flex;align-items:center;gap:13px;">
                <div style="flex:1;">
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:3px;">
                        <span style="background:rgba(79,70,229,.12);color:#818CF8;font-size:10px;
                                     font-weight:700;padding:2px 8px;border-radius:20px;">{subj}</span>
                        <span style="font-size:13px;font-weight:500;color:#F1F5F9;">{topic}</span>
                    </div>
                    <div style="font-size:11px;color:{MUTE};">Interval: {interval}</div>
                </div>
                <div style="font-size:12px;font-weight:600;">{status}</div>
            </div>""")

        gap(8)
        if st.button("▶  Start Revision Session",use_container_width=False):
            st.info("📚 Revision session would load your due topics as quick 5-question quizzes.")

        sec("Revision schedule (next 7 days)")
        sched = {"Mon":8,"Tue":5,"Wed":12,"Thu":4,"Fri":9,"Sat":15,"Sun":6}
        fig = go.Figure(go.Bar(x=list(sched.keys()),y=list(sched.values()),
                                marker_color=VIO,marker_line_width=0))
        fig.update_layout(**PL,height=180,showlegend=False,yaxis_title="Topics due")
        st.plotly_chart(fig,use_container_width=True)

    # ════════════════════════════════════════════
    #  ANALYTICS
    # ════════════════════════════════════════════
    elif page == "analytics":
        page_header("📊","Analytics","Deep dive into your performance")

        c1,c2,c3,c4 = st.columns(4)
        c1.metric("📈 Total accuracy","82%","+3% this month")
        c2.metric("⏱️ Total study hours","48h","this month")
        c3.metric("📝 Questions attempted","1,240","+180 this week")
        c4.metric("📊 Mock avg score","76/100","+4 vs last month")
        gap(4)

        tab1,tab2,tab3 = st.tabs(["📈 Performance","⚠️ Weak Areas","🔢 Question Stats"])

        with tab1:
            c1,c2 = st.columns(2)
            with c1:
                sec("Mock test score trend",mt=10)
                months = ["Aug","Sep","Oct","Nov","Dec","Jan"]
                scores = [62,68,71,74,78,82]
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=months,y=scores,mode="lines+markers",
                                          fill="tozeroy",fillcolor="rgba(79,70,229,.08)",
                                          line=dict(color=IND,width=2),
                                          marker=dict(size=6,color=IND)))
                fig.update_layout(**PL,height=220,showlegend=False,yaxis_title="Score/100")
                st.plotly_chart(fig,use_container_width=True)
            with c2:
                sec("Accuracy by subject",mt=10)
                subs = ["Polity","Geography","Science","Economics","History","Aptitude"]
                accs = [88,74,81,77,65,58]
                colors_acc = [GRN if a>=80 else (AMB if a>=65 else RED) for a in accs]
                fig2 = go.Figure(go.Bar(x=accs,y=subs,orientation="h",
                                         marker_color=colors_acc,marker_line_width=0))
                fig2.update_layout(**PL,height=220,showlegend=False,xaxis_title="Accuracy %")
                fig2.update_xaxes(ticksuffix="%")
                st.plotly_chart(fig2,use_container_width=True)

            sec("Daily study hours — last 30 days")
            dates = pd.date_range(end=datetime.date.today(),periods=30)
            hrs30 = [random.uniform(1.5,4.5) for _ in range(30)]
            fig3 = go.Figure(go.Scatter(x=dates,y=hrs30,fill="tozeroy",
                                         fillcolor="rgba(6,182,212,.07)",
                                         line=dict(color=CYN,width=1.5)))
            fig3.update_layout(**PL,height=180,showlegend=False,yaxis_title="Hours")
            st.plotly_chart(fig3,use_container_width=True)

        with tab2:
            sec("Topics you miss most often",mt=10)
            weak_topics = [
                ("Medieval History — Mughal successors",18,24),
                ("Aptitude — Time, Speed & Distance",14,20),
                ("Polity — DPSP vs Fundamental Rights",12,18),
                ("Geography — Soil types of India",10,15),
                ("Economics — 5-Year Plans",9,14),
            ]
            for topic,wrong,total in weak_topics:
                err_rate = int(wrong/total*100)
                H(f"""
                <div style="background:{SURF};border:1px solid rgba(239,68,68,.15);
                            border-left:3px solid {RED};border-radius:12px;
                            padding:12px 16px;margin-bottom:7px;
                            display:flex;align-items:center;gap:12px;">
                    <div style="flex:1;font-size:13px;color:#F1F5F9;">{topic}</div>
                    <div style="font-size:12px;font-weight:700;color:{RED};">{err_rate}% errors</div>
                </div>""")

        with tab3:
            sec("Question attempt statistics",mt=10)
            q_stats = {"Polity":320,"History":280,"Geography":240,"Science":210,"Aptitude":190}
            fig4 = go.Figure(go.Pie(labels=list(q_stats.keys()),values=list(q_stats.values()),
                                     hole=.55,marker_colors=[IND,AMB,GRN,CYN,VIO]))
            fig4.update_layout(**PL,height=280,showlegend=True,
                               legend=dict(font=dict(color="#94A3B8")))
            st.plotly_chart(fig4,use_container_width=True)

    # ════════════════════════════════════════════
    #  ACHIEVEMENTS
    # ════════════════════════════════════════════
    elif page == "achievements":
        page_header("🏆","Achievements & Badges","Your milestones and rewards")

        xp_badge(xp, lvl, get_level_name(lvl), streak)
        gap(6)

        sec("Your badges")
        badge_cols = st.columns(5)
        badges = [
            ("🔥","14-Day Streak","Post 14 days in a row",True),
            ("🎯","Sharpshooter","90%+ accuracy in a mock",True),
            ("📚","Question Master","1000 questions answered",True),
            ("⚡","Speed Demon","Finish mock in half time",True),
            ("🌟","Top Scorer","Score 190+ in full mock",False),
            ("💎","Diamond Streak","30 day streak",False),
            ("🧠","Subject Expert","95%+ in any subject",False),
            ("🏅","TNPSC Champion","Complete all mock tests",False),
            ("📰","CA Enthusiast","Read 30 days CA",True),
            ("🚀","Consistency King","Study 7 days straight",True),
        ]
        for i,(icon,name,desc,earned) in enumerate(badges):
            with badge_cols[i%5]:
                badge_chip(icon,name,desc,earned)
            if (i+1)%5==0 and i<len(badges)-1:
                badge_cols = st.columns(5)

        sec("XP History")
        xp_events = [
            ("Today","Completed 20 Polity questions","+200 XP"),
            ("Today","7-day streak bonus","+100 XP"),
            ("Yesterday","Completed Mock Test #11","+50 XP"),
            ("Dec 28","90% accuracy badge","+150 XP"),
            ("Dec 27","Completed revision session","+30 XP"),
        ]
        for date,event,xp_val in xp_events:
            H(f"""
            <div style="display:flex;align-items:center;gap:12px;padding:10px 0;
                        border-bottom:1px solid rgba(255,255,255,.05);">
                <div style="font-size:11px;color:{MUTE};width:80px;flex-shrink:0;">{date}</div>
                <div style="flex:1;font-size:13px;color:#94A3B8;">{event}</div>
                <div style="font-size:13px;font-weight:700;color:#818CF8;">{xp_val}</div>
            </div>""")

        sec("Leaderboard — This Month")
        lb = [("🥇","Arun Kumar","Group 2","3,840 XP"),
              ("🥈","Priya Rajan","Group 1","3,610 XP"),
              ("🥉","Karthik V","Group 4","3,290 XP"),
              ("4️⃣",f"{user} (You)","Group 2",f"{xp} XP"),
              ("5️⃣","Deepa S","Group 2","1,380 XP")]
        for rank,name,exam_t,xp_val in lb:
            is_you = "You" in name
            bg = f"rgba(79,70,229,.1)" if is_you else "rgba(255,255,255,.03)"
            H(f"""
            <div style="background:{bg};border:1px solid {'rgba(79,70,229,.25)' if is_you else 'rgba(255,255,255,.06)'};
                        border-radius:11px;padding:10px 14px;margin-bottom:6px;
                        display:flex;align-items:center;gap:12px;">
                <div style="font-size:16px;flex-shrink:0;">{rank}</div>
                <div style="flex:1;">
                    <div style="font-size:13px;font-weight:600;color:#F1F5F9;">{name}</div>
                    <div style="font-size:11px;color:{MUTE};">{exam_t}</div>
                </div>
                <div style="font-size:13px;font-weight:700;color:#818CF8;">{xp_val}</div>
            </div>""")

    # ════════════════════════════════════════════
    #  CURRENT AFFAIRS
    # ════════════════════════════════════════════
    elif page == "current_affairs":
        page_header("📰","Current Affairs","Stay updated for your exam")

        tab1,tab2,tab3 = st.tabs(["📅 Daily","📦 Weekly Capsule","❓ CA Quiz"])

        with tab1:
            sec("Today's Current Affairs")
            ca_items = [
                ("Tamil Nadu","Tamil Nadu becomes first state to launch comprehensive EV charging policy targeting 1 lakh charging stations by 2030.","Govt & Policy"),
                ("India","Union Cabinet approves ₹2,500 crore for PM-SHRI school upgrades across 14,500 institutions.","Education"),
                ("International","BRICS membership expands to include 4 new partner nations; India chairs next summit.","International"),
                ("Sports","Tamil Nadu boxer wins gold at Asian Championships; qualifies for 2025 World Championship.","Sports"),
                ("Awards","Noted Tamil writer M. Murugesan receives Sahitya Akademi Award for fiction.","Awards"),
                ("Schemes","PM Kisan Samman Nidhi: 16th installment released; ₹17,000 crore disbursed to 8.5 crore farmers.","Schemes"),
            ]
            cats = list(set([c[2] for c in ca_items]))
            cat_colors = {"Govt & Policy":IND,"Education":CYN,"International":VIO,
                          "Sports":GRN,"Awards":AMB,"Schemes":GRN}
            for headline,body,cat in ca_items:
                H(f"""
                <div style="background:{SURF};border:1px solid rgba(255,255,255,.07);border-radius:12px;
                            padding:14px 16px;margin-bottom:8px;">
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
                        <span style="background:rgba(79,70,229,.12);color:{cat_colors.get(cat,IND)};
                                     font-size:10px;font-weight:700;padding:2px 9px;border-radius:20px;">{cat}</span>
                        <span style="font-size:13px;font-weight:600;color:#F1F5F9;">{headline}</span>
                    </div>
                    <div style="font-size:12px;color:#64748B;line-height:1.65;">{body}</div>
                </div>""")

        with tab2:
            st.info("📦 Weekly capsules cover Tamil Nadu, India, and International affairs from Mon–Sun. Download as PDF for offline study.")
            weeks = ["Week 52 (Dec 23–29)","Week 51 (Dec 16–22)","Week 50 (Dec 9–15)"]
            for w in weeks:
                with st.expander(w):
                    H(f"<div style='font-size:13px;color:#94A3B8;'>Weekly capsule for {w} — covers Govt, Economy, Sports, International affairs in MCQ-ready summary format.</div>")

        with tab3:
            sec("Current Affairs Quiz — this week")
            ca_qs = [
                {"q":"Which state launched the 'Global Tamil Investors Meet 2025'?",
                 "opts":["Kerala","Andhra Pradesh","Tamil Nadu","Karnataka"],"correct":2},
                {"q":"The 16th BRICS Summit 2025 was chaired by which country?",
                 "opts":["China","Russia","India","South Africa"],"correct":2},
            ]
            for i,caq in enumerate(ca_qs):
                question_card(i+1,caq["q"],caq["opts"],caq["correct"],
                              "Based on recent news — check the detailed CA section for full explanation.",
                              show_answer=False)

    footer()
