# Noor & Co. automated website

Responsive Jekyll website for GitHub Pages, with GA4, Search Console verification, Google Forms/WhatsApp lead capture, and weekly Gemini API blog generation.

## 1. Configure the site
Edit `_config.yml`:
- `url`: `https://YOUR-GITHUB-USERNAME.github.io`
- `google_analytics_id`: your GA4 Measurement ID beginning `G-`
- `google_site_verification`: the token from Search Console's HTML-tag verification method
- `google_form_url`: public Google Form URL
- `google_form_embed_url`: optional Google Form embed URL
- `whatsapp_number`: business number in international digits-only format, e.g. `919876543210`
- `email`: public business email, if desired

Never put your API key in `_config.yml` or any committed file.

## 2. Publish with GitHub Pages
1. Create a **public** GitHub repository named `noor-and-co-site` (GitHub Free Pages supports public repositories).
2. Upload the *contents* of this ZIP to the repository root, including hidden `.github` folder.
3. Edit `_config.yml` and replace the placeholders, then commit.
4. Repository → **Settings → Pages → Build and deployment → Source → GitHub Actions**.
5. Repository → **Settings → Secrets and variables → Actions → New repository secret**:
   - Name: `GEMINI_API_KEY`
   - Value: your rotated Gemini API key (do not share it in chat).
6. Under Actions variables, optionally add `GEMINI_MODEL` with a model enabled for your AI Studio project, e.g. `gemini-2.5-flash`. If omitted, the workflow tries `gemini-2.5-flash` by default.
7. Open **Actions → Noor & Co Website → Run workflow**. The first run deploys the site. Find the URL under Settings → Pages; usually `https://USERNAME.github.io/noor-and-co-site/`.

## 3. Automatic blogs
The workflow runs every Monday at 03:30 UTC (about 09:00 India time; GitHub may delay scheduled jobs). It asks Gemini for one article, writes it into `_posts`, commits it, builds the site, and deploys in the same run. You can also use Actions → Run workflow and select `Generate a new blog post`.

API access and quotas are separate from Gemini Pro. This automation makes API calls only through your configured Gemini API free-tier project. If your project has no free quota/model access, the workflow will fail rather than intentionally use a paid service. Check current usage in Google AI Studio.

## 4. Before launch
- Replace the two SVG illustration placeholders with real product and workshop photographs. Keep the filenames or update the page references.
- Add only products you actually make.
- Verify all business facts. Do not claim unverified certifications, MOQs, prices, capacity, export history or delivery dates.
- Create a Google Form and add its links to `_config.yml`.
- Add your GA4 Measurement ID and test Reports → Realtime.
- Add the *new GitHub Pages URL* as a URL-prefix property in Search Console. Your old Google Sites HTML file verification does not automatically verify this new site. Use HTML-tag verification and copy its token into `_config.yml`, then commit and click Verify.
- This ZIP creates a separate new website; it does not migrate your existing Google Site.
- GitHub Pages is public. Do not commit private data, credentials or customer information.

## Cost notes
GitHub Pages and Actions can be free within GitHub Free limits for public repositories. Gemini API usage may be free within the active AI Studio quota; the Gemini Pro subscription does not itself guarantee free API calls. A custom domain costs extra. The first version uses your own photos, not automatic image generation.
