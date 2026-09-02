# health-content-check

A free checklist for anyone writing health information for patients or the public.

It does two things. It checks a page you have written and tells you what to fix, with the fixes written out. And it works forwards, as the checklist to write against before you start.

## What this is not

It is not certification. It confers no quality mark, no tick and no badge. It is not run, endorsed or reviewed by the Patient Information Forum or by NHS England.

Certification schemes assess your **production process** over time, not a single page. If you want a mark, apply to the scheme. The `references/production-process.md` template in this skill is the thing such a scheme would actually look at, so filling it in is not wasted either way.

What you can honestly say about content that passes this check: "written to the NHS standard for creating health content", or "self-assessed against the published PIF TICK criteria". Both are true.

## What it is built on

Free, public, self-assessable standards:

- NHS digital service manual, Standard for creating health content, and the writing and health literacy guidance alongside it.
- The 10 published PIF TICK criteria, used as the map of what a formal assessment covers, linked rather than reproduced.
- WCAG 2.2 AA for anything on the web.

These are revised from time to time. The skill links the live pages and states the date it checked.

## Install

Copy the `health-content-check` folder into your skills directory, then ask Claude to check a page. It triggers on phrases like "check this patient information", "is this page clear enough", "health content checklist" or "review my website health content".

## What is in it

```
health-content-check/
├── SKILL.md                            the review and writing workflow
├── references/
│   ├── criteria-gate.md                what can be checked, and what only you can attest
│   ├── improvement-playbook.md         how to fix the twelve common failures
│   └── production-process.md           the one-page method to fill in once
└── scripts/
    └── verify_refs.py                  resolves DOIs and PMIDs, catches invented citations
```

`verify_refs.py` is Python standard library only. It sends an identifier to the public CrossRef and PubMed interfaces and nothing else. No page content, no patient data, no keys.

## The one thing to understand before using it

Most of what makes health information trustworthy cannot be checked by software. Whether a real patient read it and understood it, whether a qualified person confirmed it is safe, whether anyone acts on feedback, whether the review date is honoured: those are people doing things, and the skill deliberately leaves them unticked. It will always hand you a list of items only you can confirm. That list is the point, not an omission.

## Licence and use

MIT. Free to use, copy, adapt and redistribute, including commercially, provided the copyright notice travels with it. No warranty. You remain responsible for what you publish, including anything you publish after this skill has looked at it.

Source, updates and issues: https://github.com/alistairphillips1/health-content-check
