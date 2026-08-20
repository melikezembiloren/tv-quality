"""
Günlük kalite kontrol listesinin resmi PDF raporu.

Bu, saf bir sunum (Presentation) katmanı endişesi — çıktı formatını değiştiriyor
(JSON yerine PDF), iş kuralı/veri erişimi barındırmıyor. Veri, Application
katmanındaki ListInspectionsUseCase'den (zaten var olan) InspectionListItem
DTO'ları olarak geliyor; bu modül sadece onu kağıda döküyor.
"""

from io import BytesIO
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from app.application.dto.inspection_list_dto import InspectionListItem

LOGO_PATH = Path(__file__).resolve().parent.parent / "static" / "assets" / "tectone-logo.png"

# ReportLab'ın yerleşik "Helvetica" fontu Türkçe karakterleri (ı, ş, ğ) içermiyor —
# bu satırlar Windows'un Arial TTF'ini Unicode destekli olarak kaydediyor.
FONT_REGULAR = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
_ARIAL_REGULAR = Path("C:/Windows/Fonts/arial.ttf")
_ARIAL_BOLD = Path("C:/Windows/Fonts/arialbd.ttf")
if _ARIAL_REGULAR.exists() and _ARIAL_BOLD.exists():
    pdfmetrics.registerFont(TTFont("ArialTR", str(_ARIAL_REGULAR)))
    pdfmetrics.registerFont(TTFont("ArialTR-Bold", str(_ARIAL_BOLD)))
    FONT_REGULAR = "ArialTR"
    FONT_BOLD = "ArialTR-Bold"

NAVY = colors.HexColor("#0B2A4A")
RED = colors.HexColor("#D0212B")
INK = colors.HexColor("#16202B")
INK_MUTED = colors.HexColor("#5B6B78")
BORDER = colors.HexColor("#DDE2E6")
GOOD = colors.HexColor("#0CA30C")
CRITICAL = colors.HexColor("#D03B3B")
ROW_ALT = colors.HexColor("#F5F6F8")


def _fmt_tr(iso_date: str) -> str:
    """'YYYY-MM-DD' -> 'DD.MM.YYYY'."""
    y, m, d = iso_date.split("-")
    return f"{d}.{m}.{y}"


def generate_daily_report_pdf(
    start_date: str,
    items: list[InspectionListItem],
    line_label: str | None = None,
    end_date: str | None = None,
) -> bytes:
    """
    start_date/end_date: 'YYYY-MM-DD'. end_date verilmemişse (ya da start_date'e
    eşitse) tek günlük rapor; farklıysa çok günlük bir aralık raporu üretilir —
    bu durumda kayıt tablosunda saat yerine tarih+saat gösterilir.
    """
    end_date = end_date or start_date
    is_range = end_date != start_date
    period_label = f"{_fmt_tr(start_date)} – {_fmt_tr(end_date)}" if is_range else _fmt_tr(start_date)
    report_title = "Kalite Kontrol Raporu" if is_range else "Günlük Kalite Kontrol Raporu"
    pdf_title_date = period_label

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=18 * mm,
        bottomMargin=16 * mm,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        title=f"{report_title} - {pdf_title_date}",
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "ReportTitle", parent=styles["Normal"], fontName=FONT_BOLD,
        fontSize=16, textColor=NAVY, spaceAfter=2,
    )
    sub_style = ParagraphStyle(
        "ReportSub", parent=styles["Normal"], fontName=FONT_REGULAR,
        fontSize=10, textColor=INK_MUTED,
    )
    kpi_label_style = ParagraphStyle(
        "KpiLabel", parent=styles["Normal"], fontName=FONT_REGULAR, fontSize=8,
        textColor=INK_MUTED, alignment=TA_CENTER,
    )
    kpi_value_style = ParagraphStyle(
        "KpiValue", parent=styles["Normal"], fontName=FONT_BOLD, fontSize=18,
        textColor=NAVY, alignment=TA_CENTER,
    )
    footer_style = ParagraphStyle(
        "Footer", parent=styles["Normal"], fontName=FONT_REGULAR, fontSize=7.5,
        textColor=INK_MUTED, alignment=TA_RIGHT,
    )

    elements = []

    # ---- Başlık: logo + rapor adı ----
    if LOGO_PATH.exists():
        logo = Image(str(LOGO_PATH), width=32 * mm, height=32 * mm * (170 / 1024))
    else:
        logo = Spacer(32 * mm, 1)

    title_line = f"{report_title}<br/>{period_label}"
    if line_label:
        title_line += f'<br/><font size="10" color="#5B6B78">{line_label}</font>'
    else:
        title_line += '<br/><font size="10" color="#5B6B78">Tüm Hatlar</font>'

    header_table = Table(
        [[logo, Paragraph(title_line, title_style)]],
        colWidths=[38 * mm, 140 * mm],
    )
    header_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 4 * mm))

    hr = Table([[""]], colWidths=[178 * mm], rowHeights=[0.6])
    hr.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.75, NAVY)]))
    elements.append(hr)
    elements.append(Spacer(1, 6 * mm))

    # ---- KPI özet satırı ----
    total = len(items)
    defective = sum(1 for i in items if i.result == "FAIL")
    rate = round(defective / total * 100, 1) if total else 0.0

    kpi_table = Table(
        [
            [Paragraph("TOPLAM KONTROL", kpi_label_style), Paragraph("HATALI", kpi_label_style), Paragraph("HATA ORANI", kpi_label_style)],
            [Paragraph(str(total), kpi_value_style), Paragraph(str(defective), kpi_value_style), Paragraph(f"%{rate}", kpi_value_style)],
        ],
        colWidths=[59.3 * mm, 59.3 * mm, 59.3 * mm],
    )
    kpi_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(kpi_table)
    elements.append(Spacer(1, 8 * mm))

    # ---- Kayıt tablosu ----
    if not items:
        empty_msg = "Bu tarih aralığında hiç kayıt bulunmuyor." if is_range else "Bu tarihte hiç kayıt bulunmuyor."
        elements.append(Paragraph(empty_msg, sub_style))
    else:
        cell_style = ParagraphStyle("Cell", parent=styles["Normal"], fontName=FONT_REGULAR, fontSize=8.5, textColor=INK, leading=11)
        header_style = ParagraphStyle("CellHeader", parent=styles["Normal"], fontName=FONT_BOLD, fontSize=8, textColor=colors.white)

        def result_cell(result: str) -> Paragraph:
            color = GOOD if result == "PASS" else CRITICAL
            label = "OK" if result == "PASS" else "HATALI"
            style = ParagraphStyle("ResultCell", parent=cell_style, textColor=color, fontName=FONT_BOLD)
            return Paragraph(label, style)

        time_header = "Tarih / Saat" if is_range else "Saat"
        time_fmt = "%d.%m.%Y %H:%M" if is_range else "%H:%M"

        rows = [[
            Paragraph(time_header, header_style),
            Paragraph("TV Seri No", header_style),
            Paragraph("Sonuç", header_style),
            Paragraph("Hata Türü", header_style),
            Paragraph("Ek Açıklama", header_style),
        ]]
        for it in items:
            rows.append([
                Paragraph(it.inspected_at.strftime(time_fmt), cell_style),
                Paragraph(it.tv_serial_number, cell_style),
                result_cell(it.result),
                Paragraph(it.defect_category_name or "—", cell_style),
                Paragraph(it.defect_reason or "—", cell_style),
            ])

        col_widths = [30 * mm, 32 * mm, 20 * mm, 42 * mm, 54 * mm] if is_range else [18 * mm, 32 * mm, 20 * mm, 45 * mm, 63 * mm]
        table = Table(rows, colWidths=col_widths, repeatRows=1)
        style_cmds = [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]
        for row_idx in range(1, len(rows)):
            if row_idx % 2 == 0:
                style_cmds.append(("BACKGROUND", (0, row_idx), (-1, row_idx), ROW_ALT))
        table.setStyle(TableStyle(style_cmds))
        elements.append(table)

    elements.append(Spacer(1, 10 * mm))
    elements.append(Paragraph(
        "Bu belge QualiTV Kalite Analitik Platformu üzerinden otomatik olarak oluşturulmuştur.",
        footer_style,
    ))

    doc.build(elements)
    return buffer.getvalue()
