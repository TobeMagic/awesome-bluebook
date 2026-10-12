#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 fragments 打包成 EPUB3。

用法：
    python tools/build_epub.py

产出：books/deepseek-harness/deepseek-harness-bluebook.epub

要点：
- 正文里的 SVG 图先用无头 Chrome 转成 PNG（EPUB 阅读器对 SVG 支持不齐，
  Kindle 完全不支持，所以包里放位图）；SVG 原件仍在仓库 figures/ 下
- 章节 XHTML 放 OEBPS/text/，图放 OEBPS/images/，md 里的 ../figures/ 相对
  路径正好对得上，只换扩展名
- mimetype 必须第一个进包且不压缩，这是 EPUB 的硬规矩
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import uuid
import xml.etree.ElementTree as ET
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import preview          # noqa: E402
import build_book       # noqa: E402

BOOK = os.path.join(ROOT, "books", "deepseek-harness")
FRAG = os.path.join(BOOK, "fragments")
FIGDIR = os.path.join(BOOK, "figures")
TMP = os.path.join(ROOT, ".tmp", "epub")
PNGCACHE = os.path.join(ROOT, ".tmp", "epub-png")

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

TITLE = "蓝宝书 01 · DeepSeek Harness"
SUBTITLE = "一切皆插件：一个 AI 外壳是怎么长起来的"
AUTHOR = "计算机魔术师"
LANG = "zh-CN"

CSS = """
body{margin:0 1em;line-height:1.85;color:#2C2C2A;
     font-family:'PingFang SC','Microsoft YaHei',sans-serif}
h1{font-size:1.5em;color:#1B3A6B;margin:1em 0 .6em;line-height:1.4}
h2{font-size:1.2em;color:#1B3A6B;margin:1.8em 0 .6em;padding-bottom:.3em;
   border-bottom:1px solid #E3E1D8}
h3{font-size:1.05em;color:#1B3A6B;margin:1.4em 0 .4em}
p{margin:0 0 .9em;text-align:justify}
hr{border:0;border-top:1px solid #E3E1D8;margin:1.6em 0}
ul{padding-left:1.4em;margin:0 0 .9em}
li{margin:.25em 0}
code{font-family:Menlo,Consolas,monospace;font-size:.85em;
     background:#EFEDE6;padding:.1em .3em;border-radius:3px}
pre{background:#FBFAF7;border:1px solid #E3E1D8;border-radius:8px;
    padding:.9em 1em;overflow-x:auto;font-size:.85em}
table{border-collapse:collapse;width:100%;margin:0 0 1em;font-size:.9em}
th,td{border:1px solid #E3E1D8;padding:.45em .6em;text-align:left;vertical-align:top}
th{background:#EDF2F9;color:#1B3A6B;font-weight:600}
figure{margin:1.4em 0;text-align:center}
figure img{max-width:100%;height:auto}
figcaption{font-size:.85em;line-height:1.7;margin-top:.7em;color:#5F5E5A;
           text-align:left}
blockquote{margin:1em 0;padding:.6em 1em;border-left:3px solid #0F6E56;
           background:#F5F0E8;color:#2C2C2A}
blockquote p{margin:0 0 .5em}
blockquote p:last-child{margin:0}
.src{color:#5F5E5A}
.part{font-size:.85em;color:#0F6E56;letter-spacing:.1em;margin:0 0 2em}
.coverpage{text-align:center;margin:0}
.coverpage img{max-width:80%;height:auto;margin:2em auto 1em}
.coverpage h1{font-size:1.8em;margin:.4em 0}
.coverpage .sub{font-size:1.05em;color:#5F5E5A;margin:0 0 3em}
.coverpage .by{font-size:.9em;color:#5F5E5A;letter-spacing:.15em}
"""


# ---------- 图：SVG -> PNG ----------

def svg_size(path: str) -> tuple[int, int]:
    head = open(path, encoding="utf-8").read(1200)
    m = re.search(r'viewBox="0 0 (\d+) (\d+)"', head)
    if m:
        return int(m.group(1)), int(m.group(2))
    return 680, 400


def to_png(svg_name: str) -> str:
    """把 figures/<svg_name> 转成 PNG，返回 PNG 路径（带缓存）。"""
    os.makedirs(PNGCACHE, exist_ok=True)
    png = os.path.join(PNGCACHE, svg_name[:-4] + ".png")
    if os.path.exists(png) and os.path.getsize(png) > 1000:
        return png
    src = os.path.join(FIGDIR, svg_name)
    w, h = svg_size(src)
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         "--force-device-scale-factor=2", "--default-background-color=FFFFFFFF",
         f"--screenshot={png}", f"--window-size={w},{h}",
         "file:///" + src.replace("\\", "/")],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60,
    )
    if not os.path.exists(png):
        raise RuntimeError(f"转 PNG 失败：{svg_name}")
    return png


# ---------- 组装 ----------

def xhtml(title: str, body: str) -> str:
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<!DOCTYPE html>\n'
        '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-CN" lang="zh-CN">\n'
        f'<head><meta charset="utf-8"/><title>{title}</title>'
        '<link rel="stylesheet" type="text/css" href="../style.css"/></head>\n'
        f'<body>\n{body}\n</body>\n</html>\n'
    )


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main() -> None:
    order = build_book.ORDER
    parts = build_book.PARTS

    os.makedirs(os.path.join(TMP, "OEBPS", "text"), exist_ok=True)
    os.makedirs(os.path.join(TMP, "OEBPS", "images"), exist_ok=True)

    spine, manifest, nav_items = [], [], []
    cur_part = None
    used_png = {}

    for idx, fname in enumerate(order, start=1):
        md = open(os.path.join(FRAG, fname), encoding="utf-8").read()

        # 图：../figures/x.svg -> ../images/x.png，并转图
        for svg in set(re.findall(r"\.\./figures/([a-z0-9\-]+\.svg)", md)):
            png_path = to_png(svg)
            dst = os.path.join(TMP, "OEBPS", "images", svg[:-4] + ".png")
            if svg not in used_png:
                with open(png_path, "rb") as a, open(dst, "wb") as b:
                    b.write(a.read())
                used_png[svg] = True
        md = re.sub(r"\.\./figures/([a-z0-9\-]+)\.svg", r"../images/\1.png", md)

        body = preview.render(md, FRAG, inline_svg=False)

        # 章节标题取 md 第一个 h1
        m = re.search(r"^#\s+(.*)$", md, flags=re.M)
        sec_title = m.group(1).strip() if m else fname
        slug = fname[:-3]

        part = parts.get(fname.split("-")[0] if not fname.startswith("appendix")
                         else fname[:-3], "")
        if part.startswith("第") or part.startswith("序") or part.startswith("附录"):
            if part != cur_part:
                cur_part = part
                body = f'<p class="part">{esc(part)}</p>\n' + body

        path = f"text/{slug}.xhtml"
        with open(os.path.join(TMP, "OEBPS", path), "w", encoding="utf-8") as f:
            f.write(xhtml(esc(sec_title), body))

        spine.append((slug, path, sec_title))
        manifest.append((f"x{idx}", path, "application/xhtml+xml"))
        nav_items.append((sec_title, path, part))

    # 图清单
    for i, fn in enumerate(sorted(os.listdir(os.path.join(TMP, "OEBPS", "images"))), start=1):
        manifest.append((f"img{i}", f"images/{fn}", "image/png"))

    # 封面
    cover_jpg = os.path.join(BOOK, "assets", "cover.jpg")
    if os.path.exists(cover_jpg):
        with open(cover_jpg, "rb") as a, open(os.path.join(TMP, "OEBPS", "cover.jpg"), "wb") as b:
            b.write(a.read())
        manifest.append(("cover-image", "cover.jpg", "image/jpeg"))

    # 样式
    with open(os.path.join(TMP, "OEBPS", "style.css"), "w", encoding="utf-8") as f:
        f.write(CSS)
    manifest.append(("css", "style.css", "text/css"))

    # 封面页 + 书名页
    cover_page = (
        '<div class="coverpage">'
        '<img src="cover.jpg" alt="封面"/>'
        f'<h1>{esc(TITLE)}</h1>'
        f'<p class="sub">{esc(SUBTITLE)}</p>'
        f'<p class="by">{esc(AUTHOR)} 著</p>'
        "</div>"
    )
    with open(os.path.join(TMP, "OEBPS", "text", "titlepage.xhtml"), "w", encoding="utf-8") as f:
        f.write(xhtml(esc(TITLE), cover_page))
    manifest.append(("titlepage", "text/titlepage.xhtml", "application/xhtml+xml"))

    # 目录页（人读的）
    toc_rows = []
    last = None
    for t, p, part in nav_items:
        if part and part != last:
            toc_rows.append(f'<h2>{esc(part)}</h2>')
            last = part
        toc_rows.append(f'<p><a href="{p}">{esc(t)}</a></p>')
    with open(os.path.join(TMP, "OEBPS", "text", "toc.xhtml"), "w", encoding="utf-8") as f:
        f.write(xhtml("目录",
                      "<h1>目录</h1>\n" + "\n".join(toc_rows)))
    manifest.append(("toc-page", "text/toc.xhtml", "application/xhtml+xml"))

    # nav.xhtml（机器读的，EPUB3 必需）
    nav_li = []
    last = None
    for t, p, part in nav_items:
        if part and part != last:
            if last is not None:
                nav_li.append("</ol></li>")
            nav_li.append(f"<li><span>{esc(part)}</span><ol>")
            last = part
        nav_li.append(f'<li><a href="{p}">{esc(t)}</a></li>')
    if last is not None:
        nav_li.append("</ol></li>")
    nav_doc = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<!DOCTYPE html>\n'
        '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" '
        'xml:lang="zh-CN" lang="zh-CN">\n'
        '<head><meta charset="utf-8"/><title>目录</title></head>\n'
        '<body><nav epub:type="toc" id="toc"><h1>目录</h1>\n<ol>\n'
        + "\n".join(nav_li) +
        '\n</ol></nav></body>\n</html>\n'
    )
    with open(os.path.join(TMP, "OEBPS", "nav.xhtml"), "w", encoding="utf-8") as f:
        f.write(nav_doc)
    manifest.append(("nav", "nav.xhtml", "application/xhtml+xml+nav"))

    # content.opf
    man = []
    for mid, path, mt in manifest:
        if mt == "application/xhtml+xml+nav":
            man.append(f'<item id="{mid}" href="{path}" media-type="application/xhtml+xml" properties="nav"/>')
        elif mid == "cover-image":
            man.append(f'<item id="{mid}" href="{path}" media-type="{mt}" properties="cover-image"/>')
        else:
            man.append(f'<item id="{mid}" href="{path}" media-type="{mt}"/>')
    sp = ['<itemref idref="titlepage"/>', '<itemref idref="toc-page"/>'] + [
        f'<itemref idref="{mid}"/>' for mid, path, mt in manifest
        if path.startswith("text/") and path not in
        ("text/titlepage.xhtml", "text/toc.xhtml")
    ]
    opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" xmlns:opf="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="pub-id" xml:lang="zh-CN">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>{esc(TITLE)}</dc:title>
    <dc:creator opf:role="aut">{esc(AUTHOR)}</dc:creator>
    <dc:language>{LANG}</dc:language>
    <dc:identifier id="pub-id">urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, 'bluebook-01-deepseek-harness')}</dc:identifier>
    <dc:publisher>蓝宝书</dc:publisher>
    <dc:description>{esc(SUBTITLE)}</dc:description>
    <meta property="dcterms:modified">2026-10-12T00:00:00Z</meta>
    <meta name="cover" content="cover-image"/>
  </metadata>
  <manifest>
{chr(10).join('    ' + m for m in man)}
  </manifest>
  <spine>
{chr(10).join('    ' + s for s in sp)}
  </spine>
  <guide>
    <reference type="cover" title="封面" href="text/titlepage.xhtml"/>
    <reference type="toc" title="目录" href="text/toc.xhtml"/>
  </guide>
</package>
"""
    with open(os.path.join(TMP, "OEBPS", "content.opf"), "w", encoding="utf-8") as f:
        f.write(opf)

    # container.xml + mimetype
    os.makedirs(os.path.join(TMP, "META-INF"), exist_ok=True)
    with open(os.path.join(TMP, "META-INF", "container.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n'
                '<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">\n'
                '  <rootfiles><rootfile full-path="OEBPS/content.opf" '
                'media-type="application/oebps-package+xml"/></rootfiles>\n'
                '</container>\n')
    with open(os.path.join(TMP, "mimetype"), "w", encoding="utf-8") as f:
        f.write("application/epub+zip")

    # 打包
    out = os.path.join(BOOK, "deepseek-harness-bluebook.epub")
    if os.path.exists(out):
        os.remove(out)
    with zipfile.ZipFile(out, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip",
                   compress_type=zipfile.ZIP_STORED)
        z.write(os.path.join(TMP, "META-INF", "container.xml"), "META-INF/container.xml",
                compress_type=zipfile.ZIP_DEFLATED)
        for base, _dirs, files in os.walk(os.path.join(TMP, "OEBPS")):
            for fn in files:
                full = os.path.join(base, fn)
                rel = os.path.relpath(full, TMP).replace("\\", "/")
                z.write(full, rel, compress_type=zipfile.ZIP_DEFLATED)

    # 自检：XML 是否 well-formed
    bad = []
    with zipfile.ZipFile(out) as z:
        names = z.namelist()
        assert names[0] == "mimetype", "mimetype 必须是第一个"
        ET.fromstring(z.read("OEBPS/content.opf"))
        ET.fromstring(z.read("META-INF/container.xml"))
        for nm in names:
            if nm.endswith(".xhtml"):
                try:
                    ET.fromstring(z.read(nm))
                except ET.ParseError as e:
                    bad.append(f"{nm}: {e}")
    print(f"wrote {out}  ({os.path.getsize(out)//1024} KB)")
    print(f"章节 {len(spine)} · 图 {len(used_png)} · 包内文件 {len(names)}")
    if bad:
        print("!! XML 不规范：")
        for b in bad[:10]:
            print("  ", b)


if __name__ == "__main__":
    main()
