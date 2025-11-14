import streamlit as st
import random
import time
import datetime

# --- Page Config ---
st.set_page_config(page_title="Typing Speed Test", layout="centered")

# --- Paragraphs (instead of sentences) ---
PARAGRAPHS = [
    """The quick brown fox jumps over the lazy dog. This pangram contains every letter of the alphabet at least once. 
    It is commonly used for testing keyboards and typing speed. Practice makes perfect, and consistent effort leads to improvement.""",

    """Python is a high-level, interpreted programming language known for its simplicity and readability. 
    It supports multiple programming paradigms, including procedural, object-oriented, and functional programming. 
    Developers love Python for rapid prototyping and building scalable applications.""",

    """Typing speed is measured in words per minute (WPM). Accuracy is equally important because mistakes reduce effective speed. 
    Professional typists often achieve over 80 WPM with 98% accuracy. Regular practice with varied text improves both metrics.""",

    """Technology evolves rapidly. Artificial intelligence, machine learning, and cloud computing are transforming industries. 
    Staying updated with new tools and frameworks is essential for developers. Online platforms provide excellent resources for continuous learning.""",

    """Good posture and finger placement are crucial for efficient typing. The home row keys (ASDF for left hand, JKL; for right) 
    serve as the foundation. Keep wrists elevated and fingers curved. Avoid looking at the keyboard to build muscle memory."""
]

# --- Word list (for word mode) ---
WORDS = [
    "the", "quick", "brown", "fox", "jumps", "over", "lazy", "dog", "python",
    "programming", "keyboard", "typing", "practice", "speed", "accuracy",
    "challenge", "test", "computer", "monitor", "screen", "development",
    "software", "hardware", "internet", "network", "server", "algorithm",
    "database", "function", "variable", "class", "object", "method", "loop"
]

# --- Session State ---
if 'test_active' not in st.session_state:
    st.session_state.test_active = False
    st.session_state.practice_mode = False
    st.session_state.mode = "words"  # "words", "paragraphs"
    st.session_state.round = 1
    st.session_state.total_rounds = 10
    st.session_state.score = 0
    st.session_state.total_time = 0
    st.session_state.correct_chars = 0
    st.session_state.total_chars = 0
    st.session_state.start_time = None
    st.session_state.current_text = ""
    st.session_state.user_input = ""
    st.session_state.history = []
    st.session_state.dark_mode = False

# --- Functions ---
def get_random_text():
    if st.session_state.mode == "words":
        return " ".join(random.sample(WORDS, k=random.randint(8, 15)))
    else:  # paragraphs
        return random.choice(PARAGRAPHS).strip()

def highlight_text(target, typed):
    parts = []
    for i in range(len(typed)):
        if i < len(target) and typed[i] == target[i]:
            parts.append(f"<span style='color:#27ae60'>{typed[i]}</span>")
        else:
            parts.append(f"<span style='color:#e74c3c;background:#fadbd8'>{typed[i]}</span>")
    remaining = target[len(typed):] if len(typed) < len(target) else ""
    if remaining:
        parts.append(f"<span style='color:#95a5a6'>{remaining}</span>")
    return "".join(parts)

def calculate_wpm(correct_chars, seconds):
    if seconds <= 0:
        return 0
    return (correct_chars / 5) / (seconds / 60)

def save_result():
    if st.session_state.total_chars == 0:
        return
    wpm = calculate_wpm(st.session_state.correct_chars, st.session_state.total_time)
    accuracy = (st.session_state.correct_chars / st.session_state.total_chars) * 100
    st.session_state.history.append({
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "wpm": round(wpm, 1),
        "accuracy": round(accuracy, 1),
        "score": st.session_state.score,
        "mode": st.session_state.mode
    })

def reset_test():
    st.session_state.test_active = False
    st.session_state.practice_mode = False
    st.session_state.round = 1
    st.session_state.score = 0
    st.session_state.total_time = 0
    st.session_state.correct_chars = 0
    st.session_state.total_chars = 0
    st.session_state.current_text = get_random_text()

# --- UI Styling ---
st.markdown(
    """
    <style>
    .main { padding: 2rem; }
    .stButton>button { width: 100%; margin: 0.5rem 0; }
    .text-display { 
        font-size: 1.4rem; 
        font-family: 'Courier New', monospace; 
        padding: 1.5rem; 
        background: #f8f9fa; 
        border-radius: 12px; 
        line-height: 1.6;
        white-space: pre-wrap;
        border: 1px solid #ddd;
    }
    .input-box textarea { 
        font-size: 1.3rem !important; 
        font-family: 'Courier New', monospace !important; 
        line-height: 1.6 !important;
    }
    .stats { display: flex; justify-content: space-around; flex-wrap: wrap; gap: 1rem; margin: 1rem 0; }
    .stat-box { background: #e9ecef; padding: 1rem; border-radius: 10px; min-width: 120px; text-align: center; }
    </style>
    """, unsafe_allow_html=True
)

# --- Header ---
st.title("Typing Speed Test")

# --- Controls ---
col1, col2 = st.columns(2)
with col1:
    if st.button("Start Test"):
        reset_test()
        st.session_state.test_active = True
        st.session_state.start_time = time.time()
        st.rerun()

with col2:
    if st.button("Start Practice"):
        reset_test()
        st.session_state.practice_mode = True
        st.session_state.test_active = True
        st.session_state.start_time = time.time()
        st.rerun()

st.markdown("---")

# --- Mode Selection ---
mode_col1, mode_col2 = st.columns(2)
with mode_col1:
    if st.button("Random Words"):
        st.session_state.mode = "words"
        st.success("Mode: Random Words")
with mode_col2:
    if st.button("Random Paragraph"):
        st.session_state.mode = "paragraphs"
        st.success("Mode: Random Paragraphs")

# --- Dark Mode ---
if st.button("Enable Dark Mode" if not st.session_state.dark_mode else "Disable Dark Mode"):
    st.session_state.dark_mode = not st.session_state.dark_mode
    st.rerun()

# Apply Dark Mode
if st.session_state.dark_mode:
    st.markdown(
        """
        <style>
        .stApp { background: #1a1a2e; color: #eee; }
        .text-display { background: #16213e; color: #ddd; border: 1px solid #444; }
        .stat-box { background: #16213e; color: #a29bfe; }
        </style>
        """, unsafe_allow_html=True
    )

# --- Test / Practice Logic ---
if st.session_state.test_active:
    if not st.session_state.current_text:
        st.session_state.current_text = get_random_text()

    st.markdown("---")
    if not st.session_state.practice_mode:
        st.write(f"**Round {st.session_state.round}/{st.session_state.total_rounds}** | Mode: **{st.session_state.mode.title()}**")

    # Display Target Text
    st.markdown(f"<div class='text-display'>{st.session_state.current_text}</div>", unsafe_allow_html=True)

    # Input Area
    user_input = st.text_area(
        "Type the text above:",
        value=st.session_state.user_input,
        height=160,
        key="typing_input",
        label_visibility="collapsed"
    )

    # Auto-submit when user presses Enter (ends with \n)
    if user_input.endswith("\n"):
        user_input = user_input.strip()
        st.session_state.user_input = ""

        end_time = time.time()
        time_taken = end_time - st.session_state.start_time

        # Count correct characters
        correct_chars = sum(a == b for a, b in zip(st.session_state.current_text, user_input))
        total_chars = len(st.session_state.current_text)

        st.session_state.correct_chars += correct_chars
        st.session_state.total_chars += total_chars
        st.session_state.total_time += time_taken

        is_correct = user_input == st.session_state.current_text
        if is_correct:
            st.session_state.score += 10

        # Feedback
        st.markdown("---")
        st.markdown("**Your typing:**")
        st.markdown(f"<div style='font-family:monospace;font-size:1.3rem;'>{highlight_text(st.session_state.current_text, user_input)}</div>", unsafe_allow_html=True)

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Time", f"{time_taken:.2f}s")
        with col_b:
            st.metric("Chars Correct", f"{correct_chars}/{total_chars}")
        with col_c:
            st.metric("Match", "Yes" if is_correct else "No")

        # Next Round or End
        if st.session_state.practice_mode:
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                if st.button("Next Practice"):
                    st.session_state.current_text = get_random_text()
                    st.session_state.start_time = time.time()
                    st.rerun()
            with col_p2:
                if st.button("Stop Practice"):
                    save_result()
                    st.session_state.test_active = False
                    st.session_state.practice_mode = False
                    st.rerun()

        else:
            if st.session_state.round < st.session_state.total_rounds:
                if st.button("Next Round"):
                    st.session_state.round += 1
                    st.session_state.current_text = get_random_text()
                    st.session_state.start_time = time.time()
                    st.rerun()
            else:
                if st.button("View Results"):
                    save_result()
                    st.session_state.test_active = False
                    st.rerun()

    else:
        # Start timer on first character
        if len(user_input) > 0 and st.session_state.start_time is None:
            st.session_state.start_time = time.time()

else:
    # --- Show Latest Result ---
    if st.session_state.history:
        latest = st.session_state.history[-1]
        st.markdown("## Latest Result")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("WPM", latest["wpm"])
        with col2:
            st.metric("Accuracy", f"{latest['accuracy']}%")
        with col3:
            st.metric("Score", latest["score"])
        with col4:
            st.write(f"**{latest['mode'].title()}**")

        share_text = f"I typed {latest['wpm']} WPM with {latest['accuracy']}% accuracy in {latest['mode']} mode! #TypingTest"
        st.code(share_text, language=None)

    # --- Progress History ---
    if st.button("Check Progress"):
        if st.session_state.history:
            st.markdown("## Progress History (Last 10)")
            for entry in st.session_state.history[::-1][:10]:
                st.write(f"**{entry['date']}** | {entry['mode'].title()} | WPM: {entry['wpm']} | Acc: {entry['accuracy']}% | Score: {entry['score']}")
        else:
            st.info("No test history yet. Complete a test!")

    # --- Try Again ---
    if st.button("Try Again"):
        reset_test()
        st.session_state.test_active = True
        st.session_state.start_time = time.time()
        st.rerun()

    # --- Share Results ---
    if st.button("Share Results"):
        if st.session_state.history:
            latest = st.session_state.history[-1]
            share = f"Typing Speed: {latest['wpm']} WPM | {latest['accuracy']}% accuracy | Mode: {latest['mode'].title()}"
            st.code(share)
            st.success("Copied to clipboard!")
        else:
            st.warning("Complete a test first!")

st.markdown("---")
st.caption("Built with ❤️ using Streamlit | Practice with **paragraphs** for real-world typing!")