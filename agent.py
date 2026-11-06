
from tavily import TavilyClient
from google import genai
from urllib.parse import urlparse
import time


# --------------------------------------------------
# 1. Official developer documentation domains
# --------------------------------------------------

OFFICIAL_DOMAINS = {
    "notion": [
        "developers.notion.com",
        "notion.com"
    ],
    "github": [
        "docs.github.com",
        "github.com"
    ],
    "slack": [
        "api.slack.com",
        "docs.slack.dev"
    ],
    "google": [
        "developers.google.com",
        "cloud.google.com"
    ],
    "hubspot": [
        "developers.hubspot.com"
    ]
}


# --------------------------------------------------
# 2. Research an OAuth provider
# --------------------------------------------------

def research_oauth_provider(provider, tavily_api_key, gemini_api_key):

    provider = provider.strip()

    # Connect to Tavily
    tavily = TavilyClient(api_key=tavily_api_key)

    # Find official domains for the selected provider
    official_domains = OFFICIAL_DOMAINS.get(
        provider.lower()
    )

    # --------------------------------------------------
    # 3. Search multiple OAuth topics using Tavily
    # --------------------------------------------------

    search_queries = [
        f"{provider} official API OAuth public integration authorization",
        f"{provider} API OAuth access token refresh token expiration",
        f"{provider} MCP server OAuth authorization token refresh",
        f"{provider} public integration permissions scopes redirect URI",
        f"{provider} OAuth verification approval marketplace requirements"
    ]

    all_results = []
    seen_urls = set()

    for query in search_queries:

        search_results = tavily.search(
            query=query,
            search_depth="advanced",
            max_results=3,
            include_domains=official_domains,
            include_domains_mode="prefer" if official_domains else None
        )

        for result in search_results["results"]:

            url = result["url"]

            # Avoid duplicate sources
            if url not in seen_urls:
                all_results.append(result)
                seen_urls.add(url)

    # --------------------------------------------------
    # 4. Extract and classify search results
    # --------------------------------------------------

    research_context = ""
    sources = []

    for index, result in enumerate(all_results, start=1):

        hostname = urlparse(result["url"]).hostname or ""
        hostname = hostname.lower()

        # Check whether the domain belongs to the provider
        is_official = any(
            hostname == domain or hostname.endswith("." + domain)
            for domain in (official_domains or [])
        )

        if is_official:
            source_type = "Official Provider Documentation"

        elif official_domains:
            source_type = "Third-party Source"

        else:
            source_type = "Source Not Yet Classified"

        source = {
            "id": f"S{index}",
            "title": result["title"],
            "url": result["url"],
            "source_type": source_type
        }

        sources.append(source)

        # Give Gemini identifiable source references
        research_context += (
            f"\n\nSOURCE ID: S{index}\n"
            f"Source Type: {source_type}\n"
            f"Title: {result['title']}\n"
            f"URL: {result['url']}\n"
            f"Retrieved Content: {result['content']}\n"
        )

    # --------------------------------------------------
    # 5. Connect to Gemini
    # --------------------------------------------------

    client = genai.Client(api_key=gemini_api_key)

    # --------------------------------------------------
    # 6. Evidence-based research prompt
    # --------------------------------------------------

    prompt = f"""
You are a careful OAuth integration research analyst.

Your task is to create a reliable, evidence-based OAuth setup
guide for {provider}.

Your priority is factual accuracy, not producing a complete-looking
answer.

==================================================
RESEARCH AND EVIDENCE RULES
==================================================

1. Use the supplied research material as the primary evidence.

2. Prioritise official provider documentation for technical
   requirements, OAuth behaviour, permissions and approval rules.

3. A source classified as Third-party Source must never be
   presented as an official provider requirement.

4. Every important technical claim must reference its
   supporting Source ID and URL.

5. Only make a claim if the retrieved source content actually
   supports it. A relevant title or URL alone is not sufficient
   evidence.

6. Do not invent credentials, scopes, URLs, setup steps,
   approval requirements, token lifetimes or security policies.

7. If the available evidence does not establish a fact,
   explicitly state "Not verified from available sources".

8. If sources disagree, explain the disagreement and identify
   which source is official and which is third-party.

9. Do not interpret missing documentation as proof that
   a requirement does not exist.

10. Distinguish between:
    - Internal or private integrations
    - Public OAuth integrations
    - Marketplace distribution or listing
    - Enterprise or organisation-specific installations

==================================================
AUTHENTICATION SYSTEM SEPARATION
==================================================

11. Identify the authentication system described by each source:
    - Regular provider API OAuth
    - MCP OAuth
    - Static API tokens
    - Another authentication mechanism

12. Never combine token expiration, refresh-token behaviour,
    authorization rules or security requirements from
    different authentication systems.

13. If a rule is specific to MCP OAuth, explicitly label it
    "MCP-specific".

14. Never apply MCP token lifetime rules to regular API OAuth,
    or vice versa, without explicit official evidence.

15. If the authentication system associated with a rule
    cannot be established, mark it "Not verified".

==================================================
TOKEN LIFECYCLE
==================================================

16. Check whether the provider documents:
    - Access token expiration
    - Refresh token availability
    - Refresh token expiration
    - Token rotation
    - Reauthorization requirements
    - Revocation behaviour

17. Do not assume all OAuth providers issue refresh tokens.

18. Do not assume access tokens never expire.

19. If exact token lifetimes are not documented in the
    available official sources, say so.

==================================================
SETUP AND APPROVAL
==================================================

20. Distinguish between creating an OAuth application and
    implementing the OAuth authorization flow.

21. Explain whether developers need their own OAuth application
    or can use a managed OAuth solution.

22. Do not claim managed OAuth is available unless the supplied
    evidence supports that claim.

23. Separate the following:
    - Creating an application
    - Configuring credentials
    - Authorizing individual users
    - Provider verification
    - Marketplace submission and review

24. Clearly identify actions that require human interaction,
    such as accepting consent screens, providing business
    information or completing provider review forms.

==================================================
TESTING AND CONFIDENCE
==================================================

25. This research agent has not automatically performed
    an actual OAuth authorization or token exchange.

26. Never claim that a provider integration, OAuth flow,
    callback or API request has been practically tested
    unless that test is explicitly documented in the supplied
    research material.

27. Distinguish:
    - Officially documented
    - Supported by third-party information
    - Practically tested
    - Not verified

28. Do not assign an arbitrary accuracy percentage,
    confidence score or testing status.

==================================================
RESEARCH MATERIAL
==================================================

{research_context}

==================================================
GENERATE THE GUIDE USING THESE SECTIONS
==================================================

1. Whether developers need their own OAuth application.
2. Where to create the OAuth application.
3. Step-by-step setup instructions.
4. Required credentials and OAuth scopes or capabilities.
5. Redirect URI requirements.
6. Approval, verification and marketplace requirements.
7. Common blockers and their solutions.
8. What requires human action.
9. Access-token expiration and refresh-token behaviour.
10. Source audit and verification.
11. Limitations and information that could not be verified.

==================================================
SOURCE AUDIT REQUIREMENTS
==================================================

For every important claim:

- Include its Source ID.
- Include its URL.
- Identify whether the source is official or third-party.
- Explain when evidence is insufficient or conflicting.

At the end, provide:

A. Official sources used.
B. Third-party sources used.
C. Important claims that remain unverified.
D. Practical tests that have not been performed.

Do not describe a source as verified merely because its
domain appears official. Source classification is based
on domain matching and does not independently establish
the accuracy of retrieved content.

Return a clear, structured guide suitable for developers.

Use concise technical language and avoid repeating the
same information across multiple sections.
"""

    # --------------------------------------------------
    # 7. Generate the research report with retry
    # --------------------------------------------------

    response = None

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

            break

        except Exception as error:

            error_message = str(error)

            # Retry only temporary availability errors
            if "503" in error_message or "UNAVAILABLE" in error_message:

                if attempt < 2:

                    wait_time = 10 * (attempt + 1)
                    time.sleep(wait_time)

                else:

                    raise Exception(
                        "Gemini is experiencing high demand. "
                        "Please try again later."
                    )

            else:
                raise

    # Check that Gemini returned a usable response
    if response is None or not response.text:

        raise Exception(
            "Gemini did not return a research report. "
            "Please try again."
        )

    # --------------------------------------------------
    # 8. Return report and source details
    # --------------------------------------------------

    return {
        "report": response.text,
        "sources": sources
    }
