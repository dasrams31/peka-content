# Peka AI - TikTok Developer App Submission Pack

Purpose: register a TikTok developer app so Peka AI's existing content pipeline can
publish to Peka AI's own TikTok account through the official Content Posting API
(full-auto posting, same pattern as the existing Instagram/Threads/Facebook flows).

Prepared: 2026-10-22. Status: assets ready, waiting for the TikTok account to exist
and for the owner to complete the portal steps marked OWNER below.

## Already prepared (done, live)

- Privacy Policy URL: https://peka.ai.id/privacy/ (live, HTTP 200)
- Terms of Service URL: https://peka.ai.id/terms/ (live, HTTP 200)
- Website URL: https://peka.ai.id
- App icon: `app-icon-1024.png` in this folder (1024x1024, mascot P)
- Photo hosting for API PULL_FROM_URL: https://blog.peka.ai.id/images/ (already public)

## OWNER steps (manual, in order)

1. Create the TikTok account first (app): target username @peka.ai.id,
   display name "PekaAI | Informasi Trend AI Terkini", mascot avatar,
   bio "Peka duluan soal AI. Update tools, berita, dan prompt AI tiap hari."
2. On a browser, sign in at https://developers.tiktok.com with that TikTok account
   and accept the developer terms.
3. Create an organization (name: Peka AI) and an app using the field values below.
4. Add the products and scopes below, fill the URLs, then submit for review.
   (Approval of the audit submission is the owner's tap.)

## App profile field values

- App name: Peka AI
- Category: Content / Media publishing tool (pick closest available)
- Description (short): Official publishing tool of Peka AI (peka.ai.id), an
  Indonesian AI news and tools media brand. The app publishes Peka AI's own
  editorial content to Peka AI's own TikTok account.
- Description (long): Peka AI is an Indonesian-language media brand covering AI
  news, tools, prompts, and open-source AI projects, publishing daily on
  Instagram, Threads, Facebook, and blog.peka.ai.id. This app connects our
  existing editorial pipeline to our own TikTok account through the official
  Content Posting API so scheduled posts (photo carousels and videos) can be
  published without manual uploads. The app is used only by the account owner,
  only with Peka AI's own account, and does not provide services to third parties.
- Website URL: https://peka.ai.id
- Privacy Policy URL: https://peka.ai.id/privacy/
- Terms of Service URL: https://peka.ai.id/terms/
- Icon: app-icon-1024.png (this folder)
- Platforms: Web app / server-side integration (no mobile SDK)

## Products and scopes to request

- Login Kit: scope `user.info.basic`
- Content Posting API: scopes `video.publish` and `video.upload`
  (Direct Post). Photo publishing uses the same Content Posting API.

## Audit use-case justification (paste into the review form)

"Peka AI publishes daily AI news, AI tool roundups, prompt tutorials, and
open-source repository spotlights to its own social media accounts. Our TikTok
account is the newest branch of the same editorial operation. We request Direct
Post access so our existing scheduling pipeline can publish our own prepared
photo carousels and videos to our own account at scheduled times, instead of
manual uploads. The integration signs in only with our own account, shows the
platform consent screen, and posts only content we authored. No third-party
accounts, data collection, or user-facing service is involved."

## Audit demo video (record AFTER the sandbox app exists)

Screen recording, roughly 60-90 seconds:
1. Open the integration's authorization page; click "Connect TikTok".
2. TikTok consent screen appears; approve the requested scopes.
3. Choose a prepared photo carousel from the pipeline output folder.
4. Trigger publish; show the API success response with the post ID.
5. Open the TikTok app and show the post live on the @peka.ai.id profile.

## URL prefix verification (for photo PULL_FROM_URL)

- Verify the domain `blog.peka.ai.id` in the app settings (URL properties).
- Photos will be pulled from https://blog.peka.ai.id/images/<file>.png, which the
  blog pipeline already publishes for every edition.

## After approval (integration work, handled by Muse)

- OAuth connect flow for the brand account; token stored server-side (chmod 600),
  never in chat or git.
- Extend the posting crons with a TikTok step (photo mode first, video later),
  using the canonical post URL returned by the API for the blog `links` field.
- Report results in the Peka side chat like the other platforms.
