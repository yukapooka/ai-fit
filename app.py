import streamlit as st

# ------------------------------
# Page configuration
# ------------------------------
st.set_page_config(
    page_title="AIFit",
    page_icon="🚀",
    layout="wide"
)


# ------------------------------
# App header
# ------------------------------
st.title("AIFit")
st.subheader("An AI product decision tool")

st.markdown(
    """
    AIFit helps product teams evaluate whether an AI feature is worth building, narrowing, prototyping, or avoiding by balancing AI fit, commercial potential, risk burden, and evidence readiness.
    """
)

st.divider()

# ------------------------------
# Example test cases
# ------------------------------
example_cases = {
    "Start from blank": {
        "feature_idea": "",
        "target_user": "",
        "user_problem": "",
        "ai_capability": "",
        "non_ai_alternative": "",
        "human_decision": "",
        "impact_if_wrong": "",
        "data_sensitivity": "",
        "business_value": "",
        "success_metric": "",
    },
    "AI Digital Twin for User Research Personas": {
        "feature_idea": "Create AI-generated user research personas based on interview transcripts, survey responses, and behavioral data.",
        "target_user": "Product managers, designers, and user researchers.",
        "user_problem": "Product teams want faster early-stage feedback before committing to prototypes or full research studies.",
        "ai_capability": "The AI synthesizes research data into personas and generates likely reactions to new feature ideas.",
        "non_ai_alternative": "Manual research synthesis, research repositories, and structured assumption-mapping workshops.",
        "human_decision": "Whether product teams treat AI-generated persona responses as hypotheses or as evidence of user demand.",
        "impact_if_wrong": "Teams may mistake synthetic feedback for real user validation and make poor roadmap decisions.",
        "data_sensitivity": "Medium to high. It may involve interview transcripts, survey data, and behavioral analytics.",
        "business_value": "Could reduce research bottlenecks and improve product discovery velocity.",
        "success_metric": "PMs and researchers generate better hypotheses without reducing real user research.",
    },
    "AI Grief Companion": {
        "feature_idea": "Create an AI companion that sends supportive messages or reflection prompts around difficult dates or moments.",
        "target_user": "People experiencing grief, loss, or emotionally difficult anniversaries.",
        "user_problem": "Users may want gentle support or structure during emotionally difficult moments.",
        "ai_capability": "The AI personalizes tone, timing, and reflective prompts based on user preferences and context.",
        "non_ai_alternative": "Scheduled reminders, static journaling prompts, therapist-written reflection guides, or support group referrals.",
        "human_decision": "Whether the user interprets the tool as reflection support or as an emotional substitute for human support.",
        "impact_if_wrong": "The feature may deepen dependency, simulate intimacy, or fail to escalate severe distress.",
        "data_sensitivity": "High. It may involve grief, emotional states, personal memories, and vulnerable user contexts.",
        "business_value": "Could create a differentiated wellbeing experience, but monetization must avoid exploiting vulnerability.",
        "success_metric": "Users feel supported and in control without feeling dependent, destabilized, or misled.",
    },
    "AI Financial Personality Profiler": {
        "feature_idea": "Analyze users’ spending patterns and assign financial personality profiles to personalize nudges and financial education.",
        "target_user": "Consumers using a personal finance or fintech app.",
        "user_problem": "Users want help understanding spending patterns and building healthier financial habits.",
        "ai_capability": "The AI identifies spending patterns, generates reflections, and personalizes educational content or nudges.",
        "non_ai_alternative": "Budgeting dashboards, spending categories, rule-based alerts, and static financial education modules.",
        "human_decision": "Whether users treat the profile as a helpful reflection or as a fixed judgment about their identity.",
        "impact_if_wrong": "Users may feel shamed, misclassified, manipulated, or steered toward unsuitable financial products.",
        "data_sensitivity": "High. It involves financial behavior, spending patterns, and possible socioeconomic inference.",
        "business_value": "High potential for engagement, retention, personalization, and monetizable financial journeys.",
        "success_metric": "Users feel helped, not judged or pressured, and understand the feature as editable reflection rather than fixed profiling.",
    },
}

# ------------------------------
# Sidebar example selector
# ------------------------------
st.sidebar.header("Try an example test case")
selected_case = st.sidebar.selectbox(
    "Choose a test case",
    list(example_cases.keys())
)

case = example_cases[selected_case]

# ------------------------------
# Input form
# ------------------------------
st.header("1. Describe the AI feature")

with st.form("feature_form"):
    feature_idea = st.text_area(
        "Feature_idea",
        value=case["feature_idea"],
        height=100
    )

    col1, col2 = st.columns(2)
    
    with col1:
        target_user = st.text_area(
            "Target_user",
            value=case["target_user"],
            height=90
        )
        user_problem = st.text_area(
            "User_problem",
            value=case["user_problem"],
            height=90
        )
        ai_capability = st.text_area(
            "AI_capability",
            value=case["ai_capability"],
            height=90
        )
        non_ai_alternative = st.text_area(
            "Current non-AI alternative",
            value=case["non_ai_alternative"],
            height=90
        )
    with col2:
        human_decision = st.text_area(
            "Human_decision",
            value=case["human_decision"],
            height=90
        )
        impact_if_wrong = st.text_area(
            "Impact_if_wrong",
            value=case["impact_if_wrong"],
            height=90
        )
        data_sensitivity = st.text_area(
            "Data_sensitivity",
            value=case["data_sensitivity"],
            height=90
        )
        business_value = st.text_area(
            "Business_value",
            value=case["business_value"],
            height=90
        )
    success_metric = st.text_area(
        "Success_metric",
        value=case["success_metric"],
        height=90
    )
    submitted = st.form_submit_button("Evaluate AI feature")

# -----------------------------
# Placeholder result card
# -----------------------------
if submitted:
    st.divider()
    st.header("2.Evaluation results")
    st.info("This is a placeholder result card. The LLM-generated assessment will replace this output later.")        

    # Placeholder scores
    ai_fit = 72
    commercial_upside = 78
    risk_burden = 68
    evidence_readiness = 55

    risk_adjustment = 100-risk_burden
    build_readiness = (
        ai_fit * 0.3 +
        commercial_upside * 0.25 +
        evidence_readiness * 0.25 +
        risk_adjustment * 0.2       
    )

    def get_decision_band(score):
        if score >= 80:
            return "Yes - Build/advance"
        elif score >=65:
            return "Yes, but prototype first"
        elif score >=50:
            return "Maybe - narrow scope"
        elif score >=35:
            return "Not yet - rework"
        else:
            return "No - avoid/rethink"
        
    decision_band = get_decision_band(build_readiness)

    st.subheader("Recommendation")
    st.markdown("**Prototype, but narrow scope.**")

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Build Readiness", f"{build_readiness:.0f}/100")
    col2.metric("AI Fit", f"{ai_fit}/100")
    col3.metric("Commercial Upside", f"{commercial_upside}/100")
    col4.metric("Risk Burden", f"{risk_burden}/100")
    col5.metric("Evidence Readiness", f"{evidence_readiness}/100")

    st.markdown(f"**Decision band:** {decision_band}")

    st.subheader("Core Tension")
    st.write(
        "AI can create meaningful product value, but the current framing may introduce risks that require tighter scope and validation."
    )

    st.subheader("What to build")
    st.markdown(
        """
        - Safer, narrower version of this feature
        - Human review checkpoints
        - Clear user controls
        - Validation plan before launch

        """
    )

    st.subheader("What not to build")
    st.markdown(
        """
        - Overconfident AI recommendations
        - Features that replace human judgement
        - High risk automation without evidence or validation
        """
    )

    st.subheader("Next validation step")
    st.write(
        "Test whether users understand the feature output correctly and whether the team can validate the key assumptions before build."
    )

