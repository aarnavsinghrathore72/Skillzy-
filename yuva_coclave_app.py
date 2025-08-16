import streamlit as st
import random 
import time
import google.generativeai as genai
import datetime
from collections import deque

API_KEY = "AIzaSyCpEmX1xhOHvsIaBHBRtuXabj6EeEcfI4I"
genai.configure(api_key=API_KEY)
API_KEY = "AIzaSyCpEmX1xhOHvsIaBHBRtuXabj6EeEcfI4I"   # put your key here
genai.configure(api_key=API_KEY)
MODEL = "gemini-1.5-flash"

# pick a CURRENT model (fast & cheap: 1.5-flash, higher quality: 1.5-pro)
DEFAULT_MODEL = "gemini-1.5-flash"

# -------- Feedback Library (shortened for demo) --------
feedback_library = {
    "skills": {
        "poor": """
🛠️ **Your skill development needs attention. But don't be discouraged — every expert was once a beginner.**

### ✅ Action Plan to Improve Your Skills:

1. **Identify 1–2 key skills** you want to focus on (e.g., communication, leadership, public speaking, coding).
2. **Start with low-pressure environments:**
   - Join college clubs or local NGOs.
   - Volunteer to help organize events (learn teamwork, problem-solving).
3. **Practice daily:**
   - Spend 20 minutes a day on your chosen skill.
   - Use YouTube channels like `Improvement Pill`, `CrashCourse`, or `FreeCodeCamp`.
4. **Build confidence with side projects:**
   - Make a Canva poster, write a blog, record a podcast — tiny wins matter.
5. **Track your growth:** Journal weekly progress or record short video reflections.

### 💡 Platforms to Explore:
- **Soft skills:** Toastmasters, Coursera (Effective Communication)
- **Tech skills:** Sololearn, freeCodeCamp, W3Schools

✨ *Don't aim to be perfect. Aim to get better, one rep at a time.*
""",

        "good": """
💡 **You're doing well with your skill development — now it's time to step up!**

### 🚀 How to Sharpen Your Skills:

1. **Join competitions and real-world challenges:**
   - Hackathons, debates, case study contests, public speaking events.
2. **Collaborate in teams:**
   - Lead a group project, organize an event, or build something with friends.
3. **Create a portfolio:**
   - Use GitHub, Behance, or Notion to show your work (designs, blogs, apps, leadership roles).
4. **Shadow professionals or attend webinars:**
   - See how experts do it — then model their habits.
5. **Level up soft + tech skills:**
   - Combine areas — e.g., public speaking + coding = technical storytelling.

### 🔧 Tools to Explore:
- Notion (for documenting growth)
- Duolingo or Grammarly (communication)
- Trello or Asana (project management)

🔥 *You’re no longer just learning skills — you’re building identity and influence.*
""",

        "excellent": """
🚀 **Exceptional! Your skills are top-notch — now let’s turn them into real-world impact.**

### 🌍 How to Leverage Your Skills:

1. **Mentor or teach:** 
   - Help juniors, run workshops, make content (reels/blogs) — it builds clarity and legacy.
2. **Build a personal brand:**
   - Share your story, projects, and tips on LinkedIn, Instagram, or a personal blog.
3. **Create or lead initiatives:**
   - Start a podcast, community club, or internship-ready project.
4. **Freelance or intern:**
   - Start earning or gaining experience from real clients or organizations.
5. **Balance your wheel:** 
   - Strengthen lesser-used skills (e.g., if you're tech-heavy, improve creativity or collaboration).

### 🔧 Advanced Platforms:
- LinkedIn (networking)
- Medium/Substack (write about your journey)
- Upwork/Fiverr (start freelancing)

🌟 *You’ve built the rocket — now it’s time to launch it.*
"""
    },

    "academics": {
        "poor": """
📚 **Your academics need focused attention — but don’t panic. You have what it takes to turn it around.**

### 📈 Step-by-Step Improvement Plan:

1. **Diagnose the problem:**
   - Is it understanding, discipline, distraction, or pressure?
2. **Make a 1-hour-a-day study rule:**
   - Use Pomodoro (25 min study + 5 min break × 2).
3. **Clarify basics:**
   - Watch simple explainers (Khan Academy, ExamFear, Vedantu) before tackling textbooks.
4. **Ask for help weekly:**
   - Approach teachers, peers, or YouTube tutors — small doubts block big progress.
5. **Use handwritten notes:**
   - Writing helps retain more. Summarize chapters into flashcards or mind maps.

### ⚙️ Tools to Try:
- Notion / Evernote (study planner)
- Anki (flashcards)
- Focus apps (Forest, Tide)

❤️ *Your grades don’t define your worth. But effort, mindset, and bounce-back power do.*
""",

        "good": """
👍 **You’ve got a strong academic foundation — keep the momentum going!**

### 🧗 Here’s How to Elevate Further:

1. **Study actively, not passively:**
   - Use Feynman technique: explain topics out loud in your own words.
2. **Revise weekly:**
   - Don’t just learn — revisit material on Sundays to cement it.
3. **Join group studies:**
   - Explaining to peers + listening = double retention.
4. **Take mock tests:**
   - Simulate exam pressure every 2–3 weeks.
5. **Connect subjects to real life:**
   - Economics? Read newspapers. Biology? Watch science documentaries.

### 📚 Useful Platforms:
- Toppr, Doubtnut (ask doubts)
- Evernote/Notion (track revision)
- Class Central (free university-level courses)

🎓 *You’re climbing — don’t slow down. Let your consistency do the talking.*
""",

        "excellent": """
🎓 **Top-tier academic performance! You’ve mastered consistency and focus — now use it as a launchpad.**

### 🌟 Take Your Learning Global:

1. **Start research early:**
   - Join academic clubs, reach out to professors, and work on mini research papers.
2. **Apply for scholarships and programs:**
   - Google’s CSSI, MITx, TATA Trust, or UWC — you qualify!
3. **Take MOOC certifications:**
   - EdX, Harvard Online, or Stanford’s free classes — build a global academic profile.
4. **Teach others:**
   - Run doubt-clearing sessions, mentor juniors, or create mini video lessons.
5. **Link to careers:**
   - Connect subjects with job paths — e.g., physics → data science, economics → consulting.

### 📘 Bonus Resources:
- ResearchGate, Academia.edu (for research reading)
- EdX, Coursera (certification)
- LinkedIn Learning (career-aligned content)

🏆 *This is more than good grades — it’s future leadership in the making.*
"""
    }
}


# -------- Helper Functions --------

def classify(score):
    if 70 <= score <= 100:
        return "excellent"
    elif 40 <= score < 70:
        return "good"
    else:
        return "poor"

# -------- Pages --------
def welcome_page():
    st.markdown("""
        <style>
        .welcome-container {
            background: linear-gradient(135deg, #1e3a8a, #3b82f6);
            color: white;
            padding: 50px;
            border-radius: 20px;
            text-align: center;
            font-family: 'Segoe UI', sans-serif;
            box-shadow: 0px 8px 25px rgba(0,0,0,0.25);
            animation: fadeIn 1.2s ease-in-out;
        }
        .welcome-container h1 {
            font-size: 3.2rem;
            margin-bottom: 10px;
            font-weight: bold;
        }
        .welcome-container h3 {
            font-size: 1.8rem;
            margin-bottom: 20px;
            font-weight: 500;
            color: #ffcc00;
        }
        .welcome-container p {
            font-size: 1.2rem;
            line-height: 1.7;
        }
        .welcome-points {
            background: rgba(255, 255, 255, 0.15);
            padding: 20px;
            border-radius: 15px;
            margin-top: 25px;
            font-size: 1.2rem;
            text-align: left;
            box-shadow: inset 0px 4px 10px rgba(255,255,255,0.2);
        }
        .start-button {
            background: linear-gradient(90deg, #facc15, #f97316);
            color: black;
            padding: 15px 35px;
            border-radius: 12px;
            border: none;
            cursor: pointer;
            font-size: 1.3rem;
            margin-top: 30px;
            font-weight: bold;
            box-shadow: 0px 5px 15px rgba(0,0,0,0.3);
            transition: all 0.3s ease-in-out;
        }
        .start-button:hover {
            background: linear-gradient(90deg, #f97316, #facc15);
            transform: scale(1.07);
        }
        @keyframes fadeIn {
            from {opacity: 0; transform: translateY(20px);}
            to {opacity: 1; transform: translateY(0);}
        }
        </style>

        <div class="welcome-container">
            <h1>🌟 Welcome to Skillzy</h1>
            <h3>Empowering Youth with Skills for the 21st Century</h3>
            <p>
                Skillzy is on a mission to <b>revolutionize education</b> by shifting focus 
                from rote learning to <b>skill-based assessments</b>. 
                We aim to create a <b>skilled, confident, and future-ready society</b> 
                that can tackle the challenges of tomorrow.
            </p>
            <div class="welcome-points">
                ✅ Track your skills and progress<br>
                ✅ Get instant AI-powered guidance<br>
                ✅ Prepare for real-world challenges
            </div><br>
            <button class="start-button" onclick="window.location.href='?page=chat'">🚀 Start Chatting</button>
        </div>
    """, unsafe_allow_html=True)

def page_ai_tips():
    st.markdown("""
        <style>
        .main {
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            color: white;
            font-family: 'Segoe UI', sans-serif;
        }

        h1 {
            font-size: 2.6rem !important;
            color: #ffcc00;
            text-align: center;
            font-weight: bold;
            margin-bottom: 15px;
            text-shadow: 2px 2px 10px rgba(0,0,0,0.4);
            animation: fadeIn 1s ease-in-out;
        }

        h2, h3 {
            color: #00ffea;
            font-size: 1.4rem !important;
        }

        .stTextInput input {
            font-size: 1.2rem !important;
            padding: 12px;
            border-radius: 12px;
            border: 2px solid #00ffea;
            background: rgba(255,255,255,0.08);
            color: white;
            transition: 0.3s ease-in-out;
        }
        .stTextInput input:focus {
            border-color: #ffcc00;
            box-shadow: 0 0 12px #ffcc00;
        }

        .stButton button {
            background: linear-gradient(90deg, #ffcc00, #ff8800);
            color: black;
            font-size: 1.2rem;
            font-weight: bold;
            padding: 12px 28px;
            border-radius: 10px;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease-in-out;
            box-shadow: 0px 6px 18px rgba(0,0,0,0.25);
        }
        .stButton button:hover {
            background: linear-gradient(90deg, #ff8800, #ffcc00);
            transform: scale(1.05);
        }

        .feedback-box {
            background: rgba(255,255,255,0.1);
            padding: 18px;
            border-radius: 12px;
            font-size: 1.1rem;
            line-height: 1.6;
            margin-top: 12px;
            box-shadow: inset 0px 3px 10px rgba(0,0,0,0.25);
        }

        @keyframes fadeIn {
            from {opacity: 0; transform: translateY(10px);}
            to {opacity: 1; transform: translateY(0);}
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🤖 AI Tips")
    st.write("<h3 style='text-align:center;'>Get personalized tips based on your skill and academic points.</h3>", unsafe_allow_html=True)

    skill_input = st.text_input("🎯 Your Skill Points (0–100)", placeholder="e.g. 45")
    study_input = st.text_input("📚 Your Academic Points (0–100)", placeholder="e.g. 70")

    if st.button("✅ Submit Points"):
        if skill_input and study_input:
            try:
                skill_score = int(skill_input)
                study_score = int(study_input)

                if 0 <= skill_score <= 100 and 0 <= study_score <= 100:
                    skill_level = classify(skill_score)
                    study_level = classify(study_score)

                    st.markdown("<h2>🧠 Personalized Feedback Plan:</h2>", unsafe_allow_html=True)
                    
                    st.subheader("🛠️ Skills")
                    st.markdown(f"<div class='feedback-box'>{feedback_library['skills'][skill_level]}</div>", unsafe_allow_html=True)

                    st.subheader("📚 Academics")
                    st.markdown(f"<div class='feedback-box'>{feedback_library['academics'][study_level]}</div>", unsafe_allow_html=True)
                else:
                    st.error("⚠️ Please enter scores between 0 and 100.")
            except ValueError:
                st.error("❌ Please enter valid numbers.")
        else:
            st.warning("⚠️ Please fill in both fields before submitting.")

def page_consult():
    # Inject Custom CSS
    st.markdown("""
        <style>
        /* Page background and text */
        .main {
            background: linear-gradient(135deg, #16213e, #1a1a2e);
            color: white;
            font-family: 'Segoe UI', sans-serif;
        }

        /* Title */
        h1 {
            font-size: 3rem !important;
            color: #ffcc00;
            text-align: center;
            font-weight: bold;
        }

        /* Subtitle */
        h2, h3 {
            color: #00ffea;
            font-size: 1.6rem !important;
        }

        /* Input Fields */
        .stTextInput input, .stTextArea textarea, .stSelectbox select {
            font-size: 1.2rem !important;
            padding: 12px;
            border-radius: 10px;
            border: 2px solid #00ffea;
            background-color: #0f3460;
            color: white;
        }

        /* Dropdown (Selectbox) */
        .stSelectbox div[data-baseweb="select"] > div {
            font-size: 1.2rem !important;
            background-color: #0f3460;
            border-radius: 10px;
            border: 2px solid #00ffea;
            color: white;
        }

        /* Buttons */
        .stButton button, .stFormSubmitButton button {
            background: linear-gradient(90deg, #ffcc00, #ff8800);
            color: black;
            font-size: 1.3rem;
            font-weight: bold;
            padding: 12px 25px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
        }
        .stButton button:hover, .stFormSubmitButton button:hover {
            background: linear-gradient(90deg, #ff8800, #ffcc00);
            transform: scale(1.05);
        }

        /* Divider Line */
        hr {
            border: 1px solid rgba(255,255,255,0.3);
        }

        /* Quick Resources Links */
        a {
            color: #ffcc00 !important;
            font-weight: bold;
        }

        /* Quick Chatbox */
        .stInfo {
            background-color: rgba(255,255,255,0.08);
            padding: 12px;
            border-radius: 8px;
            font-size: 1.1rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Page content
    st.title("📞 Book a Consultation")

    st.markdown("""
    <p style='font-size:1.2rem; text-align:center;'>
    Need professional advice or mentorship? Fill out the form below and one of our career or academic advisors will get in touch with you.<br><br>
    Whether you're facing confusion about your path, want advice on improving skills or academics, or just need someone to talk to — we're here for you.
    </p>
    """, unsafe_allow_html=True)

    # Consultation Form
    with st.form("consult_form", clear_on_submit=True):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number (Optional)")
        topic = st.selectbox("What would you like to consult about?", [
            "Career Guidance",
            "Skill Development",
            "Academic Support",
            "Mental Health",
            "Other"
        ])
        message = st.text_area("Briefly describe your concern")

        submitted = st.form_submit_button("📨 Submit Request")

        if submitted:
            if name and email and message:
                st.success("✅ Your request has been received! Our team will contact you within 48 hours.")
            else:
                st.warning("⚠️ Please fill out all required fields.")

    st.markdown("---")

    # Quick Resources
    st.subheader("🧠 Need Immediate Help?")
    st.markdown("""
    - **Mental Health Support:** [iCall - Free 24/7 Helpline](https://icallhelpline.org)
    - **Career Resources:** [LinkedIn Career Explorer](https://linkedin.github.io/career-explorer/)
    - **Free Skill Courses:** [Coursera Free Courses](https://www.coursera.org/courses?query=free)

    📘 You can also use the **AI Tips** section for instant feedback based on your current scores.
    """)

    # Quick Advice Chatbox
    st.markdown("### 💬 Need Quick Advice?")
    quick_question = st.text_input("Ask your quick question here...")
    if quick_question:
        st.info("🤖 This is a placeholder response: 'Thank you for your question. One of our team members will get back to you shortly.'")

def ai_brain_games():
    st.subheader("🤖 AI Brain Games (Gemini)")
    choice = st.selectbox("Type:", ["AI Trivia", "AI Riddle", "Logic Puzzle"])
    if "ai_q" not in st.session_state:
        st.session_state.ai_q = None
        st.session_state.ai_a = None

    if st.button("🎲 Get Challenge"):
        if choice == "AI Trivia":
            prompt = "Give one interesting short general-knowledge trivia question and its answer. Format: Question: ... Answer: ..."
        elif choice == "AI Riddle":
            prompt = "Give one concise riddle and its answer. Format: Riddle: ... Answer: ..."
        else:
            prompt = "Give one short logical puzzle (2-3 sentences) and its solution. Format: Puzzle: ... Solution: ..."
        try:
            # response = genai.GenerativeModel(MODEL).generate_content(prompt)
            # text = response.text.strip()
            # For offline / placeholder (if Gemini not configured), use fallback:
            text = "Question: What gas do plants take in for photosynthesis? Answer: Carbon dioxide"
            # --- Uncomment above and remove fallback when Gemini is configured. ---
            parts = text.split("Answer:") if "Answer:" in text else text.split("Solution:")
            st.session_state.ai_q = parts[0].strip()
            st.session_state.ai_a = parts[1].strip() if len(parts) > 1 else "Answer not found"
        except Exception as e:
            st.error(f"AI error: {e}")
    if st.session_state.get("ai_q"):
        st.markdown("**Challenge:**")
        st.write(st.session_state.ai_q)
        ans = st.text_input("Your Answer:", key="ai_user_ans")
        if st.button("✅ Submit Answer"):
            user = ans.strip().lower()
            correct = st.session_state.ai_a.strip().lower()
            if user and user in correct:
                st.success("🎉 Correct!")
            else:
                st.error(f"❌ Not correct. Solution: {st.session_state.ai_a}")

# ---------------- Tower of Hanoi ----------------
def tower_of_hanoi():
    st.markdown("""
    <style>
        .disk {
            background: #222; /* dark background for disks */
            color: white;     /* white dots */
            padding: 6px;
            border-radius: 8px;
            text-align: center;
            margin: 4px 0;
            font-size: 18px;
            font-family: monospace;
        }
        .peg-title {
            text-align: center;
            font-weight: bold;
            margin-bottom: 8px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.subheader("🗼 Tower of Hanoi")
    if "hanoi" not in st.session_state:
        st.session_state.hanoi = [[4, 3, 2, 1], [], []]  # default 4 disks

    pegs = st.session_state.hanoi
    st.write("Pegs (bottom → top):")

    cols = st.columns(3)
    for i, peg in enumerate(pegs):
        with cols[i]:
            st.markdown(f"<div class='peg-title'>Peg {i+1}</div>", unsafe_allow_html=True)
            for disk in reversed(peg):
                st.markdown(
                    f"<div class='disk'>{'●' * disk}</div>",
                    unsafe_allow_html=True
                )

    f = st.selectbox("From peg", [1, 2, 3], index=0)
    t = st.selectbox("To peg", [1, 2, 3], index=1)

    if st.button("Move"):
        f_idx, t_idx = f - 1, t - 1
        if pegs[f_idx] and (not pegs[t_idx] or pegs[f_idx][-1] < pegs[t_idx][-1]):
            pegs[t_idx].append(pegs[f_idx].pop())
        else:
            st.error("❌ Invalid move.")

    total_disks = sum(len(p) for p in pegs)
    if pegs == [[], [], list(range(total_disks, 0, -1))]:
        st.success("🎉 Solved!")

    if st.button("🔄 Reset Hanoi"):
        st.session_state.hanoi = [[4, 3, 2, 1], [], []]

# ---------------- N-Queens ----------------
def n_queens_game():
    st.subheader("♟️ N-Queens (place non-attacking queens)")
    n = st.slider("N (board size)", 4, 10, 8)
    if "nq_positions" not in st.session_state or st.session_state.get("nq_n") != n:
        st.session_state.nq_positions = [-1]*n  # column index for each row, -1 = empty
        st.session_state.nq_n = n
    cols = []
    st.write("Choose one column (0-based) per row, or -1 for empty:")
    for r in range(n):
        st.session_state.nq_positions[r] = st.selectbox(f"Row {r}", options=list(range(-1, n)), index=(st.session_state.nq_positions[r]+1 if st.session_state.nq_positions[r]>=0 else 0), key=f"nq_{r}")
    def valid_positions(pos):
        for r1 in range(n):
            c1 = pos[r1]
            if c1 == -1: continue
            for r2 in range(r1+1, n):
                c2 = pos[r2]
                if c2 == -1: continue
                if c1 == c2 or abs(c1-c2) == abs(r1-r2):
                    return False
        return True
    if st.button("Check N-Queens"):
        if valid_positions(st.session_state.nq_positions):
            if all(c!=-1 for c in st.session_state.nq_positions):
                st.success("🎉 Valid solution — no queens attack each other!")
            else:
                st.info("✅ No conflicts so far, but some rows are empty.")
        else:
            st.error("❌ Conflict detected!")
    if st.button("Random Solve"):
        # simple backtracking to find any solution
        sol = [-1]*n
        def bt(row):
            if row==n: return True
            for col in range(n):
                ok=True
                for r in range(row):
                    if sol[r]==col or abs(sol[r]-col)==abs(r-row):
                        ok=False; break
                if ok:
                    sol[row]=col
                    if bt(row+1): return True
                    sol[row]=-1
            return False
        bt(0)
        st.session_state.nq_positions = sol
        for r in range(n):
            st.selectbox(f"Row {r}", options=list(range(-1,n)), index=sol[r]+1 if sol[r]>=0 else 0, key=f"nq_{r}")

# ---------------- Maze (DFS generator + BFS solution) ----------------
def generate_maze(w=15, h=11):
    # cell-based maze with walls; return grid of 0=wall,1=path
    W, H = w, h
    maze = [[0]*W for _ in range(H)]
    visited = [[False]*W for _ in range(H)]
    dirs = [(0,1),(1,0),(0,-1),(-1,0)]
    def inb(x,y): return 0<=x<W and 0<=y<H
    # carve using DFS on odd coordinates only for paths
    def dfs(x,y):
        visited[y][x]=True
        maze[y][x]=1
        order = dirs[:]
        random.shuffle(order)
        for dx,dy in order:
            nx,ny = x+2*dx, y+2*dy
            if inb(nx,ny) and not visited[ny][nx]:
                maze[y+dy][x+dx]=1
                dfs(nx,ny)
    # start at (1,1)
    dfs(1,1)
    return maze

def solve_maze(maze, start=(1,1), end=None):
    H = len(maze); W = len(maze[0])
    if not end:
        # find bottom-right path cell
        for y in range(H-1, -1, -1):
            for x in range(W-1, -1, -1):
                if maze[y][x]==1:
                    end=(x,y); break
            if end: break
    q = deque([start])
    prev = {start: None}
    dirs = [(0,1),(1,0),(0,-1),(-1,0)]
    while q:
        x,y = q.popleft()
        if (x,y)==end: break
        for dx,dy in dirs:
            nx,ny = x+dx, y+dy
            if 0<=nx<W and 0<=ny<H and maze[ny][nx]==1 and (nx,ny) not in prev:
                prev[(nx,ny)] = (x,y)
                q.append((nx,ny))
    if end not in prev and start!=end: return []
    # reconstruct path
    path=[]
    cur=end
    while cur:
        path.append(cur); cur=prev[cur]
    path.reverse()
    return path

def maze_game():
    st.subheader("🧭 Maze (Find the path)")
    w = st.slider("Width (odd)", 11, 31, 15, 2)
    h = st.slider("Height (odd)", 7, 21, 11, 2)
    if "maze" not in st.session_state or st.session_state.get("maze_wh") != (w,h):
        st.session_state.maze = generate_maze(w,h)
        st.session_state.maze_wh = (w,h)
        st.session_state.maze_solution = None
    if st.button("Generate Maze"):
        st.session_state.maze = generate_maze(w,h)
        st.session_state.maze_solution = None
    maze = st.session_state.maze
    # display maze using emojis for simplicity
    s = ""
    for y,row in enumerate(maze):
        for x,val in enumerate(row):
            s += "⬜" if val==1 else "⬛"
        s += "\n"
    st.text(s)
    if st.button("Show Solution"):
        path = solve_maze(maze)
        st.session_state.maze_solution = path
    if st.session_state.get("maze_solution"):
        path = set(st.session_state.maze_solution)
        s2 = ""
        for y,row in enumerate(maze):
            for x,val in enumerate(row):
                if (x,y) in path:
                    s2 += "🔵"
                else:
                    s2 += "⬜" if val==1 else "⬛"
            s2 += "\n"
        st.text(s2)

# ---------------- Simon Memory ----------------
def simon_memory():
    st.subheader("🎵 Simon Memory (repeat the sequence)")
    colors = ["🔴","🟢","🔵","🟡"]
    if "simon_seq" not in st.session_state:
        st.session_state.simon_seq = []
        st.session_state.simon_step = 0
        st.session_state.simon_playing = False
        st.session_state.simon_score = 0
    if st.button("Start Round"):
        st.session_state.simon_seq.append(random.choice(colors))
        st.session_state.simon_playing = True
        st.session_state.simon_step = 0
        # show sequence briefly
        seq_display = " ".join(st.session_state.simon_seq)
        st.info(f"Watch: {seq_display}")
        time.sleep(0.8 + 0.2*len(st.session_state.simon_seq))
        st.rerun()
    st.write("Repeat the sequence by pressing buttons in order.")
    cols = st.columns(4)
    for i, col in enumerate(cols):
        if col.button(colors[i]):
            # user clicked a color
            if not st.session_state.simon_seq:
                st.warning("Press Start Round first!")
            else:
                expected = st.session_state.simon_seq[st.session_state.simon_step]
                if colors[i] == expected:
                    st.session_state.simon_step += 1
                    if st.session_state.simon_step == len(st.session_state.simon_seq):
                        st.success("✅ Correct sequence!")
                        st.session_state.simon_score += 1
                        st.session_state.simon_playing = False
                        st.session_state.simon_step = 0
                else:
                    st.error(f"❌ Wrong! Expected {expected}")
                    st.session_state.simon_seq = []
                    st.session_state.simon_step = 0
    st.info(f"High Score: {st.session_state.simon_score}")

def mastermind_game():
    st.subheader("🔐 Mastermind (Code Breaker)")
    colors = ["Red", "Green", "Blue", "Yellow", "Orange", "Purple"]
    if "mm_secret" not in st.session_state:
        st.session_state.mm_secret = [random.choice(colors) for _ in range(4)]
        st.session_state.mm_history = []  # list of (guess, (black, white))
    st.write("Guess the secret sequence of 4 colors. Duplicates allowed.")

    cols = st.columns(4)
    guess = []
    for i in range(4):
        guess.append(cols[i].selectbox(f"Pos {i+1}", colors, key=f"mm_{i}"))
    if st.button("Submit Guess"):
        secret = st.session_state.mm_secret[:]
        g = guess[:]
        # compute blacks
        black = sum(1 for i in range(4) if g[i] == secret[i])
        # compute whites (color matches excluding blacks)
        # remove blacks
        secret_unmatched = [secret[i] for i in range(4) if g[i] != secret[i]]
        guess_unmatched = [g[i] for i in range(4) if g[i] != secret[i]]
        white = 0
        for color in set(guess_unmatched):
            white += min(secret_unmatched.count(color), guess_unmatched.count(color))
        st.session_state.mm_history.insert(0, (g, (black, white)))
        if black == 4:
            st.success("🎉 You cracked the code!")
            st.balloons()
            if st.button("New Game"):
                st.session_state.mm_secret = [random.choice(colors) for _ in range(4)]
                st.session_state.mm_history = []
        else:
            st.info(f"Black pegs (correct place): {black} — White pegs (correct color wrong place): {white}")

    if st.session_state.mm_history:
        st.markdown("**History (most recent first):**")
        for guess, (b, w) in st.session_state.mm_history[:10]:
            st.write(f"{guess} → Black: {b}, White: {w}")

# ---------------- 15-Puzzle (Sliding) ----------------
def fifteen_puzzle_game():
    st.subheader("🔳 15-Puzzle (Sliding Puzzle)")
    size = 4
    total = size * size
    if "fp_board" not in st.session_state:
        arr = list(range(1, total))
        arr.append(0)  # 0 is empty
        # shuffle until solvable (simple approach: shuffle until not solved)
        while True:
            random.shuffle(arr)
            if arr != list(range(1, total)) + [0]:
                break
        st.session_state.fp_board = arr

    board = st.session_state.fp_board

    # helper to find index of 0 and neighbors
    empty_idx = board.index(0)

    st.write("Click a tile adjacent to the empty spot to move it.")
    # render grid of buttons
    for r in range(size):
        cols = st.columns(size)
        for c in range(size):
            idx = r * size + c
            val = board[idx]
            label = " " if val == 0 else str(val)
            # use a unique key per button
            if cols[c].button(label, key=f"fp_{idx}"):
                # attempt move: if clicked tile adjacent to empty, swap
                er, ec = divmod(empty_idx, size)
                rr, rc = divmod(idx, size)
                if abs(er - rr) + abs(ec - rc) == 1:
                    board[empty_idx], board[idx] = board[idx], board[empty_idx]
                    st.session_state.fp_board = board
                else:
                    st.warning("Tile not adjacent to empty spot!")

    if board == list(range(1, total)) + [0]:
        st.success("🎉 Puzzle solved!")

    if st.button("Reset 15-Puzzle"):
        arr = list(range(1, total)) + [0]
        random.shuffle(arr)
        st.session_state.fp_board = arr

# ---------------- Reaction Time Test ----------------
def reaction_time_test():
    st.subheader("⚡ Reaction Time Test")
    if "rt_state" not in st.session_state:
        st.session_state.rt_state = "ready"  # ready -> waiting -> click -> result
        st.session_state.rt_start = None
        st.session_state.rt_end = None
        st.session_state.rt_best = None

    if st.session_state.rt_state == "ready":
        st.write("Press **Start**, then wait for the 'CLICK' button to appear and press it as fast as you can.")
        if st.button("Start"):
            st.session_state.rt_state = "waiting"
            delay = random.uniform(1.2, 3.0)
            st.session_state.rt_start = time.time() + delay
            st.rerun()

    elif st.session_state.rt_state == "waiting":
        # If current time hasn't reached start, show waiting message
        now = time.time()
        if now < st.session_state.rt_start:
            st.write("Get ready... (wait for it)")
            # simple short sleep so it feels dynamic (non-blocking effect is limited)
            time.sleep(0.05)
            st.rerun()
        else:
            st.session_state.rt_state = "click"
            st.rerun()

    elif st.session_state.rt_state == "click":
        if st.button("CLICK!"):
            st.session_state.rt_end = time.time()
            react = st.session_state.rt_end - st.session_state.rt_start
            st.session_state.rt_state = "result"
            # record best
            if st.session_state.rt_best is None or react < st.session_state.rt_best:
                st.session_state.rt_best = react
            st.session_state.rt_last = react
            st.rerun()
        else:
            st.write("Click the big 'CLICK!' button now!")

    elif st.session_state.rt_state == "result":
        last = st.session_state.get("rt_last", None)
        best = st.session_state.get("rt_best", None)
        if last is not None:
            st.write(f"Your reaction: **{last*1000:.0f} ms**")
            if last < 0.2:
                st.success("Amazing reflexes!")
            elif last < 0.35:
                st.info("Good reaction time.")
            else:
                st.warning("Practice to improve!")
            if best:
                st.write(f"Best: **{best*1000:.0f} ms**")
        if st.button("Try Again"):
            st.session_state.rt_state = "ready"
            st.session_state.rt_start = None
            st.session_state.rt_end = None
            st.rerun()
        if st.button("Reset Best"):
            st.session_state.rt_best = None

# ---------------- Word Ladder ----------------
def word_ladder_game():
    st.subheader("🔤 Word Ladder (Transform the word)")
    # small dictionary for challenges
    wordset = {"cold","cord","card","ward","warm","form","farm","fall","foil","fail","tail","tale","male","mile","mild","gold","golf","gale","bale","bail"}
    start, end = st.columns(2)
    start_word = start.text_input("Start word (4 letters)", value="cold")
    end_word = end.text_input("End word (4 letters)", value="warm")

    if len(start_word) != len(end_word) or len(start_word) < 3:
        st.warning("Use words of same length (recommend 4).")
        return

    if st.button("Get Challenge Example"):
        # compute shortest ladder using BFS (if exists)
        def neighbors(w):
            res=[]
            for i in range(len(w)):
                for ch in 'abcdefghijklmnopqrstuvwxyz':
                    nw = w[:i]+ch+w[i+1:]
                    if nw in wordset and nw != w:
                        res.append(nw)
            return res
        # BFS
        q = deque([[start_word]])
        visited = {start_word}
        found = None
        while q:
            path = q.popleft()
            wcur = path[-1]
            if wcur == end_word:
                found = path; break
            for nb in neighbors(wcur):
                if nb not in visited:
                    visited.add(nb)
                    q.append(path + [nb])
        if found:
            st.success("Example shortest ladder: " + " → ".join(found))
        else:
            st.info("No ladder found in small dictionary. Try different words.")

    st.markdown("Enter your ladder steps (comma separated). Example: cold, cord, card, ward, warm")
    seq = st.text_area("Your ladder")
    if st.button("Validate Ladder"):
        parts = [w.strip().lower() for w in seq.split(",") if w.strip()]
        valid = True
        if not parts or parts[0] != start_word.lower() or parts[-1] != end_word.lower():
            valid = False
            st.error("Ladder must start with start word and end with end word.")
        else:
            for i in range(len(parts)-1):
                a, b = parts[i], parts[i+1]
                if len(a) != len(b) or sum(1 for x,y in zip(a,b) if x!=y) != 1 or b not in wordset:
                    valid = False
                    st.error(f"Step invalid: {a} → {b}. Each step must change exactly one letter and be a valid word.")
                    break
        if valid:
            st.success("✅ Valid ladder! Nice work.")

# ---------------- Page Games Hub ----------------
def page_games():
    st.title("🎮 Skillzy — Game Hub (AI & Advanced Logic)")
    st.write("Pick a game to train IQ, memory, and problem solving.")

    game = st.selectbox("Choose a game:", [
        "AI Brain Games",
        "Tower of Hanoi",
        "N-Queens",
        "Maze",
        "Simon Memory",
        "Mastermind",
        "15-Puzzle",
        "Reaction Time",
        "Word Ladder"
    ])

    if game == "AI Brain Games":
        ai_brain_games()
    elif game == "Tower of Hanoi":
        tower_of_hanoi()
    elif game == "N-Queens":
        n_queens_game()
    elif game == "Maze":
        maze_game()
    elif game == "Simon Memory":
        simon_memory()
    elif game == "Mastermind":
        mastermind_game()
    elif game == "15-Puzzle":
        fifteen_puzzle_game()
    elif game == "Reaction Time":
        reaction_time_test()
    elif game == "Word Ladder":
        word_ladder_game()

def page_about():
    st.title("ℹ️ About")

    st.markdown("""
    <div style="font-family: 'Segoe UI', sans-serif; padding: 20px; background-color: #f9f9f9; border-radius: 12px; border: 1px solid #ddd;">
    
    <h1 style="color:#2c3e50; text-align:center;">Digi Dharma – <span style="color:#27ae60;">Shaping a Skillful Nation</span></h1>
    
    <p style="font-size:16px; color:#555; text-align:justify;">
    <b>Digi Dharma</b> is committed to bringing a <span style="color:#e67e22;">revolutionary shift</span> in the education system by moving away from outdated marks-based evaluation and embracing a <b>modern, skill-based assessment model</b>. 
    In today’s world, academic scores alone cannot define success — true potential is measured by 
    <span style="color:#2980b9;">creativity</span>, <span style="color:#8e44ad;">problem-solving</span>, <span style="color:#16a085;">adaptability</span>, communication, and emotional intelligence.
    </p>

    <p style="font-size:16px; color:#555; text-align:justify;">
    Our platform empowers youth and citizens across India to <b>track, measure, and continuously improve</b> their skill sets. Digi Dharma is not just a digital tool — it’s a 
    <span style="color:#c0392b;">personal growth companion</span> that identifies your strengths, pinpoints areas for improvement, 
    and provides <b>personalized feedback and development roadmaps</b>.
    </p>

    <h2 style="color:#34495e;">🌏 Our Vision</h2>
    <p style="font-size:16px; color:#555; text-align:justify;">
    To create a <b>future-ready, skillful society</b> that is confident, innovative, and prepared to tackle the challenges of the 21st century. With 
    <span style="color:#27ae60;">data-driven insights</span> and inclusive technology, we aim to make skill development accessible to all — from metropolitan cities to rural villages — 
    ensuring <b>no one is left behind</b>.
    </p>

    <h2 style="color:#34495e;">🎯 Our Core Objectives</h2>
    <ul style="font-size:16px; color:#555; line-height:1.8;">
        <li>Bridge the gap between education and real-world skills.</li>
        <li>Offer equal access to skill-building resources for all backgrounds.</li>
        <li>Encourage a lifelong learning mindset that adapts to changing needs.</li>
        <li>Contribute to India’s mission of becoming a global talent powerhouse.</li>
    </ul>

    <p style="font-size:16px; color:#555; text-align:justify;">
    With Digi Dharma, we are not just preparing individuals for jobs — we are preparing them for <b>life itself</b>. 
    Together, we will nurture a generation that is <span style="color:#27ae60;">skilled</span>, 
    <span style="color:#2980b9;">confident</span>, and ready to <b>lead the future</b>.
    </p>
    </div>
    """, unsafe_allow_html=True)

def chat_bot():
    # Peach + Black theme CSS
    st.markdown("""
        <style>
        .chat-container {
            max-width: 700px;
            margin: auto;
            background-color: #fff5eb; /* light peach background */
            padding: 20px;
            border-radius: 10px;
            font-family: Arial, sans-serif;
        }
        .user-bubble {
            background-color: #ffd6a5; /* peach */
            color: black;
            padding: 10px 15px;
            border-radius: 15px;
            margin: 5px;
            text-align: right;
            display: inline-block;
            max-width: 70%;
            float: right;
            clear: both;
        }
        .bot-bubble {
            background-color: #ffffff; /* white */
            color: black;
            padding: 10px 15px;
            border-radius: 15px;
            margin: 5px;
            text-align: left;
            display: inline-block;
            max-width: 70%;
            float: left;
            clear: both;
        }
        .role-label {
            font-size: 0.8rem;
            color: #444;
            margin-bottom: 2px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("💬 Skillzy Chatbot")
    st.write("Your friendly AI study & skill buddy 📚🤝")

    # Model fixed
    model_name = "gemini-1.5-flash"

    if "chat" not in st.session_state or st.session_state.get("model_name") != model_name:
        st.session_state.model_name = model_name
        st.session_state.chat = genai.GenerativeModel(model_name).start_chat(history=[])

    # Chat history display
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for turn in st.session_state.chat.history:
        if turn.role == "user":
            st.markdown(f'<div class="user-bubble">🧑‍🎓 {turn.parts[0].text}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-bubble">🤖 {turn.parts[0].text}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Input
    user_input = st.text_input("Type your message here... 💬")
    if st.button("Send 🚀"):
        if user_input.strip():
            try:
                st.session_state.chat.send_message(user_input)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please type something before sending.")

def get_ai_quote():
    prompt = "Give me a short motivational quote for students."
    model = genai.GenerativeModel(DEFAULT_MODEL)
    response = model.generate_content(prompt)
    return response.text.strip()

def get_ai_history_fact():
    today = datetime.datetime.now().strftime("%B %d")
    prompt = f"Tell me an interesting historical event that happened on {today}, in 2-3 sentences."
    model = genai.GenerativeModel(DEFAULT_MODEL)
    response = model.generate_content(prompt)
    return response.text.strip()


def main():
    st.set_page_config(page_title="Skillzy", layout="wide")

    # --- Custom CSS Styling (unchanged) ---
    st.markdown("""
        <style>
        .sidebar .sidebar-content {
            background: linear-gradient(180deg, #1e3a8a, #3b82f6);
            color: white;
            font-size: 11px;
        }
        .fun-zone {
            background: #111827;
            padding: 10px;
            border-radius: 10px;
            margin-top: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            font-size: 13px;
        }
        .fun-zone h4 {
            color: #facc15;
            text-align: center;
            font-size: 14px;
        }
        .stButton>button {
            background: #2563eb;
            color: white;
            border-radius: 8px;
            padding: 4px 10px;
            border: none;
            font-size: 12px;
        }
        .stButton>button:hover {
            background: #facc15;
            color: black;
        }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar (left side - fun interactive panel)
    with st.sidebar:
        st.title("🎉 Skillzy Fun Zone")
        st.markdown("---")

        # --- Daily Motivation Quote (AI) ---
        with st.container():
            st.markdown("<div class='fun-zone'>", unsafe_allow_html=True)
            st.markdown("#### 💡 Daily Quote")
            if st.button("Get Quote"):
                ai_quote = get_ai_quote()
                st.info(ai_quote)
            st.markdown("</div>", unsafe_allow_html=True)

        # --- This Day in History (AI) ---
        with st.container():
            st.markdown("<div class='fun-zone'>", unsafe_allow_html=True)
            st.markdown("#### 📅 This Day in History")
            if st.button("Get History Fact"):
                ai_fact = get_ai_history_fact()
                st.success(ai_fact)
            st.markdown("</div>", unsafe_allow_html=True)

    # --- Main area with tabs (unchanged) ---
    st.title("Skillzy - Empowering Youth with Skills")

    pages = {
        "Welcome": welcome_page,
        "AI Tips": page_ai_tips,
        "Consult": page_consult,
        "Games": page_games,
        "Chat Bot": chat_bot,
        "About": page_about,
    }

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(list(pages.keys()))

    with tab1:
        pages["Welcome"]()
    with tab2:
        pages["AI Tips"]()
    with tab3:
        pages["Consult"]()
    with tab4:
        pages["Games"]()
    with tab5:
        pages["Chat Bot"]()
    with tab6:
        pages["About"]()
if __name__ == "__main__":
    main()
