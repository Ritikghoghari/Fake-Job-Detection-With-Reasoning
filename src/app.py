import streamlit as st
from predict_utils import predict_single
from styles import get_custom_css

st.set_page_config(page_title="Fake Job Detector", layout="wide", page_icon="🛡️")
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.title("🛡️ Job Integrity Verifier")
st.markdown("##### Advanced AI-powered detection for fake, scam, and modified job postings.")

job_text = st.text_area("Paste job description here", height=200, placeholder="Paste the full job posting content here to analyze integrity and authenticity...")

if st.button("Analyze Posting"):
    if not job_text.strip():
        st.warning("Please paste a job description first.")
        st.stop()

    with st.spinner("Running deep analysis (ML + Web + Email Checks)..."):
        out = predict_single({"description": job_text})

    left, right = st.columns([1.5, 1])

    with left:
        # Determine status styling
        label = out['final_label']
        if label == "REAL":
            status_class = "status-real"
            status_icon = "✅"
            status_text = "LIKELY REAL"
        elif label == "FAKE_SCAM":
            status_class = "status-fake"
            status_icon = "🚨"
            status_text = "SCAM DETECTED"
        elif label == "FAKE_MODIFIED":
            status_class = "status-suspicious"
            status_icon = "⚠️"
            status_text = "MODIFIED / TAMPERED"
        elif label == "AUTO_GENERATED":
            status_class = "status-info"
            status_icon = "🤖"
            status_text = "AI GENERATED"
        else:
            status_class = "status-info"
            status_icon = "ℹ️"
            status_text = label

        # Result Card
        st.markdown(f"""
        <div class="custom-card">
            <div class="{status_class} status-badge">
                {status_icon} &nbsp; {status_text}
            </div>
            <p style="color: #64748b; font-size: 0.95rem; line-height: 1.6;">
                {out.get('gemini', {}).get('explanation', 'No detailed explanation provided.')}
            </p>
            
            <div class="metrics-grid">
                <div class="metric-item">
                    <div class="metric-value">{out['scores']['scam_prob_model']:.0%}</div>
                    <div class="metric-label">Scam Prob</div>
                </div>
                <div class="metric-item">
                    <div class="metric-value">{out['scores']['realism_score']:.0%}</div>
                    <div class="metric-label">Realism Score</div>
                </div>
                <div class="metric-item">
                    <div class="metric-value">{out.get('integrity', {}).get('tamper_score', 0):.0%}</div>
                    <div class="metric-label">Tamper Score</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Integrity Details
        integrity = out.get("integrity", {})
        tamper_score = integrity.get("tamper_score", 0.0)
        suspicious = integrity.get("suspicious_spans", [])
        
        st.markdown(f"""
        <div class="custom-card">
            <h3>🔍 Integrity Analysis</h3>
        """, unsafe_allow_html=True)
        
        if tamper_score > 0.1:
             bar_class = "high" if tamper_score > 0.5 else ""
             st.markdown(f"""
             <div style="margin-bottom: 15px;">
                 <small>Tamper / Modification Probability</small>
                 <div class="tamper-wrapper">
                     <div class="tamper-fill {bar_class}" style="width: {tamper_score*100}%"></div>
                 </div>
             </div>
             """, unsafe_allow_html=True)

        if suspicious:
            st.markdown("<strong>Suspicious Spans Detected:</strong>")
            for s in suspicious:
                st.markdown(f"- <span style='color:#b91c1c'>{s}</span>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='color:#15803d'>No suspicious text modifications detected.</p>", unsafe_allow_html=True)
            
        st.markdown("<h4>Suspicious Keywords</h4>", unsafe_allow_html=True)
        if out['fake_keywords']:
            kw_html = "".join([f"<span class='keyword-tag'>{k}</span>" for k in out['fake_keywords']])
            st.markdown(kw_html, unsafe_allow_html=True)
        else:
            st.markdown("<small>No typical scam keywords found.</small>", unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        # Web Verification Card
        web = out.get('web_verification', {})
        web_verdict = web.get('web_verdict', 'unknown').upper()
        verdict_color = "#15803d" if "REAL" in web_verdict or "LIKELY_REAL" in web_verdict else "#b91c1c"
        
        st.markdown(f"""
        <div class="custom-card">
            <h3>🌐 Web Verification</h3>
            <div style="margin-bottom: 15px;">
                <div style="color: #64748b; font-size: 0.85rem; text-transform: uppercase; font-weight: 600;">Company Detected</div>
                <div style="font-size: 1.1rem; font-weight: 600; color: #0f172a;">{web.get('company_detected','Unknown')}</div>
            </div>
            
            <div style="margin-bottom: 15px;">
                 <div style="color: #64748b; font-size: 0.85rem; text-transform: uppercase; font-weight: 600;">Web Cross-Check Verdict</div>
                 <div style="color: {verdict_color}; font-weight: 700;">{web_verdict.replace('_', ' ')}</div>
            </div>
            
            <p style="font-size: 0.9rem; color: #334155;">{web.get('reasoning', 'No reasoning available.')}</p>
        </div>
        """, unsafe_allow_html=True)

        # Email Analysis Card
        emails = out.get('emails_checked') or []
        
        st.markdown("""<div class="custom-card"><h3>📧 Email Verification</h3>""", unsafe_allow_html=True)
        
        if emails:
            for e in emails:
                addr = e.get('email', 'Unknown')
                status = e.get('status', 'unknown')
                expl = e.get('explanation') or e.get('openai', {}).get('explanation', '')
                
                icon = "❓"
                if status == "valid": icon = "✅"
                elif status == "suspicious": icon = "⚠️"
                elif status == "invalid": icon = "❌"
                
                st.markdown(f"""
                <div style="background: #f8fafc; padding: 10px; border-radius: 8px; margin-bottom: 8px; border: 1px solid #e2e8f0;">
                    <div style="font-weight: 600; font-size: 0.9rem; display: flex; align-items: center; gap: 8px;">
                        {icon} {addr}
                    </div>
                    <div style="font-size: 0.8rem; color: #64748b; margin-top: 4px;">{expl}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("<p style='color:#64748b'>No email addresses found in text.</p>", unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)
