# Retailworld Google review templates

Three reusable Google review formats in the approved Retailworld social style (Poppins, #F27C10 at full vibrancy, white and light grey, no em dashes, reviewer's name always left off). Sample content is Dean's review, which is already approved for social.

| Template | File | Output | Concept |
|---|---|---|---|
| Reel | `review_reel.html` | 1080 x 1920 MP4, 14s, logo on first and last scenes | "Ding." A lock-screen notification lands, the review opens as chat bubbles with highlighted phrases, then an orange CTA scene. |
| Static post | `review_static.html` | 1080 x 1350 PNG, no logo | "They said it. Not us." on orange, with a tilted white Google review card. |
| Animated grid post | `review_grid.html` | 1080 x 1350 MP4, seamless 8s loop, no logo | "Five stars. No notes." Stars fill one by one, the quote highlight sweeps in, then it eases back for a clean loop. |

## Reusing a template

1. Get the reviewer's OK to share the review publicly.
2. Open the HTML file and edit only the `EDIT ME` block: recruiter name, the quote lines, and the CTA word (reel only).
3. Wrap one phrase per line in `{curly braces}` to give it the orange highlight.
4. Render from this folder (needs Python 3, Playwright with Chromium, and ffmpeg):

```
python3 render.py review_reel.html out/reel.mp4
STILL_ONLY=1 python3 render_post.py review_static.html out/static.mp4    # writes out/static.png
python3 render_post.py review_grid.html out/grid.mp4 4                   # writes out/grid.mp4 + still
```

Add `2.6,9.6,13.5` after the reel command to save preview frames at those seconds instead of rendering the video.

Length guide: reel bubbles 2 or 3 lines, each under about 20 words. Static hook 12 words max, supporting line 25 words max. Grid quote 15 words max.

## Captions (5 hashtags each)

**Reel: Ding.**
> Ding. New review just landed. ⭐⭐⭐⭐⭐
>
> "Dean was absolutely my hype man through all this."
>
> Great advice, friendly service and 10/10 communication. Want someone like that in your corner? Comment HYPE and we'll be in touch.
>
> #RetailworldResourcing #GoogleReview #RetailJobs #RetailCareers #RetailRecruitment

**Static: They said it. Not us.**
> They said it. Not us. 🧡
>
> A real Google review about Dean, from a candidate who landed their new role.
>
> Looking for your next move in retail? Link in bio.
>
> #RetailworldResourcing #GoogleReview #RetailJobs #RetailCareers #NowHiring

**Animated grid: Five stars. No notes.**
> Five stars. No notes. ⭐
>
> This is what having a recruiter in your corner looks like. Store, area and head office roles across Australia and New Zealand.
>
> Tag someone who needs a hype man.
>
> #RetailworldResourcing #GoogleReview #RetailJobs #RetailCareers #RetailRecruitment

## Publishing

For Buffer, commit the finished files to `automationRWR/retailworld-social-assets` and use the raw URL. Reel and animated grid post go in as type `reel`, the static as type `post`. Add alt text to the static.
