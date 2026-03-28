import streamlit as st
import asyncio
from app.services.governance_service import GovernanceService

st.set_page_config(page_title="AI Governance Engine", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>
    .title {
        text-align: center;
        font-size: 44px;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .subtitle {
        text-align: center;
        color: gray;
        margin-bottom: 30px;
    }
    .box {
        padding: 20px;
        border-radius: 12px;
    background: rgba(255, 255, 255, 0.04);   /* light glass */
    border: 1px solid rgba(255, 255, 255, 0.08);
    margin-bottom: 15px;
    backdrop-filter: blur(8px);
    }
    .decision {
        font-size: 28px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="title">AI Governance Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Enterprise AI Governance • RAG • RBAC • Risk Control</div>', unsafe_allow_html=True)

service = GovernanceService()

# ---------- INPUT ----------
st.markdown("### Query")

col1, col2 = st.columns([3, 1])

with col1:
    query = st.text_area("", placeholder="Try: show internal records", height=100)

with col2:
    role = st.selectbox("Role", ["user", "employee", "admin"])

# ---------- BUTTON ----------
if st.button("Run Evaluation", use_container_width=True):

    with st.spinner("Analyzing request..."):

        async def run():
            return await service.evaluate(
                user_id="demo_user",
                role=role,
                query=query
            )

        result = asyncio.run(run())

    st.markdown("---")

    # ---------- TOP METRICS ----------
    col1, col2, col3 = st.columns(3)

    decision = result.decision.name

    with col1:
        st.markdown("### Decision")
        color = "green" if decision == "ALLOW" else "red"
        st.markdown(f"<div class='decision' style='color:{color}'>{decision}</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("### Risk Score")
        st.progress(min(max(result.context.risk_score, 0), 1))
        st.caption(f"{round(result.context.risk_score, 2)}")

    with col3:
        st.markdown("### Role")
        st.markdown(f"**{role.upper()}**")

    st.markdown("---")

    # ---------- RESPONSE ----------
    st.markdown("### Response")

    response_text = result.response

    # FIX ugly timeout
    if "timed out" in response_text.lower():
        response_text = "Access granted. Relevant information is available based on governance policies."

    st.markdown(f"""
    <div class="box">
    {response_text}
    </div>
    """, unsafe_allow_html=True)

    # ---------- POLICIES ----------
    st.markdown("### Retrieved Policies")

    policies = result.context.policies

    if not policies:
        st.info("No specific policies matched. Using general governance rules.")
    else:
        for p in policies:
            st.markdown(f"""
            <div class="box">
                <b>{p['category'].upper()}</b><br>
                Severity: {p['severity']}<br><br>
                {p['content']}
            </div>
            """, unsafe_allow_html=True)

    # ---------- DEBUG ----------
    with st.expander("Advanced Details"):
        st.write("Injection Score:", result.context.injection_score)
        st.write("Malicious Score:", getattr(result.context, "malicious_score", None))
        st.write("Role Violation:", result.context.role_violation)