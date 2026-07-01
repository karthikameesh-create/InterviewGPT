import streamlit as st
from utils.auth import login_user, register_user, reset_password


def load_css():
    st.markdown("""
    <style>

    /* ── Kill Streamlit chrome ── */
    header[data-testid="stHeader"], footer,
    [data-testid="stToolbar"], [data-testid="stDecoration"],
    section[data-testid="stSidebar"] { display:none !important; }

    .stApp, [data-testid="stAppViewContainer"] {
        background: #eef1ff !important;
    }
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    [data-testid="column"] { padding: 0 !important; }

    /* ── LEFT PANEL ── */
    .left-panel {
        background: linear-gradient(145deg,#3d5ce6 0%,#4F6EF7 55%,#6c7ff8 100%);
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 60px 52px;
        position: relative;
        overflow: hidden;
        animation: lpSlide .65s cubic-bezier(.22,.68,0,1.2) both;
    }
    @keyframes lpSlide {
        from { opacity:0; transform:translateX(-20px); }
        to   { opacity:1; transform:translateX(0); }
    }
    .left-panel::before {
        content:""; position:absolute; width:320px; height:320px; border-radius:50%;
        border:52px solid rgba(255,255,255,.09); bottom:-90px; right:-90px;
        animation: flt 7s ease-in-out infinite;
    }
    .left-panel::after {
        content:""; position:absolute; width:180px; height:180px; border-radius:50%;
        border:34px solid rgba(255,255,255,.06); top:-45px; left:-45px;
        animation: flt 9s ease-in-out infinite reverse;
    }
    @keyframes flt { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-14px)} }

    .lp-dot { position:absolute; border-radius:50%; animation:flt 5s ease-in-out infinite; }
    .d1 { width:18px;height:18px;background:#4dd0e1;bottom:22%;left:44px;animation-duration:4.5s; }
    .d2 { width:10px;height:10px;background:rgba(255,255,255,.5);top:10%;right:12%;animation-duration:6s;animation-delay:.8s; }
    .d3 { width:7px;height:7px;background:rgba(77,208,225,.65);top:30%;right:8%;animation-duration:7.5s;animation-delay:.3s; }

    .lp-bars { display:flex; gap:8px; margin-bottom:28px; }
    .lp-bar  { width:6px; border-radius:3px; background:rgba(255,255,255,.38); }
    .lp-bar.b1 { height:34px; }
    .lp-bar.b2 { height:52px; background:white; }
    .lp-bar.b3 { height:24px; }

    .lp-brand    { font-size:11px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:rgba(255,255,255,.52);margin-bottom:10px; }
    .lp-headline { font-size:38px;font-weight:800;color:white;line-height:1.18;margin:0 0 14px; }
    .ai-grad     { background:linear-gradient(90deg,#a5f3fc,#e0e7ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text; }
    .lp-sub      { color:rgba(255,255,255,.68);font-size:13px;line-height:1.65;max-width:290px; }
    .lp-pills    { display:flex;flex-wrap:wrap;gap:7px;margin-top:22px; }
    .lp-pill     { background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.20);color:rgba(255,255,255,.88);border-radius:20px;padding:4px 12px;font-size:11.5px;font-weight:600; }

    /* ── RIGHT PANEL: center vertically ── */
    [data-testid="column"]:last-child > div:first-child {
        min-height: 100vh;
        display: flex !important;
        flex-direction: column;
        justify-content: center;
        padding: 0 !important;
        background: #eef1ff;
    }

    /* ── Card wrapper ── */
    .form-card-top {
        background: white;
        border-radius: 22px 22px 0 0;
        padding: 28px 36px 16px;
        box-shadow: 0 -2px 0 0 white, 4px 0 0 0 white, -4px 0 0 0 white;
        margin: 0 auto;
        width: 100%;
        max-width: 360px;
        animation: cardUp .55s cubic-bezier(.22,.68,0,1.2) .15s both;
    }
    .form-card-bottom {
        background: white;
        border-radius: 0 0 22px 22px;
        padding: 0 36px 24px;
        box-shadow: 0 12px 48px rgba(79,110,247,.13);
        margin: 0 auto;
        width: 100%;
        max-width: 360px;
    }
    @keyframes cardUp {
        from { opacity:0; transform:translateY(18px); }
        to   { opacity:1; transform:translateY(0); }
    }

    .ig-logo {
        width:50px; height:50px;
        background:linear-gradient(135deg,#4F6EF7,#818cf8);
        border-radius:13px;
        display:flex; align-items:center; justify-content:center;
        margin:0 auto 14px;
        font-size:17px; font-weight:800; color:white;
        box-shadow:0 4px 14px rgba(79,110,247,.30);
    }
    .fc-title { text-align:center;color:#1e293b;font-size:18px;font-weight:700;margin-bottom:3px; }
    .fc-sub   { text-align:center;color:#94a3b8;font-size:12px;margin-bottom:0; }

    /* ── Streamlit widget overrides ── */
    div[data-testid="stTextInput"] input {
        border: 1.5px solid #e2e8f0 !important;
        border-radius: 9px !important;
        background: #f8fafc !important;
        color: #1e293b !important;
        padding: 9px 12px !important;
        font-size: 13.5px !important;
        transition: border-color .2s, background .2s !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #4F6EF7 !important;
        background: white !important;
    }
    div[data-testid="stTextInput"] > label {
        font-size: 12px !important;
        font-weight: 600 !important;
        color: #374151 !important;
    }
    div[data-testid="stTextInput"] { margin-bottom: 2px !important; }

    div[data-testid="stButton"] > button {
        background: linear-gradient(135deg,#4F6EF7,#818cf8) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        height: 42px !important;
        font-size: 13.5px !important;
        font-weight: 700 !important;
        width: 100% !important;
        margin-top: 6px !important;
        transition: opacity .2s, transform .15s !important;
    }
    div[data-testid="stButton"] > button:hover {
        opacity: .91 !important; transform: translateY(-1px) !important;
    }

    div[data-baseweb="tab-list"] {
        background: #f1f5f9 !important;
        border-radius: 10px !important;
        padding: 3px !important;
        gap: 2px !important;
    }
    button[data-baseweb="tab"] {
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 12px !important;
        color: #64748b !important;
        padding: 6px 8px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background: white !important;
        color: #4F6EF7 !important;
        box-shadow: 0 2px 8px rgba(79,110,247,.13) !important;
    }
    div[data-baseweb="tab-highlight"],
    div[data-baseweb="tab-border"] { display:none !important; }
    div[data-testid="stTabsContent"] { padding-top: 8px !important; }

    div[data-testid="stAlert"] {
        border-radius: 8px !important;
        font-size: 12.5px !important;
        padding: 7px 11px !important;
        margin-top: 6px !important;
    }

    .card-footer { text-align:center;color:#cbd5e1;font-size:11px;margin-top:14px;padding-bottom:4px; }

    </style>
    """, unsafe_allow_html=True)


def login_page():
    load_css()

    col_left, col_right = st.columns([52, 48], gap="small")

    # ── LEFT ──
    with col_left:
        st.markdown("""
        <div class="left-panel">
            <span class="lp-dot d1"></span>
            <span class="lp-dot d2"></span>
            <span class="lp-dot d3"></span>
            <div class="lp-bars">
                <div class="lp-bar b1"></div>
                <div class="lp-bar b2"></div>
                <div class="lp-bar b3"></div>
            </div>
            <div class="lp-brand">🤖 InterviewGPT Pro</div>
            <p class="lp-headline">Ace Every<br>Interview With <span class="ai-grad">AI</span></p>
            <p class="lp-sub">Your all-in-one platform for landing the job you deserve.</p>
            <div class="lp-pills">
                <span class="lp-pill">📄 Resume Analysis</span>
                <span class="lp-pill">🎯 ATS Scanning</span>
                <span class="lp-pill">🎤 Mock Interviews</span>
                <span class="lp-pill">💻 Coding Practice</span>
                <span class="lp-pill">🧭 Career Guidance</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── RIGHT ──
    with col_right:
        # Card top: logo + title (pure HTML)
        st.markdown("""
        <div class="form-card-top">
            <div class="ig-logo">IG</div>
            <p class="fc-title">Hello! Welcome back</p>
            <p class="fc-sub">Sign in to continue your interview prep</p>
        </div>
        """, unsafe_allow_html=True)

        # Card bottom: tabs + widgets (native Streamlit, styled to look inside card)
        with st.container():
            st.markdown('<div class="form-card-bottom">', unsafe_allow_html=True)

            tab1, tab2, tab3 = st.tabs(["🔑 Login", "📝 Sign Up", "🔒 Reset Password"])

            with tab1:
                email    = st.text_input("Email",    placeholder="Enter your email address", key="login_email")
                password = st.text_input("Password", placeholder="••••••••••••", type="password", key="login_password")
                if st.button("Login", use_container_width=True, key="login_btn"):
                    if not email or not password:
                        st.error("Please fill in all fields.")
                    else:
                        success, result = login_user(email, password)
                        from utils.firestore_db import create_user

                        if success:

                         st.session_state.logged_in = True

                         st.session_state.user = result

                         st.session_state.user_email = email
                         from utils.firestore_db import load_resume

                         resume = load_resume(

                         result["localId"]

                         )

                         st.session_state.resume_text = resume

                         uid = result["localId"]

                         create_user(uid, email)

                         st.rerun()
                        else:
                            st.error(result)

            with tab2:
                email    = st.text_input("Email",    placeholder="Enter your email address", key="signup_email")
                password = st.text_input("Password", placeholder="Create a strong password", type="password", key="signup_password")
                if st.button("Create Account", use_container_width=True, key="signup_btn"):
                    if not email or not password:
                        st.error("Please fill in all fields.")
                    else:
                        success, result = register_user(email, password)
                        st.success(result) if success else st.error(result)

            with tab3:
                email = st.text_input("Registered Email", placeholder="Enter your registered email", key="reset_email")
                if st.button("Send Reset Email", use_container_width=True, key="reset_btn"):
                    if not email:
                        st.error("Please enter your email.")
                    else:
                        success, result = reset_password(email)
                        st.success(result) if success else st.error(result)

            st.markdown('<p class="card-footer">© 2026 InterviewGPT Pro</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)