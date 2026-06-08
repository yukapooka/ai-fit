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
    "validation_sample": "string",
    "validation_metrics": ["string"],
    "success_threshold": "string",
    "failure_trigger": "string",
}

# Define a prompt builder function:
def build_aifit_prompt(user_inputs):
    return f"""
You are an experienced AI product manager specializing in responsible AI product launches.
Evaluate the proposed AI feature using the AIFit framework.

Return one JSON object only. Do not include text before or after the JSON.
You must fill every field with useful, product-specific content.
Do not leave any field blank.
Do not write "Not provided."
Scores must be integers from 0 to 100.
Do not include "/100", labels, or words in score fields.
Use the exact top-level keys provided in the schema.
Do not rename keys.
Do not nest score drivers.
Important scoring rule:
The four score fields must be numeric integers only.
Use:
"ai_fit": 80

Do not use:
"ai_fit": "80/100"
"ai_fit": "High"
"ai_fit_driver": "AI is useful... 80"
Do not place score numbers inside driver text.
Driver fields should contain explanation only, no numeric score.

You must fill these fields separately:
- ai_fit: integer from 0 to 100
- ai_fit_driver: explanation sentence with no number
- commercial_upside: integer from 0 to 100
- commercial_driver: explanation sentence with no number
- risk_burden: integer from 0 to 100
- risk_driver: explanation sentence with no number
- evidence_readiness: integer from 0 to 100
- evidence_driver: explanation sentence with no number

For core_tension:
Write one sentence in this format:
"AI may [create specific product/user/business value], but may also [create specific risk or failure mode]."

For risk_type:
Classify the dominant risk_type using one of the following labels:
- False validation
- Emotional vulnerability
- Financial manipulationh
- Fairness / bias
- Privacy / sensitive data
- Over-reliance
- Workflow misalignment
- Safety escalation
- Incentive misalignment
- General AI product risk

For ai_fit_driver:
Explain why AI is or is not meaningfully justified beyond a simpler solution.

For commercial_driver:
Explain the likely business value, such as adoption, retention, efficiency, differentiation, or revenue.

For risk_driver:
Explain the main product, user, governance, or failure risk.

For evidence_driver:
Explain what makes this feature easy or hard to validate before launch.

The following fields are required and must contain one concrete sentence each:
"useful_kernel": What part of the idea is worth preserving for users?
"commercial_value": What business value is worth preserving without increasing risk?
"risky_framing": What product framing should the team avoid?
"human_checkpoint": Which human reviewer must review the output before product decisions are made?
Do not leave these fields blank.
Do not write "Not provided."
Do not rename these fields.

Example:
"useful_kernel": "Use AI to summarize support tickets, cluster recurring issues, and help humans identify patterns faster."
"commercial_value": "Preserve operational efficiency and faster product feedback loops without automating roadmap prioritization."
"risky_framing": "An AI system that directly decides which customer complaints should drive the roadmap."
"human_checkpoint": "Support leads and product managers should review AI escalation suggestions before they influence roadmap discussions."

For what_to_build and what_not_to_build:
Return 3 to 6 specific product-scope bullets each.

For next_validation_step:
Give one concrete test the product team should run next.

Output schema:
The JSON object must follow this exact schema:
{json.dumps(AIFIT_JSON_SCHEMA, indent=2)}

For the human review workflow, fill each field separately:
human_reviewer: Who should review the AI output? Be specific to the dominant risk type.
review_package: Return 4 to 6 concrete artifacts the reviewer should inspect.
Do not use generic terms like "AI output" or "feedback report" alone.
Include source material, generated output, scoring logic, edge cases, subgroup comparisons, and user-facing wording where relevant.
review_scope: What variation, subgroup, edge case, or risk pattern should the reviewer check? Be specific.
review_timing: When should the review happen? For example: before pilot launch, after the first pilot batch, before public release, or periodically after deployment.
review_action: What can the reviewer do? For example: approve, revise scoring rules, request safeguards, escalate concerns, or block release.

For Fairness / bias risk, review_package should include:
- generated outputs across different user subgroups
- source inputs used to generate those outputs
- scoring rubric or evaluation criteria
- subgroup comparison or disparity summary
- low-confidence or borderline examples
- user-facing wording that may affect confidence, identity, or self-presentation

For Privacy / sensitive data risk, review_package should include:
- raw input examples containing sensitive data
- redacted output examples
- data retention and deletion policy
- access control rules
- consent and user disclosure copy
- failure cases where sensitive information may leak

For False validation risk, review_package should include:
- AI-generated claims or recommendations
- original source evidence
- assumption-versus-evidence classification
- comparison against real user or expert feedback
- examples where AI overstates confidence

For the validation workflow, fill each field separately:
validation_method:
What concrete test should the product team run next? Be specific to the dominant risk type.
validation_sample:
What data, users, cases, outputs, or scenarios should be included in the validation?
validation_metrics:
Return 3 to 5 specific metrics or review criteria. These should measure both product value and risk.
move_forward_criteria:
Describe the qualitative evidence needed to justify moving forward. Do not invent numeric thresholds unless the user explicitly provides them. Use language such as "strong expert agreement", "no material subgroup disparity", "users understand the AI output as advisory", or "no recurring harmful pattern."
stop_or_redesign_signal:
Describe the evidence that should cause the team to narrow, redesign, or stop the feature. Focus on concerning patterns, not arbitrary numeric cutoffs.
Do not use unsupported numeric cutoffs such as ">80%", "<10%", or "4/5" unless those numbers are explicitly provided in the feature information.

For Fairness / bias risk:
- validation_method should compare AI outputs across relevant user subgroups.
- validation_sample should include diverse user profiles, edge cases, and borderline examples.
- validation_metrics should include subgroup disparity, expert agreement, perceived fairness, user confidence impact, and harmful feedback rate.
- failure_trigger should include evidence that the system penalizes valid non-standard communication styles.

For Privacy / sensitive data risk:
- validation_method should test redaction, retention, deletion, and access control.
- validation_sample should include inputs containing sensitive information and adversarial privacy cases.
- validation_metrics should include leakage rate, redaction accuracy, deletion success, access control failures, and user comprehension of consent.
- failure_trigger should include any uncontrolled exposure of sensitive information.

For False validation risk:
- validation_method should compare AI-generated claims or recommendations against real user evidence or expert review.
- validation_sample should include AI outputs, original source evidence, weak-evidence cases, and contradictory examples.
- validation_metrics should include evidence alignment, hallucinated claims, overconfidence rate, and expert agreement.
- failure_trigger should include AI outputs being treated as validation without real evidence.

For Over-reliance risk:
- validation_method should test whether users treat AI output as suggestion or authority.
- validation_sample should include high-confidence, low-confidence, correct, incorrect, and ambiguous outputs.
- validation_metrics should include override rate, calibration accuracy, user understanding, and inappropriate reliance rate.
- failure_trigger should include users following incorrect AI recommendations without review.

Do not invent universal numeric thresholds unless they are explicitly provided by the user.
When defining success_threshold or failure_trigger:
- Use qualitative or directional thresholds by default.
- If numeric thresholds are useful, label them as example thresholds for team calibration.
- Do not present arbitrary numbers as universal standards.

Use phrases like:
- "team-defined acceptable range"
- "material disparity"
- "strong expert agreement"
- "no recurring harmful pattern"
- "calibrated threshold set before pilot"
rather than unsupported numeric cutoffs.

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

    if isinstance(result["review_package"], str):
        result["review_package"] = [result["review_package"]]
    elif not isinstance(result["review_package"], list):
        result["review_package"] = [
            "Representative AI-generated outputs",
            "Source inputs used to generate those outputs",
            "Scoring or evaluation criteria",
            "Low-confidence or borderline examples",
            "User-facing wording or recommendations"
        ]

    defaults = {
        "recommendation": "",
        "core_tension": "AI may create product value, but the current framing needs further review for user risk, evidence quality, and human oversight.",
        "risk_type": "General AI product risk",
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
        "validation_sample": "Representative user inputs, AI-generated outputs, edge cases, and human-reviewed examples.",
        "validation_metrics": [
            "Output accuracy",
            "User comprehension",
            "Human reviewer agreement",
            "Risk incident rate",
            "User trust or perceived usefulness"
        ],
        "move_forward_criteria": "Move forward if reviewers find the AI output useful, accurate, and appropriate for the intended context, with no recurring harmful pattern.",
        "stop_or_redesign_signal": "Narrow or redesign if reviewers identify recurring inaccuracies, harmful outputs, user misunderstanding, or risk patterns that cannot be addressed with safeguards.",
    }

    # Fill missing or empty top-level keys.
    for key, default_value in defaults.items():
        if key not in result or result[key] in ["", None]:
            result[key] = default_value

    # Ensure list fields are lists.
    for key in ["what_to_build", "what_not_to_build","review_package","validation_metrics"]:
        if isinstance(result[key], str):
            result[key] = [result[key]]
        elif not isinstance(result[key], list):
            result[key] = ["Not provided."]
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
            "validation_sample",
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

    st.divider()

    # Core tension
    st.subheader("Core tension")
    st.write(result["core_tension"])

    # Score drivers
    st.subheader("Score drivers")
    st.markdown(f"**AI Fit:** {result['ai_fit_driver']}")
    st.markdown(f"**Commercial:** {result['commercial_driver']}")
    st.markdown(f"**Risk:** {result['risk_driver']}")
    st.markdown(f"**Evidence:** {result['evidence_driver']}")

    # Useful kernel / commercial value / risky framing
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.subheader("Useful kernel")
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
    st.subheader("Human review workflow")
    st.markdown(f"**Reviewer:** {result['human_reviewer']}")
    st.markdown("**Review package:**")
    for item in result["review_package"]:
        st.markdown(f"- {item}")
    st.markdown(f"**Review scope:** {result['review_scope']}")
    st.markdown(f"**Timing:** {result['review_timing']}")
    st.markdown(f"**Decision authority:** {result['review_action']}")


    # Validation workflow:
    st.subheader("Validation workflow")
    st.markdown(f"**Method:** {result['validation_method']}")
    st.markdown(f"**Sample:** {result['validation_sample']}")
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
        "### Sample",
        result["validation_sample"],
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
    st.subheader("Copy result as Markdown")
    st.text_area("Markdown output", markdown_output, height=400)

    st.download_button(
        label="Download Markdown",
        data=markdown_output,
        file_name=f"{safe_filename}_aifit_result.md",
        mime="text/markdown"
    )