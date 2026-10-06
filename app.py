import streamlit as st

from agent import analyze


st.set_page_config(
    page_title="AI Governance Review",
    page_icon="🛡️",
    layout="wide"
)

st.title("AI Governance Review")

st.write(
    "Review an AI use case against security and governance requirements."
)


examples = {
    "Custom": "",

    "Customer Support Assistant": (
        "A customer support team wants to use an LLM to summarize "
        "customer conversations and suggest responses to support agents. "
        "The system will process customer names, account information, "
        "support tickets, and conversation history. A human support agent "
        "will review the generated response before sending it to the customer. "
        "The application will use a third-party hosted LLM API."
    ),

    "Internal Security Assistant": (
        "The cybersecurity team wants to deploy an internal AI assistant "
        "that can analyze security alerts and recommend investigation steps. "
        "The assistant will have access to internal security logs and selected "
        "threat intelligence sources. Security analysts will review "
        "recommendations before taking action. The system will be deployed "
        "within the organization's cloud environment."
    ),

    "Automated Employee Decisions": (
        "HR wants to use an AI system to analyze employee performance "
        "information and automatically recommend employees for promotion. "
        "The system will process employee performance records and HR "
        "information. The AI recommendation will be used as the primary "
        "input into promotion decisions."
    )
}


selected = st.selectbox(
    "Example scenario",
    list(examples.keys())
)

scenario = st.text_area(
    "AI use case",
    value=examples[selected],
    height=220,
    placeholder="Describe the AI use case..."
)


if st.button(
    "Run assessment",
    type="primary",
    use_container_width=True
):
    try:
        with st.spinner("Assessing the scenario..."):
            result, trace = analyze(scenario)

        st.success("Assessment completed.")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Risk Level",
            result.risk_level
        )

        col2.metric(
            "Risk Score",
            f"{result.risk_score}/100"
        )

        col3.metric(
            "Confidence",
            f"{result.confidence:.0%}"
        )

        st.subheader("Use Case")
        st.write(result.use_case_type)

        st.subheader("Executive Summary")
        st.write(result.summary)

        st.subheader("Governance Requirements")

        for item in result.requirements:
            title = (
                f"{item.requirement_id} — "
                f"{item.title} — "
                f"{item.status}"
            )

            with st.expander(title):
                st.markdown("**Evidence**")
                st.write(item.evidence)

                st.markdown("**Recommendation**")
                st.write(item.recommendation)

        st.subheader("Key Risks")

        for risk in result.risks:
            st.write(f"• {risk}")

        st.subheader("Recommended Actions")

        for number, action in enumerate(
            result.actions,
            start=1
        ):
            st.write(f"{number}. {action}")

        st.subheader("Execution Trace")

        st.caption(
            "This trace shows application actions, not private model reasoning."
        )

        for number, step in enumerate(
            trace,
            start=1
        ):
            st.write(f"{number}. {step}")

    except Exception as error:
        st.error(str(error))
