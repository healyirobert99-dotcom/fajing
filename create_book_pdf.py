#!/usr/bin/env python3
"""Generate PDF for 《法警·行刑之后》 with cover image and all 8 chapters."""

import os
from fpdf import FPDF

# Paths
WORK_DIR = r"C:\Users\wanyu\WorkBuddy\2026-06-22-08-05-22"
COVER_IMG = r"C:\Users\wanyu\Desktop\c519969b-fb46-4d0c-a583-0c2562822cb9.png"
OUTPUT_PDF = os.path.join(WORK_DIR, "法警·行刑之后.pdf")

# Fonts
FONT_TITLE = r"C:\Windows\Fonts\simhei.ttf"     # 黑体 for titles
FONT_BODY = r"C:\Windows\Fonts\simfang.ttf"       # 仿宋 for body text
FONT_KAITI = r"C:\Windows\Fonts\simkai.ttf"       # 楷体 for quotes
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"        # 微软雅黑粗体

# Book metadata
BOOK_TITLE = "法警·行刑之后"
TAGLINE = "枪响之后，处决才刚刚开始"
AUTHOR = "万澈"

# Chapter data
CHAPTERS = [
    ("第一章", "碰到了", r"第01章-碰到了.md"),
    ("第二章", "才开始", r"第02章-才开始.md"),
    ("第三章", "别放血了", r"第03章-别放血了.md"),
    ("第四章", "影子", r"第04章-影子.md"),
    ("第五章", "不是幻觉", r"第05章-不是幻觉.md"),
    ("第六章", "旧东西", r"第06章-旧东西.md"),
    ("第七章", "出来的不是人", r"第07章-出来的不是人.md"),
    ("第八章", "赵德林的书", r"第08章-赵德林的书.md"),
]

class BookPDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A5')
        self.set_auto_page_break(True, margin=20)
        # Register fonts
        self.add_font("HeiTi", "", FONT_TITLE)
        self.add_font("FangSong", "", FONT_BODY)
        self.add_font("KaiTi", "", FONT_KAITI)
        self.add_font("YaHeiBold", "", FONT_BOLD)
        self.page_count_body = 0

    def header(self):
        if self.page_no() > 1:  # Skip header on cover page
            self.set_font("FangSong", "", 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 8, BOOK_TITLE, align="C")
            self.ln(4)
            # Thin line
            self.set_draw_color(180, 180, 180)
            self.set_line_width(0.2)
            x = self.l_margin
            y = self.get_y()
            self.line(x, y, self.w - self.r_margin, y)
            self.ln(2)

    def footer(self):
        if self.page_no() > 1:
            self.set_y(-15)
            self.set_font("FangSong", "", 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, str(self.page_no() - 1), align="C")

    def add_cover_page(self):
        """Add cover image as first page."""
        if os.path.exists(COVER_IMG):
            self.add_page()
            # Cover image fills the page
            self.image(COVER_IMG, x=0, y=0, w=self.w, h=self.h)
        else:
            # Fallback: text-only cover
            self.add_page()
            self.ln(40)
            self.set_font("HeiTi", "", 28)
            self.set_text_color(200, 40, 40)
            self.cell(0, 15, BOOK_TITLE, align="C")
            self.ln(12)
            self.set_font("KaiTi", "", 14)
            self.set_text_color(100, 100, 100)
            self.cell(0, 10, TAGLINE, align="C")
            self.ln(30)
            self.set_font("FangSong", "", 12)
            self.cell(0, 10, f"{AUTHOR} 作品", align="C")

        # A blank page after cover (like traditional books)
        self.add_page()

    def add_chapter_title(self, number, name):
        """Add a chapter title page/spread."""
        self.add_page()
        self.ln(25)

        # Chapter number
        self.set_font("HeiTi", "", 16)
        self.set_text_color(40, 40, 40)
        self.cell(0, 12, number, align="C")
        self.ln(10)

        # Chapter name - decorative
        self.set_font("HeiTi", "", 26)
        self.set_text_color(20, 20, 20)
        self.cell(0, 18, name, align="C")
        self.ln(16)

        # Decorative line
        self.set_draw_color(60, 60, 60)
        self.set_line_width(0.5)
        mid_x = self.w / 2
        self.line(mid_x - 20, self.get_y(), mid_x + 20, self.get_y())
        self.ln(12)

    def add_body_text(self, text):
        """Add body text in FangSong with proper Chinese formatting."""
        self.set_font("FangSong", "", 11)
        self.set_text_color(30, 30, 30)

        paragraphs = text.strip().split('\n')
        for para in paragraphs:
            para = para.strip()
            if not para:
                self.ln(5)
                continue

            # Handle markdown headers (just skip as text)
            if para.startswith('# '):
                continue

            # Italic lines (scene markers)
            if para.startswith('*') and para.endswith('*'):
                self.set_font("KaiTi", "", 10)
                self.set_text_color(100, 100, 100)
                self.multi_cell(0, 6.5, para.strip('*').strip(), align="C")
                self.set_font("FangSong", "", 11)
                self.set_text_color(30, 30, 30)
                self.ln(3)
                continue

            # Check if this paragraph would overflow - use multi_cell
            # fpdf2 handles word wrapping, but Chinese needs special handling
            self.multi_cell(0, 6.2, para, align="J")
            self.ln(0.5)

    def parse_chapter_file(self, filepath):
        """Read a chapter markdown file and return cleaned text."""
        full_path = os.path.join(WORK_DIR, filepath)
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove the first line (# header) as we use our own title
        lines = content.split('\n')
        # Skip the first # header line, and skip the last italic marker line
        result_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('# ') and not result_lines:
                continue
            # Skip italic status markers at end
            if stripped.startswith('*（') or stripped.startswith('*('):
                continue
            result_lines.append(line)

        return '\n'.join(result_lines).strip()


def main():
    pdf = BookPDF()

    # Add cover
    pdf.add_cover_page()

    # Add each chapter
    for i, (num, name, filename) in enumerate(CHAPTERS):
        print(f"Processing: {num} {name}...")

        # Chapter title page
        pdf.add_chapter_title(num, name)

        # Chapter body
        text = pdf.parse_chapter_file(filename)
        pdf.add_body_text(text)

    # Save
    pdf.output(OUTPUT_PDF)
    print(f"\nPDF saved to: {OUTPUT_PDF}")
    print(f"Total pages: {pdf.pages_count}")


if __name__ == "__main__":
    main()
