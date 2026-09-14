#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
=== HOSPITAL IT DIRECTOR TRANSMITTAL LETTER PDF GENERATOR                  ===
==============================================================================
"""

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# Register Cyrillic Arial Fonts
pdfmetrics.registerFont(TTFont('Arial', 'C:\\Windows\\Fonts\\arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'C:\\Windows\\Fonts\\arialbd.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Italic', 'C:\\Windows\\Fonts\\ariali.ttf'))

class LetterCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Arial", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Footer
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(40, 45, 555, 45)

        self.drawString(40, 32, "AETERNA Technologies • Официален институционален документ • Съответствие с NIS2 и GDPR.")
        self.drawRightString(555, 32, f"Страница {self._pageNumber} от {page_count}")
        self.restoreState()

def build_letter_pdf():
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "generated")
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "HOSPITAL_IT_DIRECTOR_TRANSMITTAL_LETTER_MU_SOFIA.pdf")

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=45,
        rightMargin=45,
        topMargin=50,
        bottomMargin=55
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        fontName='Arial-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#0f172a'),
        alignment=0
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        fontName='Arial',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#059669'),
        alignment=0
    )
    h2_style = ParagraphStyle(
        'Header2',
        fontName='Arial-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body',
        fontName='Arial',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=7
    )
    table_text = ParagraphStyle(
        'TableText',
        fontName='Arial',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#1e293b')
    )

    story = []

    # Title
    story.append(Paragraph("ОФИЦИАЛНО ПРИДРУЖИТЕЛНО ПИСМО ЗА СЪГЛАСУВАНЕ", title_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph("Разполагане и мрежово съгласуване на пилотен болничен Edge сървър AETERNA-VHT (Порт 8890)", subtitle_style))
    story.append(Spacer(1, 10))

    recipient_data = [
        [
            Paragraph("<b>ДО:</b><br/>"
                      "<b>ДИРЕКТОРА НА ДИРЕКЦИЯ „ИКТ“</b><br/>"
                      "Медицински Университет – София<br/>"
                      "УМБАЛ „Св. Иван Рилски“ / СБАЛО", table_text),
            Paragraph("<b>ОТ:</b><br/>"
                      "<b>ДИМИТЪР ПРОДРОМОВ</b><br/>"
                      "Главен Архитект на AETERNA Core<br/>"
                      "Authority: <code>0x41_45_54_45_52_4e_41...</code>", table_text),
            Paragraph("<b>ДАТА:</b> 14.09.2026 г.<br/>"
                      "<b>ГР.:</b> София<br/>"
                      "<b>СТАТУТ:</b> ВХОДИРАНО", table_text)
        ]
    ]
    rec_table = Table(recipient_data, colWidths=[205, 195, 105])
    rec_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(rec_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>УВАЖАЕМИ ГОСПОДИН ДИРЕКТОР НА ДИРЕКЦИЯ „ИКТ“,</b>", body_style))
    story.append(Paragraph(
        "С настоящото писмо официално входирам към ръководената от Вас дирекция комплекта техническа документация за съгласуване на пилотното "
        "разполагане на вътрешен болничен Edge възел на научно-изследователската платформа за онкологични дигитални двойници <b>AETERNA-VHT</b> "
        "(регистрирана в CERN Zenodo под DOI: 10.5281/zenodo.22734388 и DOI: 10.5281/zenodo.22703199).",
        body_style
    ))
    story.append(Paragraph(
        "В изпълнение на изискванията на <b>Директивата NIS2 (EU 2022/2555)</b> за киберсигурност на критичната инфраструктура и <b>Член 9 от GDPR</b>, "
        "системата е проектирана изцяло като <b>Zero-Cloud On-Premise LAN</b> субстрат със следните строги технически параметри:",
        body_style
    ))

    story.append(Paragraph(
        "1. <b>Нулева входяща експозиция (Drop All Inbound):</b> Болничният сървър не отваря входящи портове от интернет и отхвърля всякакъв отдалечен достъп (No TeamViewer / AnyDesk / RDP).<br/>"
        "2. <b>Изолиран LAN порт 8890:</b> Работи като защитена фонова услуга на Windows Server, достъпна единствено за оторизираните работни станции в Клиниката по онкология и Болничната аптека.<br/>"
        "3. <b>Автономен Pull-Updater (03:00 ч.):</b> Софтуерните обновления се теглят през изходящ HTTPS канал с проверка на цифров подпис по SHA-512 в извънработно време с автоматичен ролбек.<br/>"
        "4. <b>Интеграция с НЗИС („е-Здраве“ / his.bg):</b> Вграден HL7 FHIR R4 адаптер, поддържащ 12-цифрени НРН баркодове (Modulo 11) и цифрово подписване с лекарски КЕП (XAdES-BES).",
        body_style
    ))

    story.append(Paragraph("<b>Окомплектован пакет от технически приложения:</b>", h2_style))
    story.append(Paragraph(
        "• <b>Приложение 1:</b> Официален технически наръчник за внедряване (<code>AETERNA_VHT_HOSPITAL_DEPLOYMENT_MANUAL.pdf</code>)<br/>"
        "• <b>Приложение 2:</b> Спецификация за интеграция с НЗИС API (<code>NZIS_FHIR_INTEGRATION_SPEC.md</code>)<br/>"
        "• <b>Приложение 3:</b> Инсталационен PowerShell пакет за системна услуга (<code>install_hospital_windows_service.ps1</code>)<br/>"
        "• <b>Приложение 4:</b> Ръководство за настолните клиенти и лазерни скенери (<code>hospital-tauri-client/</code>)",
        body_style
    ))

    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Моля за Вашето писмено съгласуване и определяне на отговорен системен администратор от дирекция „ИКТ“ за съвместно провеждане на приемо-предавателния тест на порт 8890.",
        body_style
    ))
    story.append(Spacer(1, 10))

    # Signatures
    assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
    stamp_path = os.path.join(assets_dir, "aeterna_official_stamp_transparent.png")
    sig_path = os.path.join(assets_dir, "dimitar_prodromov_signature_transparent.png")

    sig_img = Image(sig_path, width=130, height=50) if os.path.exists(sig_path) else Paragraph("", body_style)
    stamp_img = Image(stamp_path, width=70, height=70) if os.path.exists(stamp_path) else Paragraph("", body_style)

    sig_data = [
        [
            Paragraph("<b>С уважение и готовност за съвместна работа:</b><br/><br/>"
                      "<b>Димитър Продромов</b><br/>"
                      "Главен Архитект на AETERNA Core<br/>"
                      "ID: 101327948 • УИН: 101327948<br/>"
                      "Authority: <code>0x41_45_54_45_52_4e_41...</code>", body_style),
            sig_img,
            stamp_img,
            Paragraph("<b>Входящ номер Дирекция „ИКТ“:</b><br/><br/>"
                      "Вх. №: ...........................................<br/>"
                      "Дата: .................... 2026 г.<br/>"
                      "Приел: ...........................................<br/>"
                      "Подпис и печат:", body_style)
        ]
    ]

    sig_table = Table(sig_data, colWidths=[185, 110, 75, 135])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))

    story.append(KeepTogether([sig_table]))

    doc.build(story, canvasmaker=LetterCanvas)
    print(f"✓ Letter PDF successfully generated: {pdf_path}")

if __name__ == "__main__":
    build_letter_pdf()
