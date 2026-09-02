# The gate: what can be checked, and what cannot

Work top to bottom. Verdict per item: **Met**, **Partly met**, **Not met**, **Cannot check**.

The left column is the honest scope of any automated check. The right column is the reason no skill can hand anyone a quality mark: most of what a formal assessment looks at happens outside the page and over time. It also involves other people.

Numbers in brackets map to the 10 published PIF TICK criteria, so an author who later applies to a scheme can see where their gaps are. The tests themselves are drawn from the NHS digital service manual Standard for creating health content.

---

## A. Checkable from the page itself

### A1. Purpose and need [3]
- The page has one clear job, and the author can state it in a sentence.
- It answers what the reader wants to know, not only what the author wants to say. Test: does it cover the things people actually ask, including the awkward ones (does it hurt, how long off work, what if I do nothing, what does it cost)?
- It does not duplicate an existing page that does the job better. If a national source covers it well, linking is often the better service.

### A2. Evidence [4]
- Every clinical claim is traceable to a named, dated source.
- Every number has a source, a denominator and a date. "1 in 20 people" beats "5%", and both beat "a small number".
- Sources are the right kind: peer-reviewed literature, national guidelines (NICE, SIGN, specialty bodies) or reputable government and international bodies. A competitor's website is not a source. A press release is not a source.
- Uncertainty is stated where it exists. "We do not know" is a legitimate and often necessary sentence.
- Risks and benefits both appear. A page that lists only benefits is not information.
- Every identifier resolves and matches. Run `scripts/verify_refs.py`.
- **The check the script cannot do:** open the source and confirm it says what the sentence claims. A real paper cited for a claim it does not make is the commonest serious failure.

### A3. Plain language and accessibility [6]
- Short sentences, up to about 20 words. Short paragraphs, up to about 3 sentences.
- Every technical term is explained on first use, or replaced.
- Acronyms written out on first use.
- Active voice. "You will need" not "it will be required".
- Frequencies not decimals or percentages where a frequency reads more naturally.
- Meaningful headings and lists, so the page can be scanned.
- Alt text on every image that carries meaning. Captions or transcripts on video and audio.
- Colour is not the only way meaning is conveyed. Links describe where they go, never "click here".
- No metaphors for clinical facts. No vague reassurance ("a good chance") standing in for a number.
- For anything on the web, WCAG 2.2 AA.

### A4. Transparency, legal and conflicts [7]
- The author is named, with their role and credentials.
- The publishing organisation is clear.
- Production date and next review date are on the page, visible to the reader.
- Any sponsorship, funding, commercial relationship or paid placement is declared where the reader will see it, not buried.
- Nothing that would breach the rules on promoting prescription-only medicines to the public.
- No personal data, and no identifiable patient content without documented consent.
- No claim that the page replaces medical advice, and a clear route to a real person.

### A5. Findable and connected [9, partly]
- Plain title that matches what a reader would actually type.
- Links out to the national sources a reader should have, even when those sources are not yours.
- Written so it can be found and understood on a phone.

---

## B. Only the human can attest. Leave these unticked.

Carry these into the output as an unticked list, every time. Never mark one done on the author's behalf, and never let a completed page imply they are satisfied.

### B1. Systems [1]
There is a written, followed method for producing content, with version control and archiving. Not a document that exists, a document that is used. See `references/production-process.md`.

### B2. Training [2]
Whoever writes and checks the content has the skills to do it, and keeps them current. Includes the clinical checker.

### B3. Involving users [5]
Actual patients or members of the public were involved in, or asked about, this content. Asking two people what they did not understand is worth more than any automated score. This is the criterion most often skipped and it is the one that finds the real problems.

### B4. Clinical sign-off [1, 4]
A suitably qualified person has confirmed the content is accurate and safe. If the author is that person, someone else still reads it.

### B5. Feedback [8]
There is a way for readers to say the page is wrong or unclear, someone receives it and it is logged and acted on.

### B6. Review and currency [1]
The review date is diarised, owned by a named person and honoured. A review date that passes silently is worse than none, because it tells the reader the page is current when nobody has looked.

### B7. Impact [10]
Someone knows whether the page is read, and whether it helped. Page views are a weak proxy. Ask the people at the front desk what patients still ring up to ask.

---

## Scoring

Do not produce a percentage or a grade. A score invites the author to publish at 80 percent and invites the reader to trust a number that means nothing.

Report:
- **Gate 0**: passed or not passed.
- **Required** count, that is section A items marked Not met where the failure could mislead a reader.
- What is outstanding in section B.

A page is ready when the Required list is empty and the author has honestly worked through section B. Nobody but the author can say the second part is true.
