# src/app.py
import streamlit as st
from predict_utils import predict_single

st.set_page_config(page_title="Fake Job Detector — Safe + Tamper", layout="wide")
st.markdown("""
<style>
body, .stApp { background-color: #f6f8fa; color: #0f172a; font-family: Inter, sans-serif; }
.result-box, .reasoning-box { background:#fff; border-radius:12px; padding:18px; box-shadow: 0 6px 18px rgba(2,6,23,0.06); }
.keyword { background:#fff7cc; border-radius:6px; padding:4px 8px; margin-right:6px; display:inline-block; margin-bottom:6px;}
.tamper { background:#fff1f2; border-left:4px solid #ef4444; padding:8px; border-radius:6px; margin-bottom:8px; }
</style>
""", unsafe_allow_html=True)

st.title("🕵️‍♂️ Fake Job Detector — Safe + Tamper Detection")
st.caption("OpenAI + ML + Email + Web + Hybrid Tamper Detection (Safe Mode)")

job_text = st.text_area("Paste job description here", height=380, placeholder="Paste full job posting...")

if st.button("Analyze"):
    if not job_text.strip():
        st.warning("Paste a job description first.")
        st.stop()

    with st.spinner("Analyzing..."):
        out = predict_single({"description": job_text})

    left, right = st.columns([1.6, 1])

    with left:
        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
        st.header(f"Result: {out['final_label']}")
        if out['final_label'] == "REAL":
            st.success("This posting appears REAL (Safe Mode).")
        elif out['final_label'] == "FAKE_SCAM":
            st.error("This posting appears FAKE / SCAM.")
        elif out['final_label'] == "FAKE_MODIFIED":
            st.error("This posting appears to be a REAL posting that has been MODIFIED (possible tampering).")
        elif out['final_label'] == "AUTO_GENERATED":
            st.warning("This posting looks AI-generated / templated.")
        elif out['final_label'] == "FICTIONAL":
            st.info("This posting appears fictional.")
        st.write("")
        st.subheader("Key Scores")
        sc = out['scores']
        st.write(f"- **ML Scam Probability:** {sc['scam_prob_model']:.2f}")
        st.write(f"- **OpenAI Realism Score:** {sc['realism_score']:.2f}")
        if sc.get('anomaly_score') is not None:
            st.write(f"- **Anomaly Score:** {sc['anomaly_score']:.2f}")

        st.subheader("Tamper / Integrity")
        integrity = out.get("integrity", {})
        tamper_score = integrity.get("tamper_score", 0.0)
        st.progress(tamper_score)
        st.write(f"Tamper Score: **{tamper_score:.2f}**")
        if tamper_score >= 0.65:
            st.markdown("<div class='tamper'>⚠️ High tamper score — posting contains suspicious modifications or injected content.</div>", unsafe_allow_html=True)

        suspicious = integrity.get("suspicious_spans", [])
        if suspicious:
            st.markdown("### Suspicious spans / indicators")
            for s in suspicious:
                st.write(f"- {s}")

        st.subheader("Suspicious Keywords")
        if out['fake_keywords']:
            for k in out['fake_keywords']:
                st.markdown(f"<span class='keyword'>{k}</span>", unsafe_allow_html=True)
        else:
            st.write("None found.")

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='reasoning-box'>", unsafe_allow_html=True)
        st.subheader("AI Reasoning (Doc-level)")
        st.write(out.get('gemini', {}).get('explanation', 'No explanation provided.'))

        st.subheader("Web Verification")
        web = out.get('web_verification', {})
        st.write(f"- Company detected: **{web.get('company_detected','Unknown')}**")
        st.write(f"- Verdict: **{web.get('web_verdict')}** (conf {web.get('confidence',0):.2f})")
        st.write("Reason: " + web.get('reasoning', 'No reasoning available.'))

        st.subheader("Email checks")
        emails = out.get('emails_checked') or []
        if emails:
            for e in emails:
                addr = e.get('email')
                status = e.get('status')
                expl = e.get('explanation') or e.get('openai', {}).get('explanation', '')
                if status == "valid":
                    st.success(f"✅ {addr} → {expl}")
                elif status == "suspicious":
                    st.warning(f"⚠ {addr} → {expl}")
                elif status == "invalid":
                    st.error(f"❌ {addr} → {expl}")
                else:
                    st.info(f"{addr} → {expl}")
        else:
            st.info("No emails detected.")
        st.markdown("</div>", unsafe_allow_html=True)
