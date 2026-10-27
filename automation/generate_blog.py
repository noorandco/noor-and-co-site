#!/usr/bin/env python3
import datetime as dt
import json, os, re, sys, urllib.error, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOPICS = ROOT / "automation" / "topics.json"
STATE = ROOT / "automation" / "topic_state.json"
POSTS = ROOT / "_posts"
KEY = os.environ.get("GEMINI_API_KEY", "").strip()
MODEL = os.environ.get("GEMINI_MODEL", "").strip() or "gemini-2.5-flash"

def slugify(value):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", value.lower())).strip("-")[:70]

def main():
    if not KEY:
        print("GEMINI_API_KEY is not configured; skipping generation.")
        return 0
    topics = json.loads(TOPICS.read_text(encoding="utf-8"))
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {"next_index": 0}
    if not topics:
        print("No topics configured."); return 0
    idx = int(state.get("next_index", 0)) % len(topics)
    topic = topics[idx]
    today = dt.datetime.now(dt.timezone.utc).date()
    post = POSTS / f"{today.isoformat()}-{slugify(topic['keyword'])}.md"
    if post.exists():
        print(f"{post.name} already exists; no duplicate created."); return 0
    prompt = f"""
You are the careful editorial assistant for Noor & Co., a leather manufacturing business based in Srinagar, Jammu & Kashmir, India.
Topic: {topic['keyword']}
Search intent: {topic['intent']}
Angle: {topic['angle']}

Write an original, practical article for potential retail buyers, retailers, brands and international B2B customers.
Use clear Markdown headings, a short introduction, practical advice/checklist, conclusion and a natural enquiry CTA.
Aim for 900-1300 words only if useful; do not pad. No keyword stuffing.
Never invent Noor & Co. certifications, export history, customers, factory capacity, prices, minimum order quantities, lead times, or material availability. Do not invent statistics, search volumes, citations or competitor claims.
Phrase unverified business details as questions to confirm, not as facts.
First output a line beginning exactly: Meta description: followed by a concise meta description under 160 characters. Then output the article body only. End with an HTML comment reminding the owner to fact-check before reuse. No YAML or code fences.
"""
    payload = {"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"temperature":0.45,"maxOutputTokens":6000}}
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
        data=json.dumps(payload).encode(),
        headers={"Content-Type":"application/json","x-goog-api-key":KEY},
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as res:
            data = json.loads(res.read().decode())
    except urllib.error.HTTPError as exc:
        print(f"Gemini API HTTP {exc.code}: {exc.read().decode(errors='replace')[:1000]}", file=sys.stderr); return 1
    except Exception as exc:
        print(f"Gemini API request failed: {exc}", file=sys.stderr); return 1
    candidates = data.get("candidates", [])
    parts = candidates[0].get("content", {}).get("parts", []) if candidates else []
    text = "\n".join(p.get("text", "") for p in parts).strip()
    if not text:
        print("Gemini returned no text; check model access/quota.", file=sys.stderr); return 1
    lines = text.splitlines()
    meta_line = lines[0].strip()
    meta = meta_line.split(":",1)[1].strip().strip('"') if meta_line.lower().startswith("meta description:") else ""
    if not meta or len(meta) > 180:
        meta = f"Practical guidance on {topic['keyword']}, buyer questions and sourcing considerations."
    body = "\n".join(lines[1:]).strip() if meta_line.lower().startswith("meta description:") else text
    title = topic["angle"].replace('"', "'")
    front = f'---\nlayout: post\ntitle: "{title}"\ndate: {today.isoformat()} 09:00:00 +0530\ndescription: "{meta.replace(chr(34), chr(39))}"\ncategories: [leather-guides]\n---\n\n'
    POSTS.mkdir(parents=True, exist_ok=True)
    post.write_text(front + body + "\n", encoding="utf-8")
    state["next_index"] = (idx + 1) % len(topics)
    STATE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {post.relative_to(ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
