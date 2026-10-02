import streamlit as st
import re

st.set_page_config(
    page_title="AI Interview Analyzer",
    page_icon="🎯",
    layout="wide"
)

# -----------------------------
# Helper Functions
# -----------------------------

STOP_WORDS = {
    "the", "a", "an", "and", "or", "to", "of", "in", "on",
    "for", "with", "is", "are", "was", "were", "i", "you",
    "my", "we", "it", "this", "that", "as", "at", "by",
    "from", "be", "have", "has", "had", "do", "did", "can",
    "could", "would", "should", "will", "about", "your",
    "our", "their", "they", "he", "she", "his", "her"
}


def get_words(text):
    return re.findall(
        r"[A-Za-z][A-Za-z0-9+#.-]*",
        text.lower()
    )


def keyword_score(answer, job_description):

    job_words = [
        word
        for word in get_words(job_description)
        if word not in STOP_WORDS and len(word) > 2
    ]

    if not job_words:
        return 70

    unique_words = set(job_words)
    answer_words = set(get_words(answer))

    matched_words = sum(
        1 for word in unique_words
        if word in answer_words
    )

    score = (matched_words / len(unique_words)) * 100

    return min(100, round(score))


def communication_score(answer):

    word_list = get_words(answer)

    if not word_list:
        return 0

    score = 55

    # Answer length
    if 40 <= len(word_list) <= 180:
        score += 15
    elif len(word_list) > 20:
        score += 8

    # Sentence structure
    sentences = [
        sentence.strip()
        for sentence in re.split(r"[.!?]+", answer)
        if sentence.strip()
    ]

    average_words = len(word_list) / max(len(sentences), 1)

    if 8 <= average_words <= 25:
        score += 15

    # Filler words
    fillers = re.findall(
        r"\b(um|uh|like|actually|basically|you know)\b",
        answer.lower()
    )

    if len(fillers) <= 3:
        score += 10
    elif len(fillers) > 8:
        score -= 10

    return max(0, min(100, score))


def structure_score(answer):

    text = answer.lower()

    score = 50

    structure_words = [
        "first",
        "second",
        "finally",
        "because",
        "therefore"
    ]

    example_words = [
        "example",
        "for instance",
        "project",
        "experience"
    ]

    if any(word in text for word in structure_words):
        score += 12

    if any(word in text for word in example_words):
        score += 15

    if len(get_words(answer)) >= 60:
        score += 15

    return min(100, score)


def technical_score(answer, job_description):

    job_words = set(
        word
        for word in get_words(job_description)
        if word not in STOP_WORDS
    )

    answer_words = set(get_words(answer))

    overlap = len(job_words.intersection(answer_words))

    score = 50 + min(35, overlap * 3)

    technical_terms = {
        "python",
        "java",
        "sql",
        "react",
        "javascript",
        "machine",
        "learning",
        "tensorflow",
        "api",
        "database",
        "cloud",
        "aws",
        "docker",
        "git",
        "spring",
        "algorithm",
        "model",
        "classification",
        "regression",
        "nlp",
        "rag",
        "streamlit"
    }

    score += min(
        15,
        len(answer_words.intersection(technical_terms)) * 3
    )

    return min(100, score)


def analyze_answer(answer, job_description):

    relevance = keyword_score(
        answer,
        job_description
    )

    communication = communication_score(
        answer
    )

    structure = structure_score(
        answer
    )

    technical = technical_score(
        answer,
        job_description
    )

    overall = round(
        (
            relevance
            + communication
            + structure
            + technical
        ) / 4
    )

    strengths = []
    improvements = []

    # Relevance
    if relevance >= 75:
        strengths.append(
            "Your answer is relevant to the job requirements."
        )
    else:
        improvements.append(
            "Include more concepts and keywords "
            "related to the job description."
        )

    # Communication
    if communication >= 75:
        strengths.append(
            "Your communication and sentence structure are good."
        )
    else:
        improvements.append(
            "Keep your answer clear, concise and easy to understand."
        )

    # Structure
    if structure >= 75:
        strengths.append(
            "Your answer has a reasonably good structure."
        )
    else:
        improvements.append(
            "Use the STAR method: Situation, Task, Action and Result."
        )

    # Technical
    if technical >= 75:
        strengths.append(
            "You included useful technical concepts."
        )
    else:
        improvements.append(
            "Mention specific technologies, tools, methods "
            "and project experience."
        )

    return {
        "overall": overall,
        "relevance": relevance,
        "communication": communication,
        "structure": structure,
        "technical": technical,
        "strengths": strengths,
        "improvements": improvements
    }


# -----------------------------
# Main UI
# -----------------------------

st.title("🎯 AI Interview Analyzer")

st.write(
    "Analyze interview answers and receive "
    "instant performance feedback."
)

# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.header("⚙️ Interview Setup")

    candidate_name = st.text_input(
        "Candidate Name",
        "Candidate"
    )

    target_role = st.text_input(
        "Target Role",
        "AI/ML Engineer"
    )

# -----------------------------
# Tabs
# -----------------------------

tab1, tab2, tab3 = st.tabs(
    [
        "📝 Interview Analyzer",
        "📊 Dashboard",
        "💡 Interview Tips"
    ]
)


# =====================================================
# TAB 1
# =====================================================

with tab1:

    col1, col2 = st.columns(2)

    with col1:

        question = st.text_area(
            "Interview Question",

            "Tell me about yourself and your "
            "AI/ML experience.",

            height=150
        )

    with col2:

        job_description = st.text_area(
            "Job Description",

            """
We are looking for an AI/ML Engineer with
Python, Machine Learning, TensorFlow, SQL,
NLP, Cloud, Git and problem-solving skills.
""",

            height=150
        )

    answer = st.text_area(
        "Candidate Answer",

        height=250,

        placeholder=(
            "Enter or paste the candidate's "
            "interview answer here..."
        )
    )

    analyze_button = st.button(
        "🔍 Analyze Interview",
        type="primary",
        use_container_width=True
    )

    if analyze_button:

        if not answer.strip():

            st.warning(
                "⚠️ Please enter an interview answer."
            )

        else:

            result = analyze_answer(
                answer,
                job_description
            )

            st.session_state["result"] = result

            st.success(
                "Interview answer analyzed successfully!"
            )

            st.subheader("📊 Interview Score")

            col1, col2, col3, col4, col5 = st.columns(5)

            col1.metric(
                "Overall",
                f"{result['overall']}%"
            )

            col2.metric(
                "Relevance",
                f"{result['relevance']}%"
            )

            col3.metric(
                "Communication",
                f"{result['communication']}%"
            )

            col4.metric(
                "Structure",
                f"{result['structure']}%"
            )

            col5.metric(
                "Technical",
                f"{result['technical']}%"
            )

            st.progress(
                result["overall"] / 100
            )

            # -------------------------
            # Strengths
            # -------------------------

            left, right = st.columns(2)

            with left:

                st.subheader("✅ Strengths")

                for strength in result["strengths"]:

                    st.success(
                        strength
                    )

            # -------------------------
            # Improvements
            # -------------------------

            with right:

                st.subheader("🚀 Areas for Improvement")

                for improvement in result["improvements"]:

                    st.warning(
                        improvement
                    )

            # -------------------------
            # Recommended Structure
            # -------------------------

            st.subheader(
                "💬 Recommended Answer Structure"
            )

            st.write(
                """
**1. Situation:** Explain the situation.

**2. Task:** Explain your responsibility.

**3. Action:** Explain what you did and
which technologies you used.

**4. Result:** Explain the final result
or measurable improvement.
"""
            )


# =====================================================
# TAB 2
# =====================================================

with tab2:

    st.header("📊 Candidate Dashboard")

    if "result" in st.session_state:

        result = st.session_state["result"]

        st.write(
            f"**Candidate:** {candidate_name}"
        )

        st.write(
            f"**Target Role:** {target_role}"
        )

        st.divider()

        scores = {

            "Overall Score":
                result["overall"],

            "Relevance":
                result["relevance"],

            "Communication":
                result["communication"],

            "Structure":
                result["structure"],

            "Technical":
                result["technical"]
        }

        for name, score in scores.items():

            st.write(
                f"**{name}: {score}%**"
            )

            st.progress(
                score / 100
            )

        st.divider()

        if result["overall"] >= 80:

            st.success(
                "⭐ Excellent interview performance!"
            )

        elif result["overall"] >= 60:

            st.info(
                "👍 Good performance. "
                "Continue improving."
            )

        else:

            st.error(
                "📚 More interview preparation "
                "is recommended."
            )

    else:

        st.info(
            "Analyze an interview answer first "
            "to view the dashboard."
        )


# =====================================================
# TAB 3
# =====================================================

with tab3:

    st.header(
        "💡 Interview Preparation Tips"
    )

    tips = [

        "Understand the job description before the interview.",

        "Give examples from your projects and internships.",

        "Use the STAR method for behavioral questions.",

        "Mention technologies used in your projects.",

        "Explain your role and contribution clearly.",

        "Avoid unnecessary filler words.",

        "Keep technical answers simple and structured.",

        "Mention measurable results whenever possible.",

        "Practice common HR and technical questions.",

        "Maintain confidence and professional communication."
    ]

    for index, tip in enumerate(tips, 1):

        st.write(
            f"**{index}.** {tip}"
        )


# -----------------------------
# Footer
# -----------------------------

st.divider()

st.caption(
    "AI Interview Analyzer | "
    "Python + Streamlit"
)
