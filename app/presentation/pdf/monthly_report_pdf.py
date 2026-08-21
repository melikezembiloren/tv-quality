"""
Üst yönetime sunulacak aylık kalite özet raporu.

Saf bir sunum katmanı endişesi: veri GetMonthlyReportUseCase'den (Application) DTO
olarak geliyor, bu modül sadece onu kağıda döküyor. Stil sabitleri (renkler, font)
daily_report.py ile paylaşılıyor ki iki rapor birbirinden sapmasın.

İki üretim fonksiyonu var:
- generate_monthly_report_pdf: tek bölümlük rapor (Tüm Hatlar ya da tek bir hat).
- generate_monthly_report_pdf_by_line: "Tüm Hatlar" özetiyle başlayıp ardından
  her üretim hattı için ayrı bir sayfa ekleyen, üst yönetime tek belge olarak
  sunulabilecek çok sayfalı rapor.
"""

from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart

from app.application.dto.monthly_report_dto import MonthlyReportData
from app.presentation.pdf.daily_report import (
    LOGO_PATH,
    FONT_REGULAR,
    FONT_BOLD,
    NAVY,
    INK,
    INK_MUTED,
    BORDER,
    GOOD,
    CRITICAL,
    ROW_ALT,
)

ACCENT = colors.HexColor("#4A3AA7")
WARNING = colors.HexColor("#FAB219")
SERIOUS = colors.HexColor("#EC835A")

_MONTH_NAMES_TR = {
    "01": "Ocak", "02": "Şubat", "03": "Mart", "04": "Nisan", "05": "Mayıs", "06": "Haziran",
    "07": "Temmuz", "08": "Ağustos", "09": "Eylül", "10": "Ekim", "11": "Kasım", "12": "Aralık",
}


def _month_label(month: str) -> str:
    year, mon = month.split("-")
    return f"{_MONTH_NAMES_TR.get(mon, mon)} {year}"


_styles = getSampleStyleSheet()
_TITLE_STYLE = ParagraphStyle("Title", parent=_styles["Normal"], fontName=FONT_BOLD, fontSize=16, textColor=NAVY, spaceAfter=2)
_SUB_STYLE = ParagraphStyle("Sub", parent=_styles["Normal"], fontName=FONT_REGULAR, fontSize=10, textColor=INK_MUTED)
_SECTION_STYLE = ParagraphStyle("Section", parent=_styles["Normal"], fontName=FONT_BOLD, fontSize=11.5, textColor=NAVY, spaceBefore=10, spaceAfter=4)
_KPI_LABEL_STYLE = ParagraphStyle("KpiLabel", parent=_styles["Normal"], fontName=FONT_REGULAR, fontSize=8, textColor=INK_MUTED, alignment=TA_CENTER)
_KPI_VALUE_STYLE = ParagraphStyle("KpiValue", parent=_styles["Normal"], fontName=FONT_BOLD, fontSize=18, textColor=NAVY, alignment=TA_CENTER)
_CELL_STYLE = ParagraphStyle("Cell", parent=_styles["Normal"], fontName=FONT_REGULAR, fontSize=8.5, textColor=INK, leading=11)
_HEADER_CELL_STYLE = ParagraphStyle("CellHeader", parent=_styles["Normal"], fontName=FONT_BOLD, fontSize=8, textColor=colors.white)
_FOOTER_STYLE = ParagraphStyle("Footer", parent=_styles["Normal"], fontName=FONT_REGULAR, fontSize=7.5, textColor=INK_MUTED, alignment=TA_RIGHT)


def _styled_table(rows, col_widths):
    t = Table(rows, colWidths=col_widths, repeatRows=1)
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
    ]
    for i in range(1, len(rows)):
        if i % 2 == 0:
            cmds.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))
    t.setStyle(TableStyle(cmds))
    return t


def _build_section(data: MonthlyReportData, label: str, show_by_line_table: bool = True) -> list:
    """Bir rapor bölümünün (Tüm Hatlar ya da tek bir hat) tüm flowable'larını üretir."""
    elements = []

    # ---- Başlık ----
    logo = Image(str(LOGO_PATH), width=30 * mm, height=30 * mm * (170 / 1024)) if LOGO_PATH.exists() else Spacer(30 * mm, 1)
    title_html = f"Aylık Kalite Özet Raporu<br/><font size='10' color='#5B6B78'>{_month_label(data.month)} &middot; {label}</font>"
    header_table = Table([[logo, Paragraph(title_html, _TITLE_STYLE)]], colWidths=[36 * mm, 142 * mm])
    header_table.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (1, 0), (1, 0), "RIGHT")]))
    elements.append(header_table)
    elements.append(Spacer(1, 3 * mm))
    hr = Table([[""]], colWidths=[178 * mm], rowHeights=[0.6])
    hr.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.75, NAVY)]))
    elements.append(hr)
    elements.append(Spacer(1, 5 * mm))

    # ---- KPI satırı ----
    kpi_table = Table(
        [
            [Paragraph("TOPLAM KONTROL", _KPI_LABEL_STYLE), Paragraph("TOPLAM HATALI", _KPI_LABEL_STYLE), Paragraph("HATA ORANI", _KPI_LABEL_STYLE), Paragraph("DENETİM / BULGU", _KPI_LABEL_STYLE)],
            [
                Paragraph(str(data.total_inspected), _KPI_VALUE_STYLE),
                Paragraph(str(data.total_defective), _KPI_VALUE_STYLE),
                Paragraph(f"%{data.defect_rate}", _KPI_VALUE_STYLE),
                Paragraph(f"{data.total_audits} / {data.total_findings}", _KPI_VALUE_STYLE),
            ],
        ],
        colWidths=[44.5 * mm] * 4,
    )
    kpi_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(kpi_table)

    # ---- Son 6 ay trend (bar chart) ----
    elements.append(Paragraph("Hata Oranı Trendi (Son 6 Ay)", _SECTION_STYLE))
    if data.trend_last_months:
        drawing = Drawing(178 * mm, 42 * mm)
        chart = VerticalBarChart()
        chart.x = 30
        chart.y = 10
        chart.width = 470
        chart.height = 100
        rates = [round(p.defective / p.inspected * 100, 1) if p.inspected else 0.0 for p in data.trend_last_months]
        chart.data = [rates]
        chart.categoryAxis.categoryNames = [p.period[5:] + "/" + p.period[2:4] for p in data.trend_last_months]
        chart.categoryAxis.labels.fontName = FONT_REGULAR
        chart.categoryAxis.labels.fontSize = 8
        chart.valueAxis.labels.fontName = FONT_REGULAR
        chart.valueAxis.labels.fontSize = 8
        chart.valueAxis.valueMin = 0
        chart.bars[0].fillColor = ACCENT
        chart.barWidth = 14
        drawing.add(chart)
        elements.append(drawing)
    else:
        elements.append(Paragraph("Henüz trend için yeterli veri yok.", _SUB_STYLE))

    # ---- Hat bazlı tablo (yalnızca "Tüm Hatlar" görünümünde anlamlı) ----
    if show_by_line_table:
        elements.append(Paragraph("Hat Bazlı Sonuçlar", _SECTION_STYLE))
        if data.by_line:
            rows = [[
                Paragraph("Hat", _HEADER_CELL_STYLE), Paragraph("Kontrol", _HEADER_CELL_STYLE),
                Paragraph("Hatalı", _HEADER_CELL_STYLE), Paragraph("Oran", _HEADER_CELL_STYLE),
            ]]
            for l in data.by_line:
                rate = round(l.defective / l.inspected * 100, 1) if l.inspected else 0.0
                rows.append([
                    Paragraph(f"{l.line_code} — {l.line_name}", _CELL_STYLE),
                    Paragraph(str(l.inspected), _CELL_STYLE),
                    Paragraph(str(l.defective), _CELL_STYLE),
                    Paragraph(f"%{rate}", _CELL_STYLE),
                ])
            table = Table(rows, colWidths=[88 * mm, 30 * mm, 30 * mm, 30 * mm], repeatRows=1)
            style_cmds = [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TOPPADDING", (0, 0), (-1, -1), 4.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
                ("LEFTPADDING", (0, 0), (-1, -1), 6), ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
            ]
            for i in range(1, len(rows)):
                if i % 2 == 0:
                    style_cmds.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))
            table.setStyle(TableStyle(style_cmds))
            elements.append(table)
        else:
            elements.append(Paragraph("Bu ay için hiç kontrol kaydı yok.", _SUB_STYLE))

    # ---- En sık hatalar + istasyon dağılımı (yan yana) ----
    reasons_block = [[Paragraph("Hata Türü", _HEADER_CELL_STYLE), Paragraph("Adet", _HEADER_CELL_STYLE)]]
    for r in data.top_reasons:
        reasons_block.append([Paragraph(r.reason, _CELL_STYLE), Paragraph(str(r.count), _CELL_STYLE)])
    if len(reasons_block) == 1:
        reasons_block.append([Paragraph("Hata kaydı yok", _CELL_STYLE), Paragraph("—", _CELL_STYLE)])

    station_block = [[Paragraph("İstasyon", _HEADER_CELL_STYLE), Paragraph("Adet", _HEADER_CELL_STYLE)]]
    for s in data.by_station:
        station_block.append([Paragraph(s.station, _CELL_STYLE), Paragraph(str(s.count), _CELL_STYLE)])
    if len(station_block) == 1:
        station_block.append([Paragraph("Hata kaydı yok", _CELL_STYLE), Paragraph("—", _CELL_STYLE)])

    elements.append(
        Table(
            [[
                Paragraph("En Sık Görülen Hatalar", _SECTION_STYLE),
                "",
                Paragraph("İstasyon Dağılımı", _SECTION_STYLE),
            ]],
            colWidths=[86 * mm, 6 * mm, 86 * mm],
        )
    )
    side_by_side = Table(
        [[_styled_table(reasons_block, [66 * mm, 20 * mm]), "", _styled_table(station_block, [66 * mm, 20 * mm])]],
        colWidths=[86 * mm, 6 * mm, 86 * mm],
    )
    side_by_side.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    elements.append(side_by_side)

    # ---- Denetim özeti ----
    elements.append(Paragraph("Denetim (Audit) Özeti — Bu Ay", _SECTION_STYLE))
    sev = data.severity_breakdown
    sev_rows = [
        [Paragraph("Düşük", _HEADER_CELL_STYLE), Paragraph("Orta", _HEADER_CELL_STYLE), Paragraph("Yüksek", _HEADER_CELL_STYLE), Paragraph("Kritik", _HEADER_CELL_STYLE)],
        [
            Paragraph(str(sev.low), ParagraphStyle("L", parent=_CELL_STYLE, textColor=GOOD, fontName=FONT_BOLD, alignment=TA_CENTER)),
            Paragraph(str(sev.medium), ParagraphStyle("M", parent=_CELL_STYLE, textColor=WARNING, fontName=FONT_BOLD, alignment=TA_CENTER)),
            Paragraph(str(sev.high), ParagraphStyle("H", parent=_CELL_STYLE, textColor=SERIOUS, fontName=FONT_BOLD, alignment=TA_CENTER)),
            Paragraph(str(sev.critical), ParagraphStyle("C", parent=_CELL_STYLE, textColor=CRITICAL, fontName=FONT_BOLD, alignment=TA_CENTER)),
        ],
    ]
    sev_table = Table(sev_rows, colWidths=[44.5 * mm] * 4)
    sev_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
    ]))
    elements.append(sev_table)

    elements.append(Spacer(1, 8 * mm))
    elements.append(Paragraph(
        "Bu belge QualiTV Kalite Analitik Platformu üzerinden otomatik olarak oluşturulmuştur.",
        _FOOTER_STYLE,
    ))
    return elements


def generate_monthly_report_pdf(data: MonthlyReportData, line_label: str | None = None) -> bytes:
    """Tek bölümlük rapor — line_label verilmezse 'Tüm Hatlar', verilirse o hattın adı başlıkta görünür."""
    buffer = BytesIO()
    label = line_label or "Tüm Hatlar"
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=16 * mm,
        bottomMargin=14 * mm,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        title=f"Aylık Kalite Özet Raporu - {data.month} - {label}",
    )
    elements = _build_section(data, label, show_by_line_table=(line_label is None))
    doc.build(elements)
    return buffer.getvalue()


def generate_monthly_report_pdf_by_line(overall_data: MonthlyReportData, per_line: list[tuple[str, MonthlyReportData]]) -> bytes:
    """
    Üst yönetime tek belge olarak sunulacak çok sayfalı rapor:
    1. sayfa 'Tüm Hatlar' özeti, ardından her üretim hattı için ayrı bir sayfa.
    per_line: [(hat etiketi, o hatta ait MonthlyReportData), ...]
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=16 * mm,
        bottomMargin=14 * mm,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        title=f"Aylık Kalite Özet Raporu (Hat Bazlı) - {overall_data.month}",
    )

    elements = _build_section(overall_data, "Tüm Hatlar", show_by_line_table=True)
    for label, data in per_line:
        elements.append(PageBreak())
        elements.extend(_build_section(data, label, show_by_line_table=False))

    doc.build(elements)
    return buffer.getvalue()
