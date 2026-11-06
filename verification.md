
# OAuthReady – Verification Notes

## 1. GitHub OAuth App

**Status:** Tested  
**Application:** OAuthReady  
**Provider:** GitHub  
**Difficulty:** Easy



## 2. Composio Managed OAuth Research

**Provider:** GitHub

**Composio managed OAuth:** Available

**Source:** https://docs.composio.dev/toolkits/managed-auth

### Finding
Composio already provides a managed GitHub OAuth application.

Developers using Composio do not need to register
their own GitHub OAuth application by default.

### When developers may need their own app
- Custom branding on the consent screen.
- Requesting custom OAuth scopes.
- Getting a separate rate-limit quota.

### Product insight
OAuthReady should clearly tell developers whether
they actually need to create their own OAuth app
before asking them to follow a lengthy setup guide.

**Evidence:** From official Composio documentation.


### What worked
- OAuth app registration was straightforward.
- Client ID generated successfully.
- Client Secret generated successfully.
- Redirect URI configuration was simple.
- Application settings updated successfully.
- No general app approval step was encountered during registration.

### Potential blockers to investigate
- Incorrect Client ID or Client Secret.
- Access token expiration.
- Missing or insufficient OAuth scopes.
- User authorization and organisation access restrictions.
- Private email access permissions.

### Overall assessment

- **Difficulty:** Easy
- **Registration experience:** Smooth.
- **Full OAuth authorization flow:** Not tested yet.
- **Approval wait:** No general approval step encountered during registration.

### What I learned

GitHub makes OAuth application registration relatively easy. 
The bigger challenges may occur during integration, such as 
incorrect credentials, token expiration, missing permissions 
and authorization failures.

### Evidence classification

- **Tested:** Application registration, credential generation 
  and Redirect URI configuration.
- **From docs:** To be researched and verified.
- **Uncertain:** Runtime blockers and full authorization flow 
  have not yet been tested.

### Product decision

OAuthReady will show both managed OAuth and
Bring Your Own OAuth options.

It will first explain whether developers need
their own OAuth app, then provide the relevant
setup instructions and trade-offs.




## 3. Slack OAuth App

**Status:** Tested
**Application:** OAuthReady
**Provider:** Slack
**Difficulty:** Medium (preliminary)

### What worked
- Created a Slack development workspace.
- Registered OAuthReady using Pick Features.
- Selected the bot scope `chat:write`.
- Created the application successfully.
- Authorized the application in our development workspace.
- Installed the app successfully.
- Client ID and Client Secret generated.

### OAuth configuration
- Bot Token Scope: `chat:write`
- User Token Scopes: None
- Bot Events: None
- Workspace Events: None
- Redirect URLs: Not configured yet.

### Important observations
- Slack separates Bot Token Scopes and User Token Scopes.
- Redirect URLs must be configured for OAuth redirect flows.
- Installing an app in your own workspace is different
  from distributing it publicly.
- Slack generates a Bot User OAuth Token after installation.

### Potential blockers to investigate
- Incorrect Client ID or Client Secret.
- Missing OAuth scopes.
- Incorrect redirect URL.
- Workspace installation permissions.
- Public distribution requirements.
- Slack Marketplace review requirements.

### Overall assessment
- Difficulty: Medium (preliminary).
- App creation: Successful.
- Workspace installation: Successful.
- Full OAuth authorization flow: Not tested.
- Public distribution: Not tested.

### Evidence classification
- Tested: App creation, bot scope selection and workspace installation.
- From docs: To be researched and verified.
- Uncertain: Public distribution requirements and approval timelines.


- Public distribution requirement: Slack requires developers to remove hard-coded OAuth tokens and webhook URLs.
- Each installing workspace must authorize the app through OAuth.
- Status: Documented from Slack's Manage Distribution page; not yet verified in our code.

- HTTPS requirement: Slack requires distributed apps to use HTTPS for added security.
- Status: Slack dashboard displays this requirement as complete.
- OAuthReady action: Use HTTPS URLs when deploying and configuring the OAuth flow.


- Marketplace submission: Slack displays five stages:
  1. Your App Listing
  2. Review scopes
  3. Security and compliance
  4. Testing information
  5. Automated checks
- Public distribution is currently not activated.
- Redirect URL and hard-coded information declaration are still pending.
- Marketplace submission was not attempted.




## Google OAuth App

- Status: Tested — OAuth branding and scope configuration completed.
- Initial blocker: Google Cloud required account-level 2-Step Verification (MFA).
- Project: OAuthReady.
- Audience: External.
- Publishing status: Testing.
- Gmail API: Enabled.
- Requested scope: https://www.googleapis.com/auth/gmail.readonly
- Scope classification: Restricted.
- Scope description: View email messages and settings.
- Verification centre: Google displayed that verification is not required while the app is in Testing mode.
- Production consideration: Moving to production may require OAuth verification. Restricted-scope applications may also require an independent security assessment depending on data handling.
- OAuth client credentials: Not created.
- Full OAuth authorization flow: Not tested.
- Evidence: Google Cloud Console tested directly.


## 4. Live Agent Research – Notion

**Status:** Tested – live guide generated successfully.

### What worked
- Entered Notion as an unfamiliar provider.
- Tavily retrieved relevant documentation and supporting sources.
- Gemini generated a structured OAuth research guide.
- Sources were classified into official and third-party references.
- The report distinguished regular OAuth from MCP-related authentication.
- Unverified claims and practical testing limitations were identified.

### What remains uncertain
- The generated guide has not been validated through a complete Notion OAuth flow.
- Token lifecycle details require further confirmation from official documentation.
- Third-party findings should not be treated as definitive provider requirements.

### Assessment
The live research flow successfully demonstrated how OAuthReady can investigate an unfamiliar provider without requiring a pre-written guide.


## 5. Key Corrections and Learnings

- GitHub registration does not mean the complete OAuth integration has been tested.
- Slack workspace installation is different from public distribution and Marketplace listing.
- Google's Testing publishing status does not establish that production verification will be unnecessary.
- Managed OAuth availability must be checked separately for each provider.
- Search results from third-party sources must be distinguished from official provider requirements.
- Hands-on setup time and external approval wait time should be communicated separately.

## 6. Agent vs. Human Responsibilities

### What the agent can do
- Find relevant provider documentation.
- Identify OAuth setup requirements and likely blockers.
- Summarise scopes, redirect URI requirements and approval processes.
- Generate structured setup instructions.
- Highlight uncertain information and provide source links.

### What the developer must do
- Sign in to provider dashboards.
- Create OAuth applications and configure credentials.
- Accept provider terms and permissions.
- Store client secrets securely.
- Complete provider verification or Marketplace submissions.
- Test the actual authorization and token exchange flow.

