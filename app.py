
import streamlit as st
import json
import re
from pathlib import Path
from agent import research_oauth_provider

# --------------------------------------------------
# 1. Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="OAuthReady",
    layout="wide"
)

# --------------------------------------------------
# 2. Load API keys
# --------------------------------------------------

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]

# --------------------------------------------------
# 3. Custom UI styling
# --------------------------------------------------

st.markdown("""
<style>

/* Main application background */
.stApp {
    background:
        radial-gradient(circle at 85% 5%, #142b4d 0%, transparent 35%),
        linear-gradient(135deg, #080d19 0%, #0b1220 55%, #101b31 100%);
    color: #e5edff;
}

/* Main content width */
.block-container {
    max-width: 1250px;
    padding-top: 2.5rem;
    padding-bottom: 4rem;
}

/* Hide Streamlit header decoration */
header[data-testid="stHeader"] {
    background: transparent;
}

/* Main headings */
h1, h2, h3 {
    color: #edf3ff !important;
    font-weight: 700 !important;
}

/* Paragraphs */
p, li, label {
    color: #a9b8d1;
}

/* Hero section */
.hero {
    background: linear-gradient(120deg, #142b49, #101a2d);
    border: 1px solid #31527b;
    border-radius: 24px;
    padding: 38px 42px;
    margin-bottom: 26px;
    box-shadow: 0 15px 45px rgba(0,0,0,0.18);
}

.hero-label {
    color: #48a5ff;
    font-size: 12px;
    letter-spacing: 4px;
    font-weight: 700;
    margin-bottom: 16px;
}

.hero-title {
    color: #f1f5ff;
    font-size: clamp(34px, 5vw, 58px);
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 16px;
}

.hero-title span {
    color: #399cff;
}

.hero-description {
    color: #a7b8d3;
    font-size: 17px;
    line-height: 1.7;
    max-width: 750px;
}

/* Section cards */
.panel {
    background: rgba(12, 20, 35, 0.88);
    border: 1px solid #243650;
    border-radius: 22px;
    padding: 25px;
    margin-bottom: 22px;
}

/* Small section labels */
.eyebrow {
    color: #60a5fa;
    font-size: 11px;
    letter-spacing: 3px;
    font-weight: 700;
}

/* Metric cards */
.metric-card {
    background: #0a1221;
    border: 1px solid #243650;
    border-radius: 17px;
    padding: 20px;
    min-height: 105px;
}

.metric-label {
    color: #8194b2;
    font-size: 11px;
    letter-spacing: 2px;
    margin-bottom: 12px;
}

.metric-value {
    color: #55a7ff;
    font-size: 19px;
    font-weight: 700;
}

/* Regular buttons */
.stButton > button {
    background: #101d31;
    color: #e5edff;
    border: 1px solid #31527b;
    border-radius: 30px;
    padding: 10px 18px;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: #17375e;
    color: white;
    border-color: #399cff;
}

/* Primary research button — high contrast */
div[data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(100deg, #1675df, #299cff) !important;
    color: #ffffff !important;
    border: 1px solid #58adff !important;
    border-radius: 14px !important;
    min-height: 52px;
    padding: 12px 20px !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    box-shadow: 0 5px 20px rgba(41, 156, 255, 0.25);
    opacity: 1 !important;
}

div[data-testid="stButton"] button[kind="primary"] p,
div[data-testid="stButton"] button[kind="primary"] span {
    color: #ffffff !important;
    font-weight: 700 !important;
    opacity: 1 !important;
}

div[data-testid="stButton"] button[kind="primary"]:hover {
    background: linear-gradient(100deg, #2589f0, #45adff) !important;
    border-color: #8ac7ff !important;
    color: #ffffff !important;
}

/* Text inputs */
.stTextInput input {
    background: #101827;
    color: #edf3ff;
    border: 1px solid #2c405d;
    border-radius: 12px;
}

/* Expanders */
div[data-testid="stExpander"] {
    background: #101a2a;
    border: 1px solid #263b57;
    border-radius: 14px;
    margin-bottom: 10px;
}

/* Dividers */
hr {
    border-color: #263750;
}

/* Links */
a {
    color: #48a5ff !important;
}

/* Captions */
.stCaption {
    color: #8194b2 !important;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 4. Reusable UI functions
# --------------------------------------------------

def section_title(label, title):
    st.markdown(
        f'<div class="eyebrow">{label}</div>',
        unsafe_allow_html=True
    )
    st.subheader(title)


def metric_card(label, value):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# 5. Hero section
# --------------------------------------------------

st.markdown("""
<div class="hero">
    <div class="hero-label">OAUTHREADY</div>
    <div class="hero-title">
        Your OAuth <span>setup assistant</span>
    </div>
    <div class="hero-description">
        Understand OAuth requirements, configure provider apps,
        and get step-by-step setup guidance.
    </div>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 6. Provider selection
# --------------------------------------------------

if "selected_provider" not in st.session_state:
    st.session_state.selected_provider = "GitHub"

with st.container(border=True):

    section_title("GUIDE LIBRARY", "Pick a provider")

    st.caption(
        "Library guides are hand-checked. "
        "Other provider names use the AI research agent."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("GitHub", use_container_width=True):
            st.session_state.selected_provider = "GitHub"
            st.session_state.pop("research_result", None)
            st.session_state.pop("research_provider", None)
            st.session_state["scroll_to_library"] = True
            st.rerun()

    with col2:
        if st.button("Slack", use_container_width=True):
            st.session_state.selected_provider = "Slack"
            st.session_state.pop("research_result", None)
            st.session_state.pop("research_provider", None)
            st.session_state["scroll_to_library"] = True
            st.rerun()

    with col3:
        if st.button("Google", use_container_width=True):
            st.session_state.selected_provider = "Google"
            st.session_state.pop("research_result", None)
            st.session_state.pop("research_provider", None)
            st.session_state["scroll_to_library"] = True
            st.rerun()

    st.caption(
        f"Selected provider: {st.session_state.selected_provider} ----Scroll down to view the guide."
    )

    st.divider()

    section_title("LIVE RESEARCH", "Explore another provider")

    new_provider = st.text_input(
        "Enter a provider name",
        placeholder="e.g. Zoho, Zoom or Dropbox",
        label_visibility="collapsed"
    )

    if st.button(
        "✨  Generate OAuth Research Guide",
        type="primary",
        use_container_width=True
    ):

        if not new_provider.strip():
            st.warning("Please enter a provider name.")

        else:
            with st.spinner(
                f"Researching {new_provider} OAuth documentation..."
            ):
                try:
                    research_result = research_oauth_provider(
                        provider=new_provider.strip(),
                        tavily_api_key=TAVILY_API_KEY,
                        gemini_api_key=GEMINI_API_KEY
                    )

                    st.session_state["research_result"] = research_result
                    st.session_state["research_provider"] = new_provider.strip()

                except Exception as error:
                    st.error(f"Research failed: {error}")


# --------------------------------------------------
# 7. Display AI-generated research
# --------------------------------------------------

if "research_result" in st.session_state:

    research_result = st.session_state["research_result"]
    research_provider = st.session_state["research_provider"]

    st.divider()

    section_title("AI RESEARCH AGENT · LIVE", research_provider)

    st.info("AI-generated guide · Not hand-checked")

    with st.container(border=True):

        section_title("RESEARCH REPORT", "AI-generated research guide")

        st.markdown(research_result["report"])

        # Download report
        download_content = (
            f"# {research_provider} OAuth Setup Guide\n\n"
            f"{research_result['report']}\n\n"
            "## Sources\n\n"
        )

        for source in research_result["sources"]:
            download_content += (
                f"- **{source['title']}** "
                f"({source['source_type']})\n"
                f"  - {source['url']}\n"
            )

        st.download_button(
            label="Download OAuth Guide",
            data=download_content,
            file_name=f"{re.sub(r'[^a-z0-9]+', '_', research_provider.lower())}_oauth_guide.md",
            mime="text/markdown"
        )

    # Source audit
    sources = research_result["sources"]

    official_count = sum(
        1 for source in sources
        if source["source_type"] == "Official Provider Documentation"
    )

    third_party_count = sum(
        1 for source in sources
        if source["source_type"] == "Third-party Source"
    )

    with st.container(border=True):

        section_title("SOURCE AUDIT", "Source audit & verification")

        col1, col2, col3 = st.columns(3)

        with col1:
            metric_card("TOTAL SOURCES", len(sources))

        with col2:
            metric_card("OFFICIAL SOURCES", official_count)

        with col3:
            metric_card("THIRD-PARTY SOURCES", third_party_count)

        st.write("")

        for index, source in enumerate(sources, start=1):

            with st.expander(
                f"Source {index}: {source['title']}"
            ):

                st.write(
                    f"**Classification:** {source['source_type']}"
                )

                st.markdown(
                    f"[Open source documentation]({source['url']})"
                )

        st.caption(
            "Source classification is based on domain matching. "
            "It does not independently verify the accuracy of a page."
        )


# --------------------------------------------------
# 8. Load selected library guide
# --------------------------------------------------

provider = st.session_state.selected_provider

guide_path = (
    Path(__file__).parent
    / "guides"
    / f"{provider.lower()}.json"
)

with open(guide_path, "r", encoding="utf-8") as file:
    guide = json.load(file)


# --------------------------------------------------
# 9. Provider overview
# --------------------------------------------------

st.divider()

# Scroll target for the selected provider guide
st.markdown(
    '<div id="library-guide"></div>',
    unsafe_allow_html=True
)

if st.session_state.pop("scroll_to_library", False):
    st.components.v1.html(
        """
        <script>
            const target = window.parent.document.getElementById("library-guide");
            if (target) {
                target.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });
            }
        </script>
        """,
        height=0
    )

section_title("LIBRARY GUIDE", guide["app_name"])

st.caption(guide["category"])

st.info(f"Evidence status: {guide['status']}")

with st.container(border=True):

    section_title("AT A GLANCE", "Setup overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card("DIFFICULTY", guide["difficulty"])

    with col2:
        metric_card(
            "HANDS-ON SETUP",
            guide["time_estimate"]["hands_on"]
        )

    with col3:
        metric_card(
            "APPROVAL WAIT",
            guide["time_estimate"]["approval_wait"]
        )

    st.caption(guide["time_estimate"]["note"])


# --------------------------------------------------
# 10. OAuth options
# --------------------------------------------------

with st.container(border=True):

    section_title("AUTHENTICATION", "OAuth options")

    oauth = guide["oauth_options"]

    col1, col2 = st.columns(2)

    with col1:

        if oauth.get("managed_oauth_available") is True:
            st.success("Composio-managed OAuth available")

        elif oauth.get("managed_oauth_status") == "Needs verification":
            st.warning("Composio-managed OAuth: Needs verification")

        else:
            st.info("Composio-managed OAuth: Check availability")

    with col2:

        if oauth.get("bring_your_own_oauth_available") is True:
            st.success("Bring Your Own OAuth available")

        else:
            st.info("Bring Your Own OAuth: Not confirmed")

    st.write(oauth["recommendation"])


# --------------------------------------------------
# 11. Prerequisites
# --------------------------------------------------

with st.container(border=True):

    section_title("BEFORE YOU START", "Prerequisites")

    for item in guide["prerequisites"]:
        st.markdown(f"- {item}")


# --------------------------------------------------
# 12. Setup instructions
# --------------------------------------------------

with st.container(border=True):

    section_title("YOUR ROADMAP", "Step-by-step setup guide")

    st.caption(
        "Follow each step in order to configure your provider OAuth app."
    )

    for step in guide["setup_steps"]:

        with st.expander(
            f"Step {step['step']} · {step['title']}"
        ):

            st.write(step["description"])


# --------------------------------------------------
# 13. Potential blockers
# --------------------------------------------------

with st.container(border=True):

    section_title("TROUBLESHOOTING", "Potential blockers")

    for blocker in guide["potential_blockers"]:
        st.warning(blocker)


# --------------------------------------------------
# 14. Evidence and verification
# --------------------------------------------------

with st.container(border=True):

    section_title("EVIDENCE", "Evidence and verification")

    for item in guide["evidence"]:

        st.markdown(f"**{item['type']}**")
        st.write(item["claim"])

        st.divider()


# --------------------------------------------------
# 15. Limitations
# --------------------------------------------------

with st.container(border=True):

    section_title("TRANSPARENCY", "What has not been tested")

    for limitation in guide["limitations"]:
        st.markdown(f"- {limitation}")


# --------------------------------------------------
# 16. Official sources
# --------------------------------------------------

with st.container(border=True):

    section_title("DOCUMENTATION", "Official sources")

    for index, source in enumerate(guide["sources"], start=1):
        st.markdown(f"{index}. [{source}]({source})")


# --------------------------------------------------
# 17. Footer
# --------------------------------------------------

st.markdown("""
<hr>
<div style="text-align:center; padding:20px 0;">
    <div style="color:#60a5fa; letter-spacing:3px;
                font-size:12px; font-weight:700;">
        OAUTHREADY
    </div>
    <div style="color:#8194b2; font-size:12px; margin-top:8px;">
        Making OAuth setup easier for developers.
    </div>
</div>
""", unsafe_allow_html=True)
