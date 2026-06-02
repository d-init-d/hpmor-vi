# Style Sheet

> **Editorial status (2026-06-01):** All rules below are approved and enforced. Mechanical scan-and-fix scripts must apply them across the entire corpus. Reference convention: bản dịch Harry Potter của Lý Lan (Nhã Nam / NXB Trẻ).

## Voice

### Register
Literary narration with formal tone; conversational dialogue reflecting characters' personalities.

### Formality
High formality in narration; varied formality in dialogue based on character relationships. Harry's interior voice stays analytic-witty; Hermione is precise and slightly rigid (age-appropriate); Quirrell is cold/formal; Dumbledore archaic; Snape clipped; Voldemort grand.

### Sentence Rhythm
Mirror source paragraph length; prefer short sentences for dialogue; allow complex subordination in exposition.

### Genre Constraints
Maintain rationalist tone; preserve scientific references and logical reasoning dialogue; adapt humor to Vietnamese context. HPMOR is a rationalist fanfiction that explores what would happen if Harry was raised by rationalist scientists. The prose balances dense intellectual dialogue with action and plot twists.

---

## Language Conventions

### Dialogue Punctuation
- Use **straight ASCII double quotes** `"` for dialogue in plain-text chapters. (The EPUB renderer also expects straight quotes; the build script escapes them.) Vietnamese guillemets «» are not used in chapter source — keep ASCII.
- Comma or full stop **inside** the closing quote: `"Xin chào,"` not `"Xin chào" ,`.
- **No space before** closing quote. Failures: `, "`, `. "`, `, "` must be auto-fixed.
- Quote nested in dialogue: `'…'` (single quotes) or escape with double inside.

### Titles and Headings
Translate chapter titles; preserve original numbering; translate subtitles but keep series name "Harry Potter". Chapter title appears as first non-empty line of each `ch*-vn.txt` file.

### Names
Keep all Harry Potter character names as-is (following Lý Lan convention from official Vietnamese translations). Transliterate non-Latin names where applicable; keep original forms for established HP names.

### Capitalization (mandatory)
- Generic Vietnamese HP terms are written with **only the first word capitalized** in running prose. **Title-case is a violation.**
  - Hiệu trưởng (NOT Hiệu Trưởng)
  - Biến hình (NOT Biến Hình)
  - Giám ngục (NOT Giám Ngục, NOT Dementor)
  - Thần sáng (NOT Thần Sáng, NOT Auror)
  - Bùa hộ mệnh (NOT Bùa Hộ Mệnh, NOT Patronus)
  - Bàn Trưởng (NOT Bàn Trưởng → keep, NOT Bàn Chính)
  - Chúa tể Hắc ám (NOT Chúa Tể Hắc Ám)
  - Phượng hoàng (NOT Phượng Hoàng)
  - Hiện hình (NOT Hiện Hình)
  - Bộ trưởng (NOT Bộ Trưởng)
  - Hội trưởng (NOT Hội Trưởng)
  - Áo choàng Tàng hình (NOT Áo Choàng Tàng Hình)
  - Thuốc Biến hình (Polyjuice; NOT Thuốc Biến Hình)
  - Tử thần thực tập / Kẻ Ăn Chết (Death Eater) — both forms acceptable

### Terms of Address
- Map "Professor" to "Giáo sư" (lowercase "sư") for academic staff.
- Map "Mr./Mrs." to "Ông/Bà" in formal contexts. **Exception:** "Mr Potter" is preserved **only** when the speaker is Quirrell, Voldemort, or another formal/cold character with deliberate address intent. Do not bulk-rewrite without context check.
- "Madam Pomfrey", "Madam Malkin", "Madam Bones" — keep as "Madam Pomfrey" / "Madam Malkin" / "Madam Bones" per HP canon and Lý Lan convention (no diacritics).
- "Mrs Norris" → "Bà Norris" (per Lý Lan).
- Characters use first-name basis in informal dialogue.

### Numbers, Dates, Units
Use metric units; Arabic numerals for numbers; preserve original dates.

### URL and Time
- **No space inside URLs or times.** Failures: `https: //`, `7: 24`, `2: 56` must be auto-fixed to `https://`, `7:24`, `2:56`.
- Vietnamese full-width colon `：` is not used in URLs or times; ASCII `:` only.

### Citation Conventions
Preserve original citation format; keep URLs unchanged; translate footnote text.

### Footnote and Translator-Note Policy
Translator notes in square brackets marked `[ND]` (Người dịch). Footnotes numbered per chapter. Author's "E. Y.:" notes must be kept verbatim — they are author's voice, not translator's.

---

## Adaptation Rules

### Idioms
Replace with Vietnamese equivalent when natural; paraphrase meaning when no equivalent exists.

### Humor
Preserve comedic timing over literal meaning; adapt wordplay to Vietnamese pun when possible; preserve intellectual jokes. HPMOR parodies (e.g. ch066) need natural Vietnamese humor: "Chúa của Tính Hợp Lý", "Khoa học là Bạn", etc.

### Cultural References
Retain references with brief gloss if obscure; adapt only when completely opaque to Vietnamese readers.

### Metaphors
Preserve source metaphor when comprehensible; adapt vehicle only when source metaphor is dead in Vietnamese culture.

### Repetition
Preserve deliberate rhetorical repetition; vary accidental repetition for naturalness.

### Songs, Poems, and Quoted Material
Provide faithful prose translation; preserve line breaks; do not attempt rhyme.

---

## Mechanical-Scan Mandatory Fixes

| Issue | Pattern | Auto-fix |
|---|---|---|
| Word concatenation | `làkhông`, `córất`, `khôngthực`, `vànguy hiểm`, `thực sựrất` | Insert space between Vietnamese words where the boundary is clearly an error. Skip lines that contain valid English phrases. |
| URL spacing | `https: //`, `http: //` | Replace with `https://`, `http://`. |
| Time spacing | `7: 24`, `2: 56` | Replace with `7:24`, `2:56`. |
| Space before comma/period | `xin chào ,`, `pháp sư .` | Remove space before punctuation. |
| Space inside closing quote | `xin chào" ,` | Move punctuation inside, drop space. |
| English residue | `awkward`, `awkwardness`, `poor Harry`, `Well,`, `Tolkien's wizard`, `SF` (in narrative) | Flag for review; not auto-fixed unless the surrounding context is clearly English bleed. |
| Dementor/Auror/Patronus | in narrative text | Replace with approved Vietnamese per glossary. |
| Hiệu Trưởng / Biến Hình / Thần Sáng | title-case | Normalize to "Hiệu trưởng" / "Biến hình" / "Thần sáng". |
| Bàn Chính | legacy form | Normalize to "Bàn Trưởng". |
| Thuốc Biến Hình (Polyjuice) | wrong cap | Normalize to "Thuốc Biến hình". |

---

## Forbidden Patterns

| Pattern | Reason |
|---------|--------|
| Dementor/Auror/Patronus in narrative | Inconsistent with approved glossary and Lý Lan convention |
| Title-case for HP terms (Hiệu Trưởng, Biến Hình) | Violates Vietnamese capitalization rule |
| Literal translation of English idioms | Incomprehensible to Vietnamese readers |
| Mixing formal/informal register mid-paragraph | Breaks voice consistency |
| Loan words when approved Vietnamese equivalent exists | Glossary mandates target term |
| Over-translation of scientific terms | HPMOR uses them precisely |
| Space before punctuation in dialogue | Wrong typography for Vietnamese |
| `https: //` / `7: 24` | Wrong typography for URLs/times |
| Bulk-rewriting "Mr Potter" → "cậu Potter" without context check | May destroy intentional formal voice (Quirrell, Voldemort) |