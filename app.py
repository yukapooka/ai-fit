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

#generate sample_outputs dictionary for the 3 test cases:
sample_outputs = {
    "AI Digital Twin for User Research Personas": {
        "recommendation":"Prototype, but narrow scope.",
        "core_tension":"AI can speed up research synthesis and product discovery, but may create synthetic evidence that teams mistake for real user validation.",
        "ai_fit":72,
        "commercial_upside":78,
        "risk_burden":68,
        "evidence_readiness":55,
        "confidence":"Medium",
        "score_drivers":{
            "ai_fit":"Strong use case for synthesizing messy qualitative research and surfacing assumptions.",
            "commercial":"Could reduce discovery time, improve PM/researcher productivity, and differentiate research tooling.",
            "risk":"High risk of false validation if synthetic persona responses are treated as real user evidence.",
            "evidence":"Validation is possible, but requires comparison against real user feedback and researcher judgment."
        },
        "useful_kernel":"Use AI to synthesize existing research, surface assumptions, identify missing user segments, and generate better research questions.",
        "commercial_value":"Could reduce discovery time, improve PM/researcher productivity, and differentiate research tooling.",
        "risky_framing":"Positioning AI personas as “digital users” that can answer on behalf of real people.",
        "what_to_build":[
            "Research synthesis from existing user data",
            "Assumption mapping",
            "Interview question generation",
            "Missing segment/ weak evidence flags",
            "Comparison between AI-genrated hypotheses and real user feedback"
        ],
        "what_not_to_build":[
            "Synthetic user quotes presented as evidence",
            "Persona chatbots answering as the user",
            "Product-market-fit scoring based on simulated responses",
            "Roadmap recommendations from simulated feedback",
            "Synthetic data generation that replaces actual user research"
        ],
        "human_checkpoint":"User researchers should review whether the AI output accurately reflects source research, whether minority or edge-case users are flattened, and whether PMs are using the output as hypothesis support rather than validation.",
        "next_validation_step":"Create two comparison groups: real users and AI-generated personas derived from prior research. Present both with the same new feature concept, then assess where responses converge or diverge. Use the results to determine whether AI personas are useful for hypothesis generation, not as standalone evidence of user demand.",
    },
    "AI Grief Companion": {
        "recommendation":"Prototype only as guided reflection support, with strong user controls and expert-reviewed boundaries.",
        "core_tension":"AI may offer comfort and structure during difficult moments, but may also simulate intimacy, deepen dependency, or cross into therapy-adjacent support.",
        "ai_fit":74,
        "commercial_upside":65,
        "risk_burden":88,
        "evidence_readiness":48,
        "confidence":"Medium-Low",
        "score_drivers":{
            "ai_fit":"AI can personalize tone, timing, and reflective prompts, but simpler reminders or journaling tools may solve part of the need.",
            "commercial":"Could support retention and emotional engagement, but monetization is ethically sensitive.",
            "risk":"High emotional vulnerability, dependency risk, crisis escalation risk, and unsafe support-boundary concerns.",
            "evidence":"Expert review is possible, but long-term emotional safety and dependency risk are difficult to validate."
        },
        "useful_kernel":"Use AI to offer gentle, user-controlled reflection prompts and supportive messages during difficult dates or moments.",
        "commercial_value":"A differentiated emotional wellbeing experience, higher user trust through sensitive design, and potential retention through opt-in reflective rituals rather than addictive engagement loops.",
        "risky_framing":"An AI companion that substitutes for a deceased person, simulates intimacy, or keeps users in a memory bubble instead of supporting healthy processing.",
        "what_to_build":[
            "Research synthesis from existing user data",
            "User-selected tone and message type",
            "Gentle journaling or reflection prompts",
            "Clear boundaries: This is not therapy or crisis support",
            "Easy pause, mute, unsubscribe, or reset controls",
            "Escalation guidance when users express severe distress"
        ],
        "what_not_to_build":[
            "AI that imitates or speaks as the deceased person",
            "Always-on emotional companion behavior",
            "Therapeutic advice or diagnosis",
            "Features that encourage prolonged dependency",
            "Memory loops that repeatedly resurface painful content without user control",
            "Monetization based on emotional vulnerability or increased dependency"
        ],
        "human_checkpoint":"Psychologists, grief counselors, or mental health professionals should review message templates, escalation logic, unsafe response patterns, and the boundary between reflection support and therapy-adjacent care.",
        "next_validation_step":"Run a small expert review and user comfort study. First, have mental health professionals classify sample outputs as safe, borderline, or unsafe. Then have target users assess whether the messages feel supportive, intrusive, overly intimate, or emotionally destabilizing.",
    },
    "AI Financial Personality Profiler": {
        "recommendation":"Narrow scope before prototype.",
        "core_tension":"AI may support financial reflection and personalization, but could become reductive, shame-inducing, or manipulative if used to label users or steer financial behavior.",
        "ai_fit":64,
        "commercial_upside":82,
        "risk_burden":80,
        "evidence_readiness":58,
        "confidence":"Low-Medium",
        "score_drivers":{
            "ai_fit":"AI can personalize reflection, spending insights, and financial education, but many tracking and budgeting functions can be rule-based.",
            "commercial":"High potential for engagement, retention, differentiated education journeys, and monetizable financial product pathways.",
            "risk":"High risk of behavioral influence, financial vulnerability, shame-inducing labels, and incentive misalignment.",
            "evidence":"Small-cohort testing is possible, but must test emotional safety, comprehension, pressure, bias, and conflicts of interest."
        },
        "useful_kernel":"Use AI to help users reflect on spending patterns, understand trade-offs, build financial confidence, and choose user-defined goals without assigning fixed identity labels.",
        "commercial_value":"Personalized goal journeys, habit-building loops, and educational pathways that increase retention without pushing unsuitable products.",
        "risky_framing":"Labeling users as “impulse spenders,” “risk-takers,” or “financially anxious,” then using those labels to steer them toward monetized financial products.",
        "what_to_build":[
            "User-controlled spending pattern summaries",
            "Editable insights rather than fixed personality labels",
            "Goal-based education journeys",
            "Reflection prompts around values, trade-offs, and financial confidence",
            "Transparent explanations of why a pattern was surfaced",
            "Clear separation between education and product recommendations"
        ],
        "what_not_to_build":[
            "Fixed financial personality labels based on spending data",
            "Shame-based nudges or moralizing language",
            "Product recommendations presented as best for your profile",
            "Partner-driven nudges that benefit the business more than the user",
            "Automated financial advice without qualified review or clear disclaimers",
            "Dark-pattern engagement loops based on anxiety or insecurity"
        ],
        "human_checkpoint":"Target users should review whether the interface feels supportive, non-judgmental, and understandable. Finance experts should review educational content for accuracy, while product, legal, and compliance reviewers should assess whether recommendations cross into regulated advice or conflicted selling.",
        "next_validation_step":"Compare two prototypes: one with fixed personality labels and one with editable, user-controlled pattern summaries. Measure user comprehension, perceived support, shame or pressure, trust, and intent to continue using the feature.",
    }
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
# Output results
# -----------------------------
if submitted:
    st.divider()
    st.header("2.Evaluation results")
    
    # Handle blank case first:
    if selected_case == "Start from blank":
        st.warning("Custom LLM-generated results will be added in the next version. For now, choose one of the sample cases.")
    else:
        #Pull the selected sample result:
        result = sample_outputs[selected_case]

        result = sample_outputs[selected_case]

        ai_fit = result["ai_fit"]
        commercial_upside = result["commercial_upside"]
        risk_burden = result["risk_burden"]
        evidence_readiness = result["evidence_readiness"]

        #calculate build readiness score:
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

        # ------------------------------
        # One-page result card
        # ------------------------------
        st.subheader("Recommendation")
        st.markdown(f"**{result['recommendation']}**")

        st.markdown(f"**Decision band:** {decision_band}")

        #Score snapshot
        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric("Build Readiness", f"{build_readiness:.0f}/100",
                    help="Overall readiness to move forward, balancing AI fit, business value, evidence readiness, and risk burden.")
        col2.metric("AI Fit", f"{ai_fit}/100",
                    help="Does AI add meaningful value beyond a simpler solution?")
        col3.metric("Commercial Upside", f"{commercial_upside}/100",
                    help="Does this feature create meaningful business value through adoption, retention, revenue, differentiation, or efficiency?")
        col4.metric("Risk Burden", f"{risk_burden}/100",
                    help="How much harm, sensitivity, or governance effort does this introduce?")
        col5.metric("Evidence Readiness", f"{evidence_readiness}/100",
                    help="Can the team test this responsibly before launch?")

        st.markdown(f"**Confidence:** {result['confidence']}")

        st.divider()

        # Core tension
        st.subheader("Core tension")
        st.write(result["core_tension"])

        # Score drivers
        st.subheader("Score drivers")
        #st.write(result["score_drivers"])

        score_drivers = result["score_drivers"]
        st.markdown(f"**AI Fit:** {score_drivers['ai_fit']}")
        st.markdown(f"**Commercial:** {score_drivers['commercial']}")
        st.markdown(f"**Risk:** {score_drivers['risk']}")
        st.markdown(f"**Evidence:** {score_drivers['evidence']}")

        # Useful kernel / commercial value / risky framing
        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.subheader("Useful kerenel")
            st.write(result["useful_kernel"])

        with col_b:
            st.subheader("Commercial value")
            st.write(result["commercial_value"])

        with col_c:
            st.subheader("Risky framing to avoid")
            st.write(result["risky_framing"])
        
        # What to build / not build
        col_build, col_not_build = st.columns(2)

        with col_build:
            st.subheader("What to build")
            for item in result["what_to_build"]:
                st.markdown(f"- {item}")
            
            with col_not_build:
                st.subheader("What not to build")
                for item in result["what_not_to_build"]:
                    st.markdown(f"- {item}")
        
        # Human checkpoint
        st.subheader("Human checkpoint")
        st.write(result["human_checkpoint"])

        # Next validation step
        st.subheader("Next validation step")
        st.write(result["next_validation_step"])

