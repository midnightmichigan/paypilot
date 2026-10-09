# HUNT-LOG — bounty hunt 2026-10-09

## What was checked
- **Devpost hackathons** (open, cash prizes): via devpost.com/hackathons
  (JS-rendered, read via search-engine cache + per-hackathon rules pages).
- **Kaggle competitions**: skipped this pass — checked standing state only;
  current open cash comps are mostly long-running ML leaderboards that need
  days of GPU tuning, poor fit for a fast AI-builder entry window.
- **Bugcrowd/HackerOne**: noted as a standing lane (responsible disclosure,
  real vulns in scope) but no same-day quick-win scope was identified this
  pass; left for a dedicated audit run.
- **HackerEarth / MLH**: mostly student/in-person circuits; nothing matching
  the $0/remote/solo filters surfaced.

## Ranked top 3 (prize × AI-builder winnability)

### 1. PayPal AI Hackathon — $67,500 — deadline Nov 12, 2026 3:00 PM EST
- URL: https://paypalaihackathon.devpost.com/
- Online, ~10,120 participants, solo allowed, global eligibility.
- Build: app integrating PayPal developer platform (free sandbox) + any AI tool.
- Submit: project + text description + FUNCTIONAL DEMO (run instructions or
  hosted URL — **no video required**). Existing projects allowed with
  meaningful progress during the hackathon window.
- Why #1: biggest prize with the longest runway (34 days), no video
  requirement, free sandbox removes all cost, solo-friendly, and the
  PayPal+AI integration is squarely in an AI builder's wheelhouse.

### 2. Qloo Agentic Hackathon — $25,000 cash — submissions through Oct 30, 2026
- URL: https://qloo.devpost.com/
- Online, ~852 participants, prizes: $15k / $6k / $4k.
- Build: AI agent with "taste" using the Qloo API (recommendations with
  cultural/preference judgment).
- Submit: live hosted demo app + public repo + text description + open-source
  license — **demo videos NOT required** (judges use the app).
- Why #2: smallest participant pool of the big prizes → best odds; no video;
  21 days is enough for one polished agent.

### 3. Life After Code (GitLab) — $45,000 — deadline Oct 27, 2026 9:00 AM EDT
- URL: https://gitlab-transcend.devpost.com/
- Online, ~1,364 participants. Theme: automate what happens after code is
  written (GitLab Duo Agent Platform, CI/CD).
- Submit: text description + public GitLab project (MIT, visible CI/CD
  history) + demo video <3 min on YouTube + (Path B) deployed project live
  until ~Nov 16.
- Why #3: strong prize-to-participant ratio, but the GitLab-platform lock-in
  and mandatory demo video make it heavier than #1/#2. Screen-recorded demo
  with no human on camera satisfies the video rule.

## Skipped (with reasons)
- **Meta VR Start Developer Competition ($1M, Nov 18)** — needs Dakota's Meta
  sign-in + gov photo-ID per his prior deferral. Hard skip.
- **Build, Ship, Shape: Amazon Developer Hackathon ($138k, Oct 23)** —
  ~52,000 participants, Amazon-device tracks; prize/odds ratio worse than #1.
- **AWS CDS Agentic AI Partner Hackathon ($40k, Oct 28)** — requires an AWS
  Partner Central ACE opportunity ID (partner account); likely blocked.
- **Nebius x NVIDIA Global AI Hackathon ($50k+, Oct 30)** — 20,147
  participants; requires Nebius infra + NVIDIA open models.
- **OpenCV AI Competition 2026 ($20,250, Oct 27)** — vision + AWS; doable but
  weaker fit than the top 3.
- **Build With AI: Basics ($2,500, Oct 26)** — SubCut already submitted; no
  duplicate entries.
- **IEEE ClimateChain ($3,000, Oct 25)** / **YouCam API ($6,000, Nov 2)** —
  small prizes relative to effort.
- **IonQ/Qollab quantum 48h sprint (Oct 9–11)** — registration closed Oct 6.
- **Code for a Billion (18 lakh INR, Nov 15)** — India-centric judging homes;
  eligibility risk.

## What was scaffolded (#1 pick)
`~/workspace/bounty-hunts/paypal-ai-hackathon/` — **PayPilot**, an AI invoice
generator for casual sellers:
- `app.py` (stdlib-only server), `ai_parser.py` (LLM + fallback parser),
  `paypal_client.py` (PayPal Invoicing API v2 + labeled mock mode),
  `static/index.html` (UI), `test_flow.py` (all tests passing).
- Real working start, not a stub: end-to-end parse → invoice flow verified in
  mock mode; zero-config for judges; real sandbox path wired behind env vars.

## Next steps (need main-agent / Dakota decisions)
1. Create the free PayPal Developer sandbox app (his standing signup auth
   covers free account creation) and run one real sandbox invoice.
2. Push to public GitHub (midnightmichigan) with an OSI license file.
3. Main-agent review of the entry, then submit on Devpost before Nov 12.
4. Optional parallel: start Qloo (#2) scaffold — 21-day window, smallest pool.
