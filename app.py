import streamlit as st
from pipeline.claim_extractor import extract_claims
from pipeline.fact_checker import fact_check
from pipeline.responder import generate_response

st.title("🩺 Maternal Health Fact Checker")
st.write("Check if a pregnancy-related health claim is true or false.")

user_input = st.text_area(
    "Enter a health claim or message:",
    placeholder="e.g. Don't eat papaya during pregnancy, it causes miscarriage."
)

if st.button("Check Claim"):
    if user_input.strip() == "":
        st.warning("Please enter a claim first.")
    else:
        with st.spinner("Analyzing..."):
            claims = extract_claims(user_input)
            results = fact_check(claims)
            response = generate_response(results)

        # Severity badge color
        severity_color = {
            "DANGEROUS": "🔴",
            "HARMFUL": "🟠", 
            "BENIGN": "🟢"
        }
        badge = severity_color.get(response["severity"], "⚪")

        st.subheader("Result")
        st.markdown(f"**Verdict:** {response['verdict']}")
        st.markdown(f"**Severity:** {badge} {response['severity']}")
        st.markdown(f"**Confidence:** {int(response['confidence'] * 100)}%")
        st.progress(response["confidence"])
        
        st.subheader("Analysis")
        st.write(response["response"])
        
        st.subheader("Sources")
        for source in response["cited_sources"]:
            st.markdown(f"→ [{source}]({source})")