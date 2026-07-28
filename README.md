# pmapparel.com

The P&M Apparel website. Plain, fast, static HTML. No build step required: the `site/` folder is the website.

## How it's organized
- `site/` = the actual website (deploy this)
- `build.py` = the generator that creates `site/` (edit content here, then run `python3 build.py`)

## Deploy to Vercel (first time, ~10 minutes)
1. Create a new repository on GitHub (e.g. `pmapparel-site`) and upload this whole folder.
2. Go to vercel.com, log in, click "Add New > Project", and import the GitHub repo.
3. Framework preset: "Other". Set **Output Directory** to `site`. Leave build command empty.
4. Click Deploy. You'll get a preview URL like pmapparel-site.vercel.app.
5. When ready to go live: Vercel > Project > Settings > Domains > add `www.pmapparel.com`, then follow the DNS instructions it shows (two records to change in GoDaddy).

## Editing content later
Small text fix: edit the HTML file directly in `site/`.
Bigger changes: edit `build.py` and re-run `python3 build.py` (or just ask Claude).

## Before launch checklist
- [ ] Paste the four blog posts from the old Google Site into `site/blog/*/index.html`
- [ ] Swap `site/assets/logo-*.png` for SVG exports from Illustrator (filled logo, black and white versions)
- [ ] Add photos (see below)
- [ ] Verify the site in Google Search Console and submit `sitemap.xml`
- [ ] 301-redirect the bare domain (pmapparel.com) to www in GoDaddy / Vercel
- [ ] Update the LinkedIn address to 1100 S 5th St to match everywhere else

## Adding photos
Export web-size JPGs (1600px wide, ~200-400KB) from the Dropbox `Website Assets/Photos 2024` folder into `site/assets/photos/`, then add `<img>` tags where wanted. Good hero/section candidates: press and production shots (PM-07x-09x series), team shots, and Megan's headshot for the About page.
