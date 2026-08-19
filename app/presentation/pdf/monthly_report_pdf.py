"""
Üst yönetime sunulacak aylık kalite özet raporu — tek sayfalık PDF.

Saf bir sunum katmanı endişesi: veri GetMonthlyReportUseCase'den (Application) DTO
olarak geliyor, bu modül sadece onu kağıda döküyor. Stil sabitleri (renkler, font)
daily_report.py ile paylaşılıyor ki iki rapor birbirinden sapmasın.
"""

from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
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


def generate_monthly_report_pdf(data: MonthlyReportData) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=16 * mm,
        bottomMargin=14 * mm,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        title=f"Aylık Kalite Özet Raporu - {data.month}",
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("Title", parent=styles["Normal"], fontName=FONT_BOLD, fontSize=16, textColor=NAVY, spaceAfter=2)
    sub_style = ParagraphStyle("Sub", parent=styles["Normal"], fontName=FONT_REGULAR, fontSize=10, textColor=INK_MUTED)
    section_style = ParagraphStyle("Section", parent=styles["Normal"], fontName=FONT_BOLD, fontSize=11.5, textColor=NAVY, spaceBefore=10, spaceAfter=4)
    kpi_label_style = ParagraphStyle("KpiLabel", parent=styles["Normal"], fontName=FONT_REGULAR, fontSize=8, textColor=INK_MUTED, alignment=TA_CENTER)
    kpi_value_style = ParagraphStyle("KpiValue", parent=styles["Normal"], fontName=FONT_BOLD, fontSize=18, textColor=NAVY, alignment=TA_CENTER)
    cell_style = ParagraphStyle("Cell", parent=styles["Normal"], fontName=FONT_REGULAR, fontSize=8.5, textColor=INK, leading=11)
    header_cell_style = ParagraphStyle("CellHeader", parent=styles["Normal"], fontName=FONT_BOLD, fontSize=8, textColor=colors.white)
    footer_style = ParagraphStyle("Footer", parent=styles["Normal"], fontName=FONT_REGULAR, fontSize=7.5, textColor=INK_MUTED, alignment=TA_RIGHT)

    elements = []

    # ---- Başlık ----
    logo = Image(str(LOGO_PATH), width=30 * mm, height=30 * mm * (170 / 1024)) if LOGO_PATH.exists() else Spacer(30 * mm, 1)
    title_html = f"Aylık Kalite Özet Raporu<br/><font size='10' color='#5B6B78'>{_month_label(data.month)} &middot; Üst Yönetim Sunumu İçin</font>"
    header_table = Table([[logo, Paragraph(title_html, title_style)]], colWidths=[36 * mm, 142 * mm])
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
            [Paragraph("TOPLAM KONTROL", kpi_label_style), Paragraph("TOPLAM HATALI", kpi_label_style), Paragraph("HATA ORANI", kpi_label_style), Paragraph("DENETİM / BULGU", kpi_label_style)],
            [
                Paragraph(str(data.total_inspected), kpi_value_style),
                Paragraph(str(data.total_defective), kpi_value_style),
                Paragraph(f"%{data.defect_rate}", kpi_value_style),
                Paragraph(f"{data.total_audits} / {data.total_findings}", kpi_value_style),
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
    elements.append(Paragraph("Hata Oranı Trendi (Son 6 Ay)", section_style))
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
        elements.append(Paragraph("Henüz trend için yeterli veri yok.", sub_style))

    # ---- Hat bazlı tablo ----
    elements.append(Paragraph("Hat Bazlı Sonuçlar", section_style))
    if data.by_line:
        rows = [[
            Paragraph("Hat", header_cell_style), Paragraph("Kontrol", header_cell_style),
            Paragraph("Hatalı", header_cell_style), Paragraph("Oran", header_cell_style),
        ]]
        for l in data.by_line:
            rate = round(l.defective / l.inspected * 100, 1) if l.inspected else 0.0
            rows.append([
                Paragraph(f"{l.line_code} — {l.line_name}", cell_style),
                Paragraph(str(l.inspected), cell_style),
                Paragraph(str(l.defective), cell_style),
                Paragraph(f"%{rate}", cell_style),
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
        elements.append(Paragraph("Bu ay için hiç kontrol kaydı yok.", sub_style))

    # ---- En sık hatalar + istasyon dağılımı (yan yana) ----
    reasons_block = [[Paragraph("Hata Türü", header_cell_style), Paragraph("Adet", header_cell_style)]]
    for r in data.top_reasons:
        reasons_block.append([Paragraph(r.reason, cell_style), Paragraph(str(r.count), cell_style)])
    if len(reasons_block) == 1:
        reasons_block.append([Paragraph("Hata kaydı yok", cell_style), Paragraph("—", cell_style)])

    station_block = [[Paragraph("İstasyon", header_cell_style), Paragraph("Adet", header_cell_style)]]
    for s in data.by_station:
        station_block.append([Paragraph(s.station, cell_style), Paragraph(str(s.count), cell_style)])
    if len(station_block) == 1:
        station_block.append([Paragraph("Hata kaydı yok", cell_style), Paragraph("—", cell_style)])

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

    elements.append(
        Table(
            [[
                Paragraph("En Sık Görülen Hatalar", section_style),
                "",
                Paragraph("İstasyon Dağılımı", section_style),
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
    elements.append(Paragraph("Denetim (Audit) Özeti — Bu Ay", section_style))
    sev = data.severity_breakdown
    sev_rows = [
        [Paragraph("Düşük", header_cell_style), Paragraph("Orta", header_cell_style), Paragraph("Yüksek", header_cell_style), Paragraph("Kritik", header_cell_style)],
        [
            Paragraph(str(sev.low), ParagraphStyle("L", parent=cell_style, textColor=GOOD, fontName=FONT_BOLD, alignment=TA_CENTER)),
            Paragraph(str(sev.medium), ParagraphStyle("M", parent=cell_style, textColor=WARNING, fontName=FONT_BOLD, alignment=TA_CENTER)),
            Paragraph(str(sev.high), ParagraphStyle("H", parent=cell_style, textColor=SERIOUS, fontName=FONT_BOLD, alignment=TA_CENTER)),
            Paragraph(str(sev.critical), ParagraphStyle("C", parent=cell_style, textColor=CRITICAL, fontName=FONT_BOLD, alignment=TA_CENTER)),
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
        footer_style,
    ))

    doc.build(elements)
    return buffer.getvalue()
