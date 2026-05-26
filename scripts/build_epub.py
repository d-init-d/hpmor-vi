#!/usr/bin/env python3
"""Build the Vietnamese HPMOR EPUB from clean chapter text files."""

from __future__ import annotations

import argparse
import html
import re
import shutil
import sys
import tempfile
import uuid
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
CHAPTER_DIR = ROOT / "text" / "chapters"
COVER_PATH = ROOT / "assets" / "cover.jpg"
DEFAULT_OUTPUT = ROOT / "dist" / "hpmor-vi.epub"

BOOK_TITLE_VI = "Harry Potter và Phương pháp Tư duy Duy lý"
CREATOR = "Eliezer Yudkowsky"
TRANSLATOR = "d-init-d, with the D Transcreate workflow"
LANGUAGE = "vi"
SOURCE_REPOSITORY = "https://github.com/rrthomas/hpmor"
WORKFLOW_REPOSITORY = "https://github.com/d-init-d/d-transcreate-skill"
PROJECT_REPOSITORY = "https://github.com/d-init-d/hpmor-vi"


@dataclass(frozen=True)
class Chapter:
    index: int
    source_path: Path
    href: str
    nav_label: str
    title: str
    body_blocks: list[str]


def normalize_heading(raw: str, fallback: str) -> str:
    heading = raw.strip()
    heading = re.sub(r"^#+\s*", "", heading)
    heading = heading.strip()
    return heading or fallback


def chapter_index(path: Path) -> int:
    match = re.fullmatch(r"ch(\d+)-vn\.txt", path.name)
    if not match:
        raise ValueError(f"Unexpected chapter filename: {path.name}")
    return int(match.group(1))


def read_chapter(path: Path) -> Chapter:
    index = chapter_index(path)
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")

    first_non_empty = next((line for line in lines if line.strip()), "")
    title = normalize_heading(first_non_empty, f"Muc {index:03d}")

    body_lines: list[str] = []
    skipped_heading = False
    for line in lines:
        if not skipped_heading and line.strip() == first_non_empty.strip():
            skipped_heading = True
            continue
        body_lines.append(line)

    blocks: list[str] = []
    current: list[str] = []
    for line in body_lines:
        stripped = line.strip()
        if not stripped:
            if current:
                blocks.append(" ".join(current).strip())
                current = []
            continue
        if stripped in {"*", "* * *", "---", "***"}:
            if current:
                blocks.append(" ".join(current).strip())
                current = []
            blocks.append(stripped)
            continue
        current.append(stripped)
    if current:
        blocks.append(" ".join(current).strip())

    nav_label = f"{index:03d}. {title}"
    return Chapter(
        index=index,
        source_path=path,
        href=f"text/chapter-{index:03d}.xhtml",
        nav_label=nav_label,
        title=title,
        body_blocks=blocks,
    )


def discover_chapters() -> list[Chapter]:
    paths = sorted(CHAPTER_DIR.glob("ch*-vn.txt"), key=chapter_index)
    if not paths:
        raise FileNotFoundError(f"No chapter text files found in {CHAPTER_DIR}")
    chapters = [read_chapter(path) for path in paths]
    expected = list(range(1, len(chapters) + 1))
    actual = [chapter.index for chapter in chapters]
    if actual != expected:
        raise ValueError(f"Chapter sequence is not contiguous: expected {expected[:3]}..., got {actual[:3]}...")
    return chapters


def xhtml_document(title: str, body: str, extra_head: str = "") -> str:
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="vi" lang="vi">
<head>
  <meta charset="utf-8"/>
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" type="text/css" href="../styles/book.css"/>
  {extra_head}
</head>
<body>
{body}
</body>
</html>
"""


def render_block(block: str) -> str:
    if block in {"*", "* * *", "---", "***"}:
        return '    <div class="scene-break" aria-label="Ngat canh">* * *</div>'

    escaped = html.escape(block)
    if len(block) >= 2 and block.startswith("*") and block.endswith("*"):
        inner = html.escape(block[1:-1].strip())
        return f'    <p class="note"><em>{inner}</em></p>'

    if re.fullmatch(r"\[[-—].*[-—]\]", block):
        return f'    <p class="chapter-end">{escaped}</p>'

    return f"    <p>{escaped}</p>"


def render_chapter(chapter: Chapter) -> str:
    body = [
        '  <section epub:type="chapter" class="chapter">',
        f"    <h1>{html.escape(chapter.title)}</h1>",
    ]
    body.extend(render_block(block) for block in chapter.body_blocks)
    body.append("  </section>")
    return xhtml_document(chapter.title, "\n".join(body))


def render_title_page() -> str:
    body = f"""
  <section epub:type="titlepage" class="title-page">
    <h1>{html.escape(BOOK_TITLE_VI)}</h1>
    <p class="subtitle">Bản dịch tiếng Việt không chính thức</p>
    <p class="byline">Nguyên tác: {html.escape(CREATOR)}</p>
    <p class="byline">Bản dịch và đóng gói: d-init-d</p>
    <p class="byline">Workflow: D Transcreate Skill</p>
  </section>
"""
    return xhtml_document(BOOK_TITLE_VI, body)


def render_cover_page() -> str:
    body = """
  <section epub:type="cover" class="cover-page">
    <img src="../images/cover.jpg" alt="Book cover"/>
  </section>
"""
    return xhtml_document("Cover", body)


def render_credits_page() -> str:
    body = f"""
  <section epub:type="frontmatter acknowledgments" class="credits">
    <h1>Ghi công</h1>
    <p>Bản dịch tiếng Việt này là một dự án cộng đồng không chính thức dựa trên <em>Harry Potter and the Methods of Rationality</em> của {html.escape(CREATOR)}.</p>
    <p>Ấn bản nguồn để đối chiếu và cấu trúc sách được ghi công cho repository <a href="{SOURCE_REPOSITORY}">rrthomas/hpmor</a>.</p>
    <p>Quy trình dịch và kiểm soát chất lượng sử dụng <a href="{WORKFLOW_REPOSITORY}">D Transcreate Skill</a>: lập brief, source map, glossary, style sheet, story bible, chunk manifest và QA report trước khi đóng EPUB.</p>
    <p>Cover art gốc được ghi công cho Bogdan Butnaru theo thông tin từ HPMOR.com.</p>
    <p>Dự án này không liên kết với J. K. Rowling, Warner Bros., Eliezer Yudkowsky, HPMOR.com hay repository nguồn.</p>
  </section>
"""
    return xhtml_document("Ghi công", body)


def render_qa_note() -> str:
    body = """
  <section epub:type="frontmatter" class="qa-note">
    <h1>Ghi chú chất lượng</h1>
    <p>Bản EPUB này được đóng từ corpus tiếng Việt trong thư mục <code>text/chapters/</code>. Corpus đã qua kiểm tra hoàn chỉnh cấu trúc: đủ 126 tệp chương, không còn blocker thiếu chương nghiêm trọng.</p>
    <p>Đây là bản release candidate. Báo cáo QA trong repository vẫn giữ các caveat về độ mượt văn chương, tính nhất quán thuật ngữ và nhu cầu đọc soát cuối bởi biên tập viên con người.</p>
    <p>Người đọc và người review có thể kiểm chứng quy trình qua thư mục <code>workflow/</code> và tái tạo EPUB bằng <code>python scripts/build_epub.py --check</code>.</p>
  </section>
"""
    return xhtml_document("Ghi chú chất lượng", body)


def render_nav(chapters: list[Chapter]) -> str:
    chapter_items = "\n".join(
        f'      <li><a href="{chapter.href}">{html.escape(chapter.nav_label)}</a></li>'
        for chapter in chapters
    )
    body = f"""
  <nav epub:type="toc" id="toc">
    <h1>Mục lục</h1>
    <ol>
      <li><a href="frontmatter/title.xhtml">Trang nhan đề</a></li>
      <li><a href="frontmatter/credits.xhtml">Ghi công</a></li>
      <li><a href="frontmatter/qa-note.xhtml">Ghi chú chất lượng</a></li>
{chapter_items}
    </ol>
  </nav>
  <nav epub:type="landmarks" hidden="hidden">
    <h2>Landmarks</h2>
    <ol>
      <li><a epub:type="cover" href="frontmatter/cover.xhtml">Cover</a></li>
      <li><a epub:type="titlepage" href="frontmatter/title.xhtml">Title Page</a></li>
      <li><a epub:type="toc" href="nav.xhtml">Table of Contents</a></li>
      <li><a epub:type="bodymatter" href="{chapters[0].href}">Start</a></li>
    </ol>
  </nav>
"""
    return xhtml_document("Mục lục", body, extra_head="")


def render_ncx(chapters: list[Chapter], uid: str) -> str:
    points: list[str] = []
    play_order = 1
    fixed_entries = [
        ("title", "Trang nhan đề", "frontmatter/title.xhtml"),
        ("credits", "Ghi công", "frontmatter/credits.xhtml"),
        ("qa-note", "Ghi chú chất lượng", "frontmatter/qa-note.xhtml"),
    ]
    for item_id, label, href in fixed_entries:
        points.append(
            f"""    <navPoint id="{item_id}" playOrder="{play_order}">
      <navLabel><text>{html.escape(label)}</text></navLabel>
      <content src="{href}"/>
    </navPoint>"""
        )
        play_order += 1
    for chapter in chapters:
        points.append(
            f"""    <navPoint id="chapter-{chapter.index:03d}" playOrder="{play_order}">
      <navLabel><text>{html.escape(chapter.nav_label)}</text></navLabel>
      <content src="{chapter.href}"/>
    </navPoint>"""
        )
        play_order += 1

    return f"""<?xml version="1.0" encoding="utf-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="{uid}"/>
    <meta name="dtb:depth" content="1"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle><text>{html.escape(BOOK_TITLE_VI)}</text></docTitle>
  <navMap>
{chr(10).join(points)}
  </navMap>
</ncx>
"""


def render_css() -> str:
    return """
@namespace epub "http://www.idpf.org/2007/ops";

html {
  -webkit-hyphens: auto;
  hyphens: auto;
}

body {
  color: #1f1f1f;
  font-family: "Literata", "Georgia", "Times New Roman", serif;
  font-size: 1em;
  line-height: 1.58;
  margin: 0;
  padding: 0 6%;
}

a {
  color: #315f8f;
}

.cover-page {
  margin: 0;
  padding: 0;
  text-align: center;
}

.cover-page img {
  display: block;
  height: auto;
  margin: 0 auto;
  max-height: 100vh;
  max-width: 100%;
}

.title-page {
  min-height: 90vh;
  padding-top: 20vh;
  text-align: center;
}

.title-page h1 {
  font-size: 2.1em;
  line-height: 1.18;
  margin: 0 0 1.4em;
}

.subtitle,
.byline {
  margin: 0.45em 0;
  text-indent: 0;
}

.credits,
.qa-note,
.chapter {
  break-before: page;
  page-break-before: always;
}

h1 {
  break-after: avoid;
  color: #111;
  font-size: 1.55em;
  font-weight: 700;
  line-height: 1.25;
  margin: 2.2em 0 1.2em;
  text-align: center;
}

p {
  margin: 0;
  orphans: 2;
  text-align: justify;
  text-indent: 1.35em;
  widows: 2;
}

h1 + p,
.scene-break + p,
.note,
.chapter-end,
.credits p,
.qa-note p {
  text-indent: 0;
}

.credits p,
.qa-note p {
  margin: 0 0 0.9em;
  text-align: left;
}

.note {
  font-style: italic;
  margin: 0 0 0.9em;
  text-align: left;
}

.scene-break {
  break-inside: avoid;
  margin: 1.8em 0;
  text-align: center;
  text-indent: 0;
}

.chapter-end {
  font-variant: small-caps;
  margin-top: 2em;
  text-align: center;
}

code {
  font-family: "Consolas", "Menlo", monospace;
  font-size: 0.9em;
}

nav[epub|type~="toc"] ol {
  list-style-type: none;
  margin: 0;
  padding: 0;
}

nav[epub|type~="toc"] li {
  margin: 0.42em 0;
}
""".strip() + "\n"


def render_opf(chapters: list[Chapter], uid: str, modified: str) -> str:
    items: list[tuple[str, str, str, str]] = [
        ("nav", "nav.xhtml", "application/xhtml+xml", "nav"),
        ("ncx", "toc.ncx", "application/x-dtbncx+xml", ""),
        ("style", "styles/book.css", "text/css", ""),
        ("cover-image", "images/cover.jpg", "image/jpeg", "cover-image"),
        ("cover", "frontmatter/cover.xhtml", "application/xhtml+xml", ""),
        ("title-page", "frontmatter/title.xhtml", "application/xhtml+xml", ""),
        ("credits", "frontmatter/credits.xhtml", "application/xhtml+xml", ""),
        ("qa-note", "frontmatter/qa-note.xhtml", "application/xhtml+xml", ""),
    ]
    items.extend(
        (f"chapter-{chapter.index:03d}", chapter.href, "application/xhtml+xml", "")
        for chapter in chapters
    )

    manifest = "\n".join(
        f'    <item id="{item_id}" href="{href}" media-type="{mt}"{f" properties=\"{props}\"" if props else ""}/>'
        for item_id, href, mt, props in items
    )
    spine_items = [
        "cover",
        "title-page",
        "credits",
        "qa-note",
        *[f"chapter-{chapter.index:03d}" for chapter in chapters],
    ]
    spine = "\n".join(f'    <itemref idref="{item_id}"/>' for item_id in spine_items)

    return f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id" prefix="dc: http://purl.org/dc/elements/1.1/">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="book-id">urn:uuid:{uid}</dc:identifier>
    <dc:title>{html.escape(BOOK_TITLE_VI)}</dc:title>
    <dc:language>{LANGUAGE}</dc:language>
    <dc:creator id="creator">{html.escape(CREATOR)}</dc:creator>
    <dc:contributor id="translator">{html.escape(TRANSLATOR)}</dc:contributor>
    <dc:publisher>d-init-d</dc:publisher>
    <dc:source>{SOURCE_REPOSITORY}</dc:source>
    <dc:relation>{WORKFLOW_REPOSITORY}</dc:relation>
    <dc:relation>{PROJECT_REPOSITORY}</dc:relation>
    <dc:description>Unofficial Vietnamese translation release candidate of Harry Potter and the Methods of Rationality, packaged from auditable D Transcreate workflow artifacts.</dc:description>
    <dc:rights>Original story by Eliezer Yudkowsky. Source EPUB/LaTeX edition credited to rrthomas/hpmor. Vietnamese translation packaged for non-commercial fan/community review.</dc:rights>
    <meta property="dcterms:modified">{modified}</meta>
    <meta name="cover" content="cover-image"/>
  </metadata>
  <manifest>
{manifest}
  </manifest>
  <spine toc="ncx">
{spine}
  </spine>
</package>
"""


def write_epub(output_path: Path) -> None:
    if not COVER_PATH.exists():
        raise FileNotFoundError(f"Missing cover image: {COVER_PATH}")

    chapters = discover_chapters()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    uid = str(uuid.uuid5(uuid.NAMESPACE_URL, PROJECT_REPOSITORY))
    modified = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    with tempfile.TemporaryDirectory(prefix="hpmor-vi-epub-") as tmp:
        epub_root = Path(tmp)
        (epub_root / "META-INF").mkdir()
        (epub_root / "OEBPS" / "frontmatter").mkdir(parents=True)
        (epub_root / "OEBPS" / "images").mkdir()
        (epub_root / "OEBPS" / "styles").mkdir()
        (epub_root / "OEBPS" / "text").mkdir()

        (epub_root / "mimetype").write_text("application/epub+zip", encoding="ascii", newline="")
        (epub_root / "META-INF" / "container.xml").write_text(
            """<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
""",
            encoding="utf-8",
        )

        shutil.copyfile(COVER_PATH, epub_root / "OEBPS" / "images" / "cover.jpg")
        (epub_root / "OEBPS" / "styles" / "book.css").write_text(render_css(), encoding="utf-8")
        (epub_root / "OEBPS" / "frontmatter" / "cover.xhtml").write_text(render_cover_page(), encoding="utf-8")
        (epub_root / "OEBPS" / "frontmatter" / "title.xhtml").write_text(render_title_page(), encoding="utf-8")
        (epub_root / "OEBPS" / "frontmatter" / "credits.xhtml").write_text(render_credits_page(), encoding="utf-8")
        (epub_root / "OEBPS" / "frontmatter" / "qa-note.xhtml").write_text(render_qa_note(), encoding="utf-8")
        (epub_root / "OEBPS" / "nav.xhtml").write_text(render_nav(chapters), encoding="utf-8")
        (epub_root / "OEBPS" / "toc.ncx").write_text(render_ncx(chapters, uid), encoding="utf-8")
        (epub_root / "OEBPS" / "content.opf").write_text(render_opf(chapters, uid, modified), encoding="utf-8")

        for chapter in chapters:
            target = epub_root / "OEBPS" / chapter.href
            target.write_text(render_chapter(chapter), encoding="utf-8")

        if output_path.exists():
            output_path.unlink()
        with zipfile.ZipFile(output_path, "w") as zf:
            zf.write(epub_root / "mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
            for path in sorted(epub_root.rglob("*")):
                if path.is_dir() or path.name == "mimetype":
                    continue
                archive_name = path.relative_to(epub_root).as_posix()
                zf.write(path, archive_name, compress_type=zipfile.ZIP_DEFLATED)


def check_epub(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(path)

    with zipfile.ZipFile(path) as zf:
        bad = zf.testzip()
        if bad is not None:
            raise ValueError(f"Corrupt ZIP member: {bad}")
        names = zf.namelist()
        if not names or names[0] != "mimetype":
            raise ValueError("EPUB mimetype must be the first ZIP member")
        if zf.read("mimetype") != b"application/epub+zip":
            raise ValueError("Invalid mimetype payload")
        required = {
            "META-INF/container.xml",
            "OEBPS/content.opf",
            "OEBPS/nav.xhtml",
            "OEBPS/toc.ncx",
            "OEBPS/styles/book.css",
            "OEBPS/images/cover.jpg",
        }
        missing = required.difference(names)
        if missing:
            raise ValueError(f"Missing required EPUB files: {sorted(missing)}")

        for xml_name in [
            "META-INF/container.xml",
            "OEBPS/content.opf",
            "OEBPS/nav.xhtml",
            "OEBPS/toc.ncx",
            *[name for name in names if name.startswith("OEBPS/text/") and name.endswith(".xhtml")],
        ]:
            ElementTree.fromstring(zf.read(xml_name))

        chapter_count = len([name for name in names if name.startswith("OEBPS/text/chapter-") and name.endswith(".xhtml")])
        source_count = len(list(CHAPTER_DIR.glob("ch*-vn.txt")))
        if chapter_count != source_count:
            raise ValueError(f"EPUB chapter count {chapter_count} != source chapter count {source_count}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the Vietnamese HPMOR EPUB.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Output EPUB path.")
    parser.add_argument("--check", action="store_true", help="Validate the generated EPUB structure after building.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    write_epub(args.output)
    if args.check:
        check_epub(args.output)
    display_path = args.output
    try:
        display_path = args.output.relative_to(ROOT)
    except ValueError:
        pass
    print(f"Built {display_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
