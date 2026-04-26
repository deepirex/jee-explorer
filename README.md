# JEE 2026 Cutoff Explorer

Free, no-signup tool for JEE 2026 aspirants to find realistic college options based on official CSAB 2025 and JoSAA 2025 closing ranks.

## Features

- Enter rank + home state + category + gender + exam (Mains/Advanced)
- See reachable options across 23 IITs, 31 NITs, 26 IIITs, 41 GFTIs
- Reach / Target / Safe classification by margin
- Filter by branch, quota, institute type
- Toggle between JoSAA and CSAB sources
- Inputs persist in localStorage (no server, no tracking)

## Stack

Pure static HTML + vanilla JS. No build step. No dependencies. Deploy anywhere that serves static files.

## Files

- `index.html` — single-page app
- `data.json` — closing-rank dataset (5,743 rows from CSAB 2025 + JoSAA 2025)
- `robots.txt` — allow indexing

## Local development

```bash
python3 -m http.server 8000
open http://localhost:8000
```

## Deploy to Cloudflare Pages

1. Push this folder to a new GitHub repository.
2. Go to https://dash.cloudflare.com → Workers & Pages → Create → Pages → Connect to Git.
3. Select the repo. Build settings:
   - Build command: *(leave empty)*
   - Build output directory: `/`
4. Deploy. You'll get a `*.pages.dev` URL within ~30 seconds.
5. (Optional) Add a custom domain under the Pages project settings.

## Updating cutoff data

When new JoSAA / CSAB rounds publish:

1. Download the official OR/CR CSV from josaa.nic.in or csab.nic.in.
2. Save to the project root with the same column structure as `2025`.
3. Re-run the dataset builder script (see `build_dataset.py` in `/Downloads/`).
4. Commit the updated `data.json` and push.

## Disclaimer

This tool uses publicly-available historical cutoff data. It is not affiliated with NTA, JoSAA, CSAB, or any institute. 2025 closing ranks are a guide, not a guarantee for 2026. Always verify final cutoffs on official sources before locking choices.

## License

Free to use for personal college planning. Data is public.
