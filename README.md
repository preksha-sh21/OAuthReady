# OAuthReady

**Know the steps, the wait and the blockers before you start setting up an OAuth app.**

Live App: https://preksha-integrations.streamlit.app

GitHub Repository: https://github.com/preksha-sh21/OAuthReady

---

## The problem I'm solving

If you're building an AI agent and want your users to connect Gmail, Slack or Notion, you usually have to register an OAuth app with that provider first. Creating the app is often the easy part. The hard part is everything nobody tells you upfront:

- Where do I even start?
- Will this take 10 minutes or 6 weeks of review?
- What will get me blocked? A privacy policy, a verified domain, a security assessment?

Today developers piece this together from scattered docs, forum posts and emails to the provider. OAuthReady tries to give them one clear, shareable guide instead.

## What I learned before building

I set up OAuth apps on three providers myself before writing any code, and that shaped the whole product:

1. **Creating the app takes minutes everywhere. Approval is what's different.** GitHub had no approval step. Slack worked in my own workspace right away but needs extra steps for public distribution. Google worked in testing mode, but a restricted Gmail scope needs verification before production.
2. **Two things decide how hard it gets:** *who* will use the app (just me vs. anyone) and *what data* it asks for (basic profile vs. reading email).
3. **Setup time and approval wait are two different numbers.** "15 minutes of work + weeks of waiting" is very different from "1 hour", so every guide shows them separately.
4. **You can usually start building before approval.** Slack's own workspace and Google's testing mode let developers keep moving while they wait.
5. **An agent can research, but a human has to act.** Logging in, creating the app, copying secrets and submitting for review all need the developer.

I also looked at Composio's managed OAuth directory. When I checked, it listed **127 apps** where Composio provides the OAuth app and **275 apps** where developers must bring their own. Those "bring your own" apps, plus anyone who wants their own app name on the consent screen, custom scopes or their own rate limits, are where developers really get stuck. That's who this tool is for.

## What it does

- **Curated guides** for GitHub (easy), Slack (medium) and Google (hard). I checked these by hand, and they show the full range of difficulty.
- **Live research for any other app.** Type an app name or website and an agent searches the provider's docs and writes a guide on the spot.
- **A clear summary at the top of each guide:** difficulty, hands-on setup time, approval wait, and what you can do vs. what the agent did.
- **A source audit.** Every source is listed and tagged as official (the provider's own domain) or third-party.
- **Download.** Any guide can be exported as Markdown to share with a teammate.

## How the live research works

1. You enter an app the library doesn't cover.
2. **Tavily** searches for that app's OAuth setup, review process and scopes.
3. Results are deduplicated and tagged as official or third-party by domain.
4. **Gemini** reads only those results and writes a structured guide in the same format as the curated ones.
5. The guide is shown next to its sources, so you can check anything that looks off.

## Key decisions

- **Focus on approval and blockers, not just steps.** Steps are easy to find in docs. "How long will this take and what will stop me" is not.
- **Show setup time and approval wait separately**, because mixing them hides the real cost.
- **Hand-check a few guides instead of generating 100 weak ones.** Three providers with different difficulty taught me more than a large unchecked list would.
- **Keep curated guides out of the agent's path.** GitHub, Slack and Google load my checked guides, so they're never overwritten by AI output.
- **Tavily for search, Gemini for writing.** I first tried Gemini's built-in Google Search grounding, but my free key had no quota for it (`429 RESOURCE_EXHAUSTED`). Splitting search and writing fixed this, and it also gives me real URLs to show as sources instead of links the model might make up.
- **Streamlit**, so my time went into the guides rather than frontend code.
- **JSON files for guides**, so the content is separate from the code and easy to review or edit.

## What I tested vs. what comes from docs

| Provider | What I did myself | What I didn't do |
|---|---|---|
| GitHub | Registered an OAuth app. No approval step came up. | Full sign-in and token exchange |
| Slack | Created a workspace and app, added the `chat:write` bot scope, installed it in my own workspace, got a client ID and secret, and reviewed the distribution and HTTPS requirements | Full OAuth flow, public distribution |
| Google | Set up an external app in testing mode with a restricted Gmail scope, and looked into the production verification requirements | Submitting for verification (it can take weeks) |

Everything else in the guides comes from provider docs and is linked in the source audit. Details are in `verification.md`.

## Running it locally

```bash
git clone ADD_YOUR_GITHUB_LINK
cd oauth-guides

python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

Create `.streamlit/secrets.toml` (it's in `.gitignore`, so it never gets committed):

```toml
GEMINI_API_KEY = "your_gemini_api_key"
TAVILY_API_KEY = "your_tavily_api_key"
```

Both have free tiers. Then run:

```bash
python -m streamlit run app.py
```

## Project structure

```text
oauth-guides/
├── .streamlit/secrets.toml   # your keys, not committed
├── guides/
│   ├── github.json
│   ├── slack.json
│   └── google.json
├── app.py                    # Streamlit UI
├── agent.py                  # Tavily search + Gemini guide writing
├── verification.md           # what I checked, corrected, or couldn't verify
├── requirements.txt
└── README.md
```

## Limitations

- It doesn't create OAuth apps for you. It tells you how and what to expect.
- I didn't run full OAuth sign-in and token flows for every provider, or complete any production approval.
- Approval times come from docs and public reports, so treat them as estimates, not promises.
- Official vs. third-party tagging is based on the domain only. It doesn't prove a source is correct.
- Live guides can be incomplete or wrong. That's why sources are always shown, and you should check key steps against the official docs.
- Provider docs change, so a guide can go out of date.
- Free API tiers have rate limits, so heavy use may slow down or fail.

## Security

- API keys live only in Streamlit secrets, never in the code.
- `secrets.toml` and `.env` files are in `.gitignore`.
- No client IDs or secrets from my test apps are included in this repo.

## What I'd do next

- Grow the curated library, starting with the most-used "bring your own OAuth app" providers.
- Check each generated claim against its source automatically, and flag anything unsupported.
- Add a "last checked" date and refresh old guides.
- Let developers report when a guide is wrong, so it improves over time.
