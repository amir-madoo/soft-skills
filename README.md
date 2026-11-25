# Practical Judgment - Learning Tracker

A separate, lightweight static web app for the curriculum in `content/curriculum.md`. It has no account, backend, analytics, external fonts, or runtime third-party services. Curriculum data is bundled locally in `curriculum.json`; progress is kept separately in this browser's local storage.

## Supplied curriculum structure

The source specifies **15 units**, **five capstones** inside U15, and **zero separately defined lesson records** or named modules. The app presents each supplied unit as its own learning page and each capstone as a separate activity. It does not invent sub-lessons. Unit text, practice, assessment, review prompts, resource references, and the broader guidance are retained from the source. The full source file is included under `content/`.

There are 15 unique unit IDs (`u1`-`u15`) and five unique capstone IDs (`capstone-1`-`capstone-5`). Curriculum internal U-number references are checked at startup. `validate.py` performs a fuller offline data audit.

## Run locally

Service workers and local storage require an HTTP origin; opening `index.html` directly as a `file://` URL is not supported.

1. Install Python 3 if it is not already available.
2. Open a terminal in this `soft-skills-app` folder.
3. Run `python -m http.server 8000`.
4. Open `http://localhost:8000` in a browser.
5. Stop the local server with Ctrl+C when finished.

You can also use any simple static file server. No package installation or build step is needed.

## GitHub Pages publishing

The app uses relative URLs, so it works both at a repository root (`https://account.github.io/`) and a project path (`https://account.github.io/repository/`). The service worker scope and manifest start URL are relative to the app's published directory.

Because this app lives in `soft-skills-app/` to keep it separate from other project files, GitHub Pages needs to publish that folder. To do that with GitHub Actions:

1. Commit/push this folder to a GitHub repository.
2. Copy `deploy/pages.yml` into the repository's `.github/workflows/pages.yml` (create the directories if needed). This adds only the Pages deployment workflow; it does not move or overwrite the app or curriculum.
3. In the repository, open **Settings -> Pages** and set the source to **GitHub Actions**.
4. Push to the configured branch (default workflow branch: `main`) or run the workflow from the **Actions** tab.
5. Open the Pages URL shown in repository settings. If the repository name differs, the project URL is handled by the relative paths.

The workflow uploads only the `soft-skills-app/` directory as the site artifact. It uses GitHub's Pages actions during deployment; the app itself does not call a service at runtime.

## Install on a phone

Publish or serve the app over HTTPS, then open its URL in the phone browser. On Android/Chrome, use the browser menu and choose **Install app** or **Add to Home screen**. On iPhone/iPad Safari, use **Share -> Add to Home Screen**. The app shell and curriculum are cached after the first successful online load. Offline support requires a browser that supports service workers and a secure origin (localhost is also accepted for local development).

## Progress backup and restore

The Dashboard shows your current unit, overall completion, recent activity, and next recommended unit. Navigate with **Dashboard**, **Curriculum**, **Reviews**, **Capstones**, and **Progress / Backup**.

Progress stays in the current browser profile on the current device. It is not synced. In **Progress / Backup**, choose **Export Progress** to download a JSON file containing completion state, notes, answers/reflections, evidence links, feedback, rubric scores, assessment-save state, timestamps, and recent activity. Keep that file somewhere safe.

On the destination browser/device, open the same app and choose **Import Progress**. The app checks the backup's app/schema identifiers, known item IDs, record structure, and activity format before merging records. Unknown curriculum IDs or malformed files are rejected with an explanation. For an item already present, the more recently updated record takes precedence; curriculum data is never replaced by an import.

Clearing site data/browser storage deletes the local copy. Export first if you want to keep it.

## Curriculum maintenance and limitations

`curriculum.json` is the app's read-only content bundle; learner data is stored independently. If the source curriculum changes, regenerate and review `curriculum.json`, update the edition/check metadata as appropriate, and run `python validate.py`. Existing progress uses stable item IDs and remains in the browser. Renaming/removing IDs requires a deliberate migration if existing records should be retained.

The source provides unit-level activities, not separately named lesson sequences. The app therefore offers one focused page per supplied unit, with its content grouped under expandable sections, and separate pages for the five supplied capstones. The app preserves the source's stated boundaries: completion does not guarantee expertise, wealth, or career success. Time-sensitive law, markets, policy, and geopolitics should be refreshed from the dated/authoritative sources named in the curriculum.
