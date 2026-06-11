import streamlit as st
import json
import requests

# ------------------------------
# Page configuration
# ------------------------------
st.set_page_config(
    page_title="AIFit",
    page_icon="🚀",
    layout="wide"
)

st.markdown(
    """
    <style>

    /* Widget labels */
    .stTextArea label,
    .stTextInput label,
    .stSelectbox label,
    .stRadio label,
    .stCheckbox label {
        font-size: 1.2rem !important;
        font-weight: 600 !important;
    }

    /* Text entered into text areas */
    textarea {
        font-size: 1.05rem !important;
        line-height: 1.5 !important;
    }

    /* Selectbox text */
    div[data-baseweb="select"] {
        font-size: 1.05rem !important;
    }

    /* Section headers */
    h2, h3 {
        font-size: 1.2rem !important;
    }
    
    .stMarkdown p {
        font-size: 1.15rem;
        line-height: 1.6;

    }

    .stMarkdown li {
        font-size: 1.15rem;
        line-height: 1.6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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
        "risk_type": "False validation",
        "risk_themes": [
            "synthetic evidence",
            "unsupported claims",
            "overconfidence",
            "reduced real user research",
        ],
        "risk_rationale": "AIFit classifies this as False validation because product teams may treat AI-generated persona responses as evidence of user demand even when those responses are synthetic or weakly supported by source research.",
        "ai_fit":72,
        "commercial_upside":78,
        "risk_burden":68,
        "evidence_readiness":55,
        "confidence":"Medium",
        "score_drivers":{
            "ai_fit_driver":"Strong use case for synthesizing messy qualitative research and surfacing assumptions.",
            "commercial_driver":"Could reduce discovery time, improve PM/researcher productivity, and differentiate research tooling.",
            "risk_driver":"High risk of false validation if synthetic persona responses are treated as real user evidence.",
            "evidence_driver":"Validation is possible, but requires comparison against real user feedback and researcher judgment."
        },
        "useful_kernel":"Use AI to synthesize existing research, surface assumptions, identify missing user segments, and generate better research questions.",
        "commercial_value":"Could reduce discovery time, improve PM/researcher productivity, and differentiate research tooling.",
        "risky_framing":"Positioning AI personas as “digital users” that can answer on behalf of real people.",
        "what_to_build":[
            "Research synthesis from existing user data",
            "Assumption mapping",
            "Interview question generation",
            "Missing segment/ weak evidence flags",
            "Comparison between AI-generated hypotheses and real user feedback"
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
        "risk_type": "Emotional vulnerability",
        "risk_themes": [
            "emotional dependency",
            "false intimacy",
            "distress escalation",
            "user autonomy",
        ],
        "risk_rationale": "AIFit classifies this as Emotional vulnerability because users may rely on the AI for support during grief or distress, creating risks of dependency, unsafe boundaries, or missed escalation to human help.",
        "ai_fit":74,
        "commercial_upside":65,
        "risk_burden":88,
        "evidence_readiness":48,
        "confidence":"Medium-Low",
        "score_drivers":{
            "ai_fit_driver":"AI can personalize tone, timing, and reflective prompts, but simpler reminders or journaling tools may solve part of the need.",
            "commercial_driver":"Could support retention and emotional engagement, but monetization is ethically sensitive.",
            "risk_driver":"High emotional vulnerability, dependency risk, crisis escalation risk, and unsafe support-boundary concerns.",
            "evidence_driver":"Expert review is possible, but long-term emotional safety and dependency risk are difficult to validate."
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
                "risk_type": "Financial manipulation",
        "risk_themes": [
            "identity labeling",
            "shame or coercion",
            "incentive misalignment",
            "financial vulnerability",
        ],
        "risk_rationale": "AIFit classifies this as Financial manipulation because users may treat inferred spending profiles as fixed identity labels and may be nudged toward financial behaviors or products that do not serve their interests.",
        "ai_fit":64,
        "commercial_upside":82,
        "risk_burden":80,
        "evidence_readiness":58,
        "confidence":"Low-Medium",
        "score_drivers":{
            "ai_fit_driver":"AI can personalize reflection, spending insights, and financial education, but many tracking and budgeting functions can be rule-based.",
            "commercial_driver":"High potential for engagement, retention, differentiated education journeys, and monetizable financial product pathways.",
            "risk_driver":"High risk of behavioral influence, financial vulnerability, shame-inducing labels, and incentive misalignment.",
            "evidence_driver":"Small-cohort testing is possible, but must test emotional safety, comprehension, pressure, bias, and conflicts of interest."
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

# -----------------------------
# LLM prompt and schema
# -----------------------------

# Define schema of json output:
AIFIT_JSON_SCHEMA = {
    "recommendation": "string",
    "core_tension": "string",
    "risk_type": "string",
    "risk_themes": ["string"],
    "risk_rationale":"string",
    "ai_fit": 0,
    "commercial_upside": 0,
    "risk_burden": 0,
    "evidence_readiness": 0,
    "confidence": "Low | Low-Medium | Medium | Medium-High | High",
    "ai_fit_driver": "string",
    "commercial_driver": "string",
    "risk_driver": "string",
    "evidence_driver": "string",
    "useful_kernel": "string",
    "commercial_value": "string",
    "risky_framing": "string",
    "what_to_build": ["string"],
    "what_not_to_build": ["string"],
    "human_checkpoint":"string",
    "human_reviewer": "string", #split up human checkpoint to granular levels
    "review_package": ["string"],
    "review_scope": "string",
    "review_timing": "string",
    "review_action": "string",
    "next_validation_step": "string",
    "validation_method": "string",
    "validation_coverage": "string",
    "validation_metrics": ["string"],
    "success_threshold": "string",
    "failure_trigger": "string",
}

RISK_TYPE_GUIDANCE = {
    "Emotional vulnerability": {
        "key_questions": [
            "Could users become emotionally dependent on the AI?",
            "Could users mistake the AI for human or therapeutic support?",
            "Are distress signals handled safely?",
            "Do users have clear pause, opt-out, and escalation controls?",
        ],
        "validation_focus": [
            "emotional support without increased dependency",
            "expert review of tone and boundary safety",
            "safe handling of distress signals",
            "user control over timing, frequency, and opt-out",
            "avoidance of overly intimate or substitutive messaging",
        ],
        "move_forward_guidance": (
            "Move forward only if users feel supported without increased dependency, "
            "reviewers approve message tone and boundaries, opt-out controls work reliably, "
            "and distress escalation pathways are safe."
        ),
        "stop_signal_guidance": (
            "Stop or redesign if users treat the AI as a substitute for human support, "
            "messages increase distress or dependency, opt-out controls fail, or high-risk distress is not escalated safely."
        ),
    },
    "False validation": {
        "key_questions": [
            "Can AI-generated claims, summaries, or recommendations be traced back to reliable source evidence?",
            "Could users mistake AI-generated output for verified truth, official guidance, or real-world validation?",
            "Does the feature reduce appropriate human verification or evidence gathering?",
            "Are uncertainty, source quality, and confidence clearly communicated?",
        ],
        "validation_focus": [
            "evidence alignment between AI output and source material",
            "unsupported, outdated, or hallucinated claims",
            "user understanding of the AI output as advisory rather than authoritative",
            "continued use of appropriate human verification or real-world evidence",
            "reviewer confidence in traceability, source quality, and uncertainty communication",
        ],
        "move_forward_guidance": (
            "Move forward only if outputs are traceable to reliable source evidence, users understand the limits of AI-generated guidance, "
            "unsupported claims are clearly flagged, and appropriate human verification remains available."
        ),
        "stop_signal_guidance": (
            "Stop or redesign if users treat AI outputs as authoritative evidence, unsupported or outdated claims recur, "
            "confidence signals obscure uncertainty, or human verification pathways are bypassed."
        ),
    },
    "Fairness / bias": {
        "key_questions": [
            "Does the AI treat relevant user subgroups differently?",
            "Could the feature penalize valid non-standard behavior or communication styles?",
            "Are scoring rubrics fair across contexts?",
        ],
        "validation_focus": [
            "expert agreement across relevant subgroups",
            "subgroup differences in tone, severity, or recommendations",
            "user-perceived fairness",
            "harmful or identity-shaping feedback",
            "edge cases and borderline examples",
        ],
        "move_forward_guidance": (
            "Move forward only if expert reviewers find the output fair across relevant subgroups, "
            "users do not feel pressured to conform to a narrow norm, and no material disparity appears in tone or scoring severity."
        ),
        "stop_signal_guidance": (
            "Stop or redesign if outputs repeatedly penalize valid non-standard communication, create subgroup disparities, "
            "or pressure users to change identity-linked behavior."
        ),
    },
    "Privacy / sensitive data": {
        "key_questions": [
            "What sensitive data is collected, stored, or exposed?",
            "Can outputs leak private information?",
            "Are consent, retention, deletion, and access controls clear?",
        ],
        "validation_focus": [
            "data minimization",
            "redaction quality",
            "retention and deletion behavior",
            "access control failures",
            "user understanding of consent and data use",
        ],
        "move_forward_guidance": (
            "Move forward only if sensitive inputs are minimized, redacted where appropriate, stored securely, "
            "deleted as promised, and users clearly understand consent and data use."
        ),
        "stop_signal_guidance": (
            "Stop or redesign if raw sensitive data is exposed, consent is unclear, deletion fails, access controls fail, "
            "or private information leaks into outputs."
        ),
    },
    "General AI product risk": {
        "key_questions": [
            "Does AI add value beyond simpler alternatives?",
            "What user or business decision could be distorted?",
            "What evidence is needed before launch?",
        ],
        "validation_focus": [
            "user value",
            "output quality",
            "human review",
            "user understanding",
            "risk mitigation",
        ],
        "move_forward_guidance": (
            "Move forward only if the feature shows clear user value, reliable output quality, and manageable risk with human oversight."
        ),
        "stop_signal_guidance": (
            "Stop or redesign if outputs are unreliable, users misunderstand the AI role, or risks cannot be mitigated through product safeguards."
        ),
    },
   "Financial manipulation": {
        "key_questions": [
            "Could the feature pressure users toward financial behaviors that benefit the business more than the user?",
            "Could users feel shamed, judged, or reduced to a financial identity label?",
            "Could inferred profiles steer users toward unsuitable products or decisions?",
            "Are users able to understand, edit, reject, or delete the profile?"
        ],
        "validation_focus": [
            "user understanding of profile meaning and limitations",
            "emotional impact of labels and nudges",
            "pressure or coercion in financial recommendations",
            "fairness across income, age, and financial vulnerability groups",
            "separation between education and monetized product recommendations"
        ],
        "move_forward_guidance": (
            "Move forward only if users understand the profile as an editable reflection rather than a fixed identity, "
            "nudges are perceived as supportive rather than shaming or coercive, and financial recommendations are clearly separated from education."
        ),
        "stop_signal_guidance": (
            "Stop or redesign if users feel judged, shamed, pressured toward financial products, or if inferred profiles create unfair treatment "
            "across income, age, or financial vulnerability groups."
        ),
    },
}

def format_risk_guidance_for_prompt():
    sections = []

    for risk_type, guidance in RISK_TYPE_GUIDANCE.items():
        section = f"""
Risk type: {risk_type}

Key questions:
{chr(10).join([f"- {item}" for item in guidance["key_questions"]])}

Validation focus:
{chr(10).join([f"- {item}" for item in guidance["validation_focus"]])}

Move-forward guidance:
{guidance["move_forward_guidance"]}

Stop/redesign guidance:
{guidance["stop_signal_guidance"]}
"""
        sections.append(section)

    return "\n".join(sections)

# Define a prompt builder function:
def build_aifit_prompt(user_inputs):
    return f"""
You are an experienced AI product manager specializing in responsible AI product launches.

Evaluate the proposed AI feature using the AIFit framework.

Return one valid JSON object only.
Do not include markdown, commentary, code fences, or text before/after the JSON.
Use the exact top-level keys in the schema.
Do not rename keys.
Do not leave fields blank.
Do not write "Not provided."

The JSON object must follow this schema:
{json.dumps(AIFIT_JSON_SCHEMA, indent=2)}

Evaluation dimensions:
- AI Fit: Does AI add meaningful value beyond a simpler non-AI solution?
- Commercial Upside: Could this create adoption, retention, revenue, differentiation, or efficiency?
- Risk Burden: What user, product, governance, or failure risk does this introduce?
- Evidence Readiness: Can the team test this responsibly before launch?

Scoring rules:
- ai_fit, commercial_upside, risk_burden, and evidence_readiness must be integers from 0 to 100.
- Do not include "/100", labels, or words in score fields.
- Driver fields must contain explanation only, with no numeric score.

Risk type:
Choose the dominant risk_type from the risk-specific guidance below.
Choose the risk that most directly affects user judgment, autonomy, safety, or harm.
Do not select "Privacy / sensitive data" merely because sensitive data is used. Select it only when data exposure, consent, retention, deletion, or access control is the dominant risk.
For financial profiling, spending insights, nudges, or personalized money advice, prefer "Financial manipulation" when the main concern is shame, coercion, identity labeling, incentive misalignment, or steering users toward unsuitable financial behavior.
For knowledge assistants, copilots, onboarding tools, internal policy assistants, and information retrieval systems, prefer "False validation" when the primary risk is users acting on incorrect, outdated, unsupported, or overconfident AI guidance.

Core output guidance:
- core_tension: One sentence in the form "AI may [create value], but may also [create risk]."
- useful_kernel: What part of the idea is worth preserving?
- commercial_value: What business value is worth preserving without increasing risk?
- risky_framing: What product framing should the team avoid?
- what_to_build: 3 to 6 concrete product-scope items.
- what_not_to_build: 3 to 6 concrete product boundaries or anti-patterns.

Human review workflow:
Fill each field separately.
- human_reviewer: Who should review the AI output? Be specific to the dominant risk type.
- review_package: 4 to 6 concrete artifacts the reviewer should inspect. Include source material, generated output, scoring logic, edge cases, subgroup comparisons, or user-facing wording where relevant.
- review_scope: What variation, subgroup, edge case, or risk pattern should the reviewer check?
- review_timing: When should review happen?
- review_action: What can the reviewer do? For example: approve, revise, request safeguards, escalate, or block release.

Validation workflow:
Fill each field separately.
- validation_method: What concrete test should the product team run next?
- validation_coverage: What users, scenarios, edge cases, inputs, and outputs must be represented? Do not specify exact sample sizes unless provided by the user.
- validation_metrics: 4 to 6 metrics that match the dominant risk_type. Do not reuse generic metrics from another risk type.
- move_forward_criteria: Qualitative evidence that would justify moving forward. Do not invent numeric thresholds.
- stop_or_redesign_signal: Evidence that should cause the team to narrow, redesign, pause, or stop the feature.

Avoid unsupported precision:
Do not invent sample sizes, percentages, Likert targets, or numeric cutoffs unless the user explicitly provides them.
Use qualitative phrases such as "strong expert agreement", "material disparity", "no recurring harmful pattern", "users understand the AI output as advisory", or "team-defined acceptable range."

Risk-specific guidance:
{format_risk_guidance_for_prompt()}
Use the risk-specific guidance to adapt the review workflow, validation metrics, move-forward criteria, and stop/redesign signal.
Do not copy the guidance word-for-word unless it directly fits the feature.
Adapt it to the actual product idea.

risk_themes:
Return 2 to 5 specific risk themes that explain the dominant risk in this case.
These should add nuance beyond the broad risk_type.
Examples of risk themes:
- high-stakes decision support
- delayed care
- false reassurance
- escalation failure
- over-reliance
- identity labeling
- data leakage
- incentive conflict
- emotional dependency
- evidence misuse
- outdated guidance
- user autonomy

risk_rationale:
Explain in one or two sentences why this risk_type and these risk_themes were selected.
Tie the rationale to the specific feature, user decision influenced, and impact if wrong.
Do not give a generic explanation.

Feature information:
Feature idea: {user_inputs["feature_idea"]}
Target user: {user_inputs["target_user"]}
User problem: {user_inputs["user_problem"]}
Proposed AI capability: {user_inputs["ai_capability"]}
Current non-AI alternative: {user_inputs["non_ai_alternative"]}
Human decision influenced: {user_inputs["human_decision"]}
Impact if wrong: {user_inputs["impact_if_wrong"]}
Data sensitivity: {user_inputs["data_sensitivity"]}
Business value: {user_inputs["business_value"]}
Success metric: {user_inputs["success_metric"]}

"""

# extract only the JSON object before parsing, avoid extra text:
def extract_json_object(text):
    """
    Extract the first JSON object from model output.
    Handles cases where the model adds text before or after the JSON.
    """
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("No valid JSON object found in model output.")
    json_text = text[start:end + 1]
    return json.loads(json_text)

def generate_llm_result(user_inputs):
    api_key = st.secrets["OPENROUTER_API_KEY"]
    prompt = build_aifit_prompt(user_inputs)
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "AIFit",
        },
        json={
            "model": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "temperature": 0.2,
        },
        timeout=60,
    )
    if response.status_code != 200:
        st.error("OpenRouter request failed")
        st.write("Status code:", response.status_code)
        st.write("Response body:", response.text)
        response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    content = content.strip()
    if content.startswith("```json"):
        content = content.replace("```json", "").replace("```", "").strip()
    elif content.startswith("```"):
        content = content.replace("```", "").strip()
    return extract_json_object(content)

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
# Input form
# ------------------------------
st.header("1. Describe the AI feature")

with st.form("feature_form"):
    st.markdown("### Product idea")

    feature_idea = st.text_area(
        "Feature idea*",
        value=case["feature_idea"],
        height=90,
        placeholder="Describe the AI feature you want to evaluate."
    )

    ai_capability = st.text_area(
        "Proposed AI capability*",
        value=case["ai_capability"],
        height=80,
        placeholder="What will the AI actually do?"
    )

    non_ai_alternative = st.text_area(
        "Current non-AI alternative",
        value=case["non_ai_alternative"],
        height=70,
        placeholder="How is this problem solved today without AI?"
    )

    st.markdown("### User and problem")

    col1, col2 = st.columns(2)

    with col1:
        target_user = st.text_area(
            "Target user*",
            value=case["target_user"],
            height=70,
            placeholder="Who is this for?"
        )

    with col2:
        user_problem = st.text_area(
            "User problem*",
            value=case["user_problem"],
            height=70,
            placeholder="What problem is this meant to solve?"
        )

    st.markdown("### Business value")

    col3, col4 = st.columns(2)

    with col3:
        business_value = st.text_area(
            "Business value*",
            value=case["business_value"],
            height=70,
            placeholder="What business value are you hoping to create? Reduce support workload, improve conversion, increase retention, improve efficiency..."
        )

    with col4:
        success_metric = st.text_area(
            "Success metric",
            value=case["success_metric"],
            height=70,
            placeholder="What would success look like?"
        )

    st.markdown("### Risk and failure mode")

    impact_if_wrong = st.text_area(
        "Impact if wrong *",
        value=case["impact_if_wrong"],
        height=80,
        placeholder="Describe the most important failure mode if the AI is incorrect."
    )

    with st.expander("Advanced context"):
        human_decision = st.text_area(
            "Human decision influenced",
            value=case["human_decision"],
            height=70,
            placeholder="What human decision will this AI output influence?"
        )

        data_sensitivity = st.text_area(
            "Data sensitivity",
            value=case["data_sensitivity"],
            height=70,
            placeholder="Does it involve personal, financial, health, workplace, emotional, or confidential data?"
        )
    submitted = st.form_submit_button("Evaluate AI feature")

# -----------------------------
# Output results
# -----------------------------
def parse_score(value):
    """
    Convert LLM score outputs into integers.
    Handles values like 72, "72", "72/100", or "AI Fit: 72".
    """
    if isinstance(value, int) or isinstance(value, float):
        return int(value)

    if isinstance(value, str):
        digits = "".join([char for char in value if char.isdigit()])
        if digits:
            return int(digits[:3]) if int(digits[:3]) <= 100 else 100

    return 0

# normalization step after LLM returns result - useful when the model misses or renames fields:
def normalize_llm_result(result):
    """
    Ensure the LLM result has all required keys.
    Handles both old nested score_drivers format and new flattened driver fields.
    """
    # If model returns the old nested score_drivers format, map it to flat fields.
    score_drivers = result.get("score_drivers", {})

    if isinstance(score_drivers, dict):
        result["ai_fit_driver"] = score_drivers.get(
            "ai_fit",
            result.get("ai_fit_driver", "")
        )
        result["commercial_driver"] = score_drivers.get(
            "commercial",
            result.get("commercial_driver", "")
        )
        result["risk_driver"] = score_drivers.get(
            "risk",
            result.get("risk_driver", "")
        )
        result["evidence_driver"] = score_drivers.get(
            "evidence",
            result.get("evidence_driver", "")
        )

    if "review_package" not in result or result["review_package"] in ["", None]:
        result["review_package"] = [
            "Representative AI-generated outputs",
            "Source inputs used to generate those outputs",
            "Scoring or evaluation criteria",
            "Low-confidence or borderline examples",
            "User-facing wording or recommendations",
        ]
    elif isinstance(result["review_package"], str):
        result["review_package"] = [result["review_package"]]
    elif not isinstance(result["review_package"], list):
        result["review_package"] = [
            "Representative AI-generated outputs",
            "Source inputs used to generate those outputs",
            "Scoring or evaluation criteria",
            "Low-confidence or borderline examples",
            "User-facing wording or recommendations",
        ]

    defaults = {
        "recommendation": "",
        "core_tension": "AI may create product value, but the current framing needs further review for user risk, evidence quality, and human oversight.",
        "risk_type": "General AI product risk",
        "risk_themes": ["General AI product risk"],
        "risk_rationale": "AIFit selected this risk classification based on the likely user decision influenced by the AI output and the potential impact if the AI is wrong.",
        "ai_fit": 0,
        "commercial_upside": 0,
        "risk_burden": 0,
        "evidence_readiness": 0,
        "confidence": "",
        "ai_fit_driver": "AI fit requires review because the model did not explain whether AI adds value beyond simpler alternatives.",
        "commercial_driver": "Commercial upside requires review because the model did not explain business value clearly.",
        "risk_driver": "Risk burden requires review because the model did not identify the main failure mode clearly.",
        "evidence_driver": "Evidence readiness requires review because the model did not specify how this feature should be tested.",
        "useful_kernel": "Use AI to support human review by summarizing information, surfacing patterns, and helping teams make better-informed decisions.",
        "commercial_value": "Preserve efficiency, differentiation, and faster decision-making without removing human accountability.",
        "risky_framing": "An AI system that replaces human judgment or presents its recommendations as final decisions.",
        "human_reviewer": "A responsible human reviewer.",
        "review_package": [
            "Representative AI-generated outputs",
            "Source inputs used to generate those outputs",
            "Scoring or evaluation criteria",
            "Low-confidence or borderline examples",
            "User-facing wording or recommendations"
        ],
        "review_scope": "Review whether the AI output is accurate, fair, safe, and appropriate for the intended user context.",
        "review_timing": "Before pilot launch and again after reviewing early pilot outputs.",
        "review_action": "Reviewers can approve, request revisions, require safeguards, escalate concerns, or block release.",
        "what_to_build": ["Not provided."],
        "what_not_to_build": ["Not provided."],
        "next_validation_step": "Run a focused validation test using representative inputs, human review, and risk-specific success criteria.",
        "validation_method": "Run a focused pilot to test whether the feature creates product value without introducing unacceptable risk.",
        "validation_coverage": "Representative user inputs, AI-generated outputs, edge cases, and human-reviewed examples.",
        "validation_metrics": [
            "Output accuracy",
            "User comprehension",
            "Human reviewer agreement",
            "Risk incident rate",
            "User trust or perceived usefulness"
        ],
        "move_forward_criteria": "Move forward only if the validation evidence shows the feature creates user value while keeping the dominant risk within a team-defined acceptable range.",
        "stop_or_redesign_signal": "Narrow or redesign if validation reveals that the dominant risk appears repeatedly, affects vulnerable users, or cannot be mitigated through product safeguards.",
    }

    # Fill missing or empty top-level keys.
    for key, default_value in defaults.items():
        if key not in result or result[key] in ["", None]:
            result[key] = default_value

    # Ensure list fields are lists.
    for key in [
        "what_to_build",
        "what_not_to_build",
        "review_package",
        "validation_metrics",
        "risk_themes",
    ]:
        if isinstance(result[key], str):
            result[key] = [result[key]]
        elif not isinstance(result[key], list):
            result[key] = ["Not provided."]
    return result

def apply_risk_specific_validation_fallbacks(result):
    """
    Safety net only.
    The prompt should generate risk-specific validation content.
    This function only replaces obviously generic fallback text.
    """
    risk_type = result.get("risk_type", "General AI product risk")
    guidance = RISK_TYPE_GUIDANCE.get(
        risk_type,
        RISK_TYPE_GUIDANCE["General AI product risk"]
    )

    generic_move_forward_phrases = [
        "Move forward only if the validation evidence shows",
        "Move forward if reviewers find the AI output useful",
        "Proceed if the feature demonstrates clear user value",
        "useful, accurate, and appropriate",
        "dominant risk within a team-defined acceptable range",
    ]

    generic_stop_phrases = [
        "Narrow or redesign if validation reveals",
        "Redesign if reviewers identify recurring inaccuracies",
        "The feature should be narrowed or redesigned if outputs are inaccurate",
        "risk patterns that cannot be addressed with safeguards",
    ]

    if (
        not result.get("move_forward_criteria")
        or any(phrase in result["move_forward_criteria"] for phrase in generic_move_forward_phrases)
    ):
        result["move_forward_criteria"] = guidance["move_forward_guidance"]

    if (
        not result.get("stop_or_redesign_signal")
        or any(phrase in result["stop_or_redesign_signal"] for phrase in generic_stop_phrases)
    ):
        result["stop_or_redesign_signal"] = guidance["stop_signal_guidance"]

    return result

if submitted:
    st.divider()
    st.header("2.Evaluation results")
    
    user_inputs={
        "feature_idea": feature_idea,
        "target_user": target_user,
        "user_problem": user_problem,
        "ai_capability": ai_capability,
        "non_ai_alternative": non_ai_alternative,
        "human_decision": human_decision,
        "impact_if_wrong": impact_if_wrong,
        "data_sensitivity": data_sensitivity,
        "business_value": business_value,
        "success_metric": success_metric,
    }

    # Validate mandatory and optional input fields:
    required_fields = {
        "Feature idea": feature_idea,
        "Target user": target_user,
        "User problem": user_problem,
        "Proposed AI capability": ai_capability,
        "Impact if wrong": impact_if_wrong,
        "Business value": business_value,
    }
    missing_fields = [
        name for name, value in required_fields.items() 
        if not value or not value.strip()
    ]
    if missing_fields:
        st.warning(f"Please complete the required fields: {', '.join(missing_fields)}")
        st.stop()

    # Handle blank case first:
    if selected_case == "Start from blank":
        with st.spinner("Generating AIFit assessment..."):
            try:
                result = generate_llm_result(user_inputs)
                st.success("LLM result received.")
                #st.write("Raw result:", result)
            except Exception as e:
                st.error(f"Could not generate LLM result: {e}")
                st.stop()
    else:
        result = sample_outputs[selected_case]
    
    # Call normalizer
    result = normalize_llm_result(result)
    result = apply_risk_specific_validation_fallbacks(result)

    ai_fit = parse_score(result["ai_fit"])
    commercial_upside = parse_score(result["commercial_upside"])
    risk_burden = parse_score(result["risk_burden"])
    evidence_readiness = parse_score(result["evidence_readiness"])

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

    # add recommendation fallback after build readiness is computed:
    weak_recommendations = [
    "",
    None,
    "Review manually",
    "Review manually — incomplete model output.",
    "Incomplete model output",
    ]

    if result["recommendation"] in weak_recommendations:
        if build_readiness >= 65:
            result["recommendation"] = "Prototype first, with defined safeguards and validation."
        elif build_readiness >= 50:
            result["recommendation"] = "Narrow scope before prototype, with human review and validation."
        elif build_readiness >= 35:
            result["recommendation"] = "Rework the product framing before moving forward."
        else:
            result["recommendation"] = "Avoid or rethink the AI feature as currently framed."

    score_keys = ["ai_fit", "commercial_upside", "risk_burden", "evidence_readiness"]
    missing_score_keys = [
        key for key in score_keys
        if key not in result or result[key] in ["", None]
    ]

    if missing_score_keys:
        st.warning(
            f"LLM output was missing score fields: {missing_score_keys}. "
            "Scores may be unreliable.")

    weak_fields = [
        key for key in [
            "core_tension",
            "useful_kernel",
            "commercial_value",
            "risky_framing",
            "human_reviewer",
            "review_package",
            "review_scope",
            "review_timing",
            "review_action",
            "next_validation_step",
            "ai_fit_driver",
            "commercial_driver",
            "risk_driver",
            "evidence_driver",
            "validation_method",
            "validation_coverage",
            "move_forward_criteria",
            "stop_or_redesign_signal",
        ]
        if result[key] in ["", None, "Not provided.", "Not provided"]
    ]

    if not result["review_package"] or result["review_package"] == ["Not provided."]:
        weak_fields.append("review_package")
    
    if not result["validation_metrics"] or result["validation_metrics"] == ["Not provided."]:
        weak_fields.append("validation_metrics")

    if result["confidence"] in ["", None, "Low"] and len(weak_fields) == 0:
        result["confidence"] = "Medium"
    elif result["confidence"] in ["", None]:
        result["confidence"] = "Low"
 
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
    st.markdown(f"**Dominant risk type:** {result['risk_type']}")
    st.markdown("**Risk themes:**")
    for theme in result["risk_themes"]:
        st.markdown(f"- {theme}")
    st.markdown(f"**Risk rationale:** {result['risk_rationale']}")

    st.info(
        "AIFit provides structured decision support, not final product judgment. "
        "Custom evaluations are generated using an LLM and may vary across runs. "
        "Teams should review outputs with appropriate product, domain, legal, or policy experts before making launch decisions."
    )

    st.divider()

    # Move detailed sections into expanders:
    # Core tension
    st.subheader("Core tension")
    st.write(result["core_tension"])

    # Build / not build stays visible
    col_build, col_not_build = st.columns(2)

    with col_build:
        st.subheader("What to build")
        for item in result["what_to_build"]:
            st.markdown(f"- {item}")

    with col_not_build:
        st.subheader("What not to build")
        for item in result["what_not_to_build"]:
            st.markdown(f"- {item}")

    # Detailed sections hidden by default
    with st.expander("Score drivers"):
        st.markdown(f"**AI Fit:** {result['ai_fit_driver']}")
        st.markdown(f"**Commercial:** {result['commercial_driver']}")
        st.markdown(f"**Risk:** {result['risk_driver']}")
        st.markdown(f"**Evidence:** {result['evidence_driver']}")

    with st.expander("Human review workflow"):
        st.markdown(f"**Reviewer:** {result['human_reviewer']}")
        st.markdown("**Review package:**")
        for item in result["review_package"]:
            st.markdown(f"- {item}")
        st.markdown(f"**Review scope:** {result['review_scope']}")
        st.markdown(f"**Timing:** {result['review_timing']}")
        st.markdown(f"**Decision authority:** {result['review_action']}")

    with st.expander("Validation workflow"):
        st.markdown(f"**Method:** {result['validation_method']}")
        st.markdown(f"**Validation coverage:** {result['validation_coverage']}")
        st.markdown("**Metrics:**")
        for item in result["validation_metrics"]:
            st.markdown(f"- {item}")
        st.markdown(f"**Move-forward criteria:** {result['move_forward_criteria']}")
        st.markdown(f"**Stop or redesign signal:** {result['stop_or_redesign_signal']}")
    
    # ------------------------------
    # Markdown version of result
    # ------------------------------
    what_to_build_md = [f"- {item}" for item in result["what_to_build"]]
    what_not_to_build_md = [f"- {item}" for item in result["what_not_to_build"]]

     # create filename for markdown file:
    def make_safe_filename(text, max_length=35):
        """
        Create a short, safe filename from user-provided text.
        """
        text = text.lower().strip()
        # Keep only letters, numbers, spaces, underscores, and hyphens
        safe_chars = []
        for char in text:
            if char.isalnum() or char in [" ", "_", "-"]:
                safe_chars.append(char)
        filename = "".join(safe_chars)
        # Replace spaces with underscores
        filename = filename.replace(" ", "_")
        # Collapse repeated underscores
        while "__" in filename:
            filename = filename.replace("__", "_")
        # Truncate
        filename = filename[:max_length].strip("_")
        # Fallback if empty
        if not filename:
            filename = "aifit_result"
        return filename
    
    display_feature = feature_idea if selected_case == "Start from blank" else selected_case
    safe_filename= make_safe_filename(display_feature)

    markdown_lines = [
        "# AIFit Result",
        "",
        "## Feature",
        display_feature,
        "",
        "## Feature Information",
        "",
        "### Feature Idea",
        feature_idea,
        "",
        "### Target User",
        target_user,
        "",
        "### User Problem",
        user_problem,
        "",
        "### Proposed AI Capability",
        ai_capability,
        "",
        "### Current Non-AI Alternative",
        non_ai_alternative,
        "",
        "### Human Decision Influenced",
        human_decision,
        "",
        "### Impact If Wrong",
        impact_if_wrong,
        "",
        "### Data Sensitivity",
        data_sensitivity,
        "",
        "### Business Value",
        business_value,
        "",
        "### Success Metric",
        success_metric,
        "",
        "---",
        "",
        "## Recommendation",
        result["recommendation"],
        "",
        "## Build Readiness",
        f"{build_readiness:.0f}/100",
        "",
        "## Decision Band",
        decision_band,
        "",
        "## Score Snapshot",
        f"- AI Fit: {ai_fit}/100",
        f"- Commercial Upside: {commercial_upside}/100",
        f"- Risk Burden: {risk_burden}/100",
        f"- Evidence Readiness: {evidence_readiness}/100",
        f"- Confidence: {result['confidence']}",
        "",
        "## Core Tension",
        result["core_tension"],
        "",
        "## Risk Type",
        result["risk_type"],
        "",
        "## Risk Themes",
        *[f"- {item}" for item in result["risk_themes"]],
        "",
        "## Risk Rationale",
        result["risk_rationale"],
        "",
        "## Useful Kernel",
        result["useful_kernel"],
        "",
        "## Commercial Value Worth Preserving",
        result["commercial_value"],
        "",
        "## Risky Framing",
        result["risky_framing"],
        "",
        "## What to Build",
        *what_to_build_md,
        "",
        "## What Not to Build",
        *what_not_to_build_md,
        "",
        "## Human Review Workflow",
        "",
        "### Reviewer",
        result["human_reviewer"],
        "",
        "### Review Package",
        *[f"- {item}" for item in result["review_package"]],
        "",
        "### Review Scope",
        result["review_scope"],
        "",
        "### Review Timing",
        result["review_timing"],
        "",
        "### Decision Authority",
        result["review_action"],
        "",
        "## Validation Workflow",
        "",
        "### Method",
        result["validation_method"],
        "",
        "### Validation Coverage",
        result["validation_coverage"],
        "",
        "### Metrics",
        *[f"- {item}" for item in result["validation_metrics"]],
        "",
        "### Move-forward Criteria",
        result["move_forward_criteria"],
        "",
        "### Stop or Redesign Signal",
        result["stop_or_redesign_signal"],
    ]

    markdown_output = "\n".join(markdown_lines)

    # Add a button to copy/download markdown output:
    with st.expander("Copy or download Markdown report"):
        st.markdown("### Markdown preview")
        st.markdown(markdown_output)

        with st.expander("Copy raw Markdown"):
            st.text_area("Raw Markdown", markdown_output, height=400)

        st.download_button(
            label="Download Markdown",
            data=markdown_output,
            file_name=f"{safe_filename}_aifit_result.md",
            mime="text/markdown"
        )

