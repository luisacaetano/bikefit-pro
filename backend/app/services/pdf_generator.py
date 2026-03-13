"""
Gerador de Relatórios PDF para Bike Fit
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
from typing import Dict, Any, Optional
import os


class PDFGenerator:
    """Gerador de relatórios PDF para sessões de bike fit"""

    def __init__(self):
        """Inicializa o gerador de PDF"""
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Configura estilos personalizados"""
        self.styles.add(ParagraphStyle(
            name='TitleCustom',
            parent=self.styles['Heading1'],
            fontSize=24,
            alignment=TA_CENTER,
            spaceAfter=30,
            textColor=colors.HexColor('#2563EB')
        ))

        self.styles.add(ParagraphStyle(
            name='SubtitleCustom',
            parent=self.styles['Heading2'],
            fontSize=14,
            alignment=TA_CENTER,
            spaceAfter=20,
            textColor=colors.HexColor('#64748B')
        ))

        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceBefore=20,
            spaceAfter=10,
            textColor=colors.HexColor('#1E40AF')
        ))

    def generate(self, dados: Dict[str, Any], output_path: str) -> str:
        """
        Gera relatório PDF de uma sessão de bike fit

        Args:
            dados: Dicionário com dados da sessão
            output_path: Caminho para salvar o PDF

        Returns:
            Caminho do arquivo gerado
        """
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )

        elements = []

        # Título
        elements.append(Paragraph("BikeFit Pro", self.styles['TitleCustom']))
        elements.append(Paragraph("Relatório de Análise Postural", self.styles['SubtitleCustom']))
        elements.append(Spacer(1, 20))

        # Dados do paciente
        elements.append(Paragraph("Dados do Paciente", self.styles['SectionTitle']))
        paciente_data = [
            ["Nome:", dados.get("paciente", "N/A")],
            ["Data da Sessão:", dados.get("data", datetime.now().strftime("%d/%m/%Y"))],
        ]
        t = Table(paciente_data, colWidths=[4*cm, 10*cm])
        t.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 20))

        # Ângulos Antes
        if "angulos_antes" in dados:
            elements.append(Paragraph("Ângulos - Antes do Ajuste", self.styles['SectionTitle']))
            elements.append(self._create_angles_table(dados["angulos_antes"]))
            elements.append(Spacer(1, 15))

        # Ângulos Depois
        if "angulos_depois" in dados:
            elements.append(Paragraph("Ângulos - Após Ajuste", self.styles['SectionTitle']))
            elements.append(self._create_angles_table(dados["angulos_depois"]))
            elements.append(Spacer(1, 15))

        # Comparação
        if "angulos_antes" in dados and "angulos_depois" in dados:
            elements.append(Paragraph("Comparação", self.styles['SectionTitle']))
            elements.append(self._create_comparison_table(
                dados["angulos_antes"],
                dados["angulos_depois"]
            ))
            elements.append(Spacer(1, 15))

        # Ajustes Realizados
        if "ajustes" in dados:
            elements.append(Paragraph("Ajustes Realizados", self.styles['SectionTitle']))
            elements.append(self._create_adjustments_table(dados["ajustes"]))
            elements.append(Spacer(1, 15))

        # Recomendações
        if "recomendacoes" in dados:
            elements.append(Paragraph("Recomendações", self.styles['SectionTitle']))
            for rec in dados["recomendacoes"]:
                elements.append(Paragraph(f"• {rec}", self.styles['Normal']))
            elements.append(Spacer(1, 15))

        # Rodapé
        elements.append(Spacer(1, 30))
        footer_text = f"Relatório gerado por BikeFit Pro em {datetime.now().strftime('%d/%m/%Y às %H:%M')}"
        elements.append(Paragraph(footer_text, self.styles['SubtitleCustom']))

        # Gerar PDF
        doc.build(elements)
        return output_path

    def _create_angles_table(self, angles: Dict) -> Table:
        """Cria tabela de ângulos"""
        angle_names = {
            "knee_extension": "Extensão do Joelho",
            "knee_flexion": "Flexão do Joelho",
            "hip": "Quadril",
            "ankle": "Tornozelo",
            "trunk": "Tronco",
            "elbow": "Cotovelo",
            "knee": "Joelho"
        }

        data = [["Articulação", "Ângulo Medido", "Faixa Ideal"]]

        ideal_ranges = {
            "knee_extension": "140° - 150°",
            "knee_flexion": "65° - 75°",
            "hip": "40° - 50°",
            "ankle": "90° - 110°",
            "trunk": "40° - 55°",
            "elbow": "150° - 170°",
            "knee": "140° - 150°"
        }

        for key, value in angles.items():
            name = angle_names.get(key, key)
            ideal = ideal_ranges.get(key, "N/A")
            data.append([name, f"{value}°", ideal])

        t = Table(data, colWidths=[5*cm, 4*cm, 4*cm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')])
        ]))
        return t

    def _create_comparison_table(self, before: Dict, after: Dict) -> Table:
        """Cria tabela comparativa antes/depois"""
        angle_names = {
            "knee_extension": "Extensão do Joelho",
            "knee_flexion": "Flexão do Joelho",
            "hip": "Quadril",
            "ankle": "Tornozelo",
            "trunk": "Tronco",
            "elbow": "Cotovelo",
            "knee": "Joelho"
        }

        data = [["Articulação", "Antes", "Depois", "Variação"]]

        all_keys = set(before.keys()) | set(after.keys())
        for key in all_keys:
            name = angle_names.get(key, key)
            val_before = before.get(key, "N/A")
            val_after = after.get(key, "N/A")

            if isinstance(val_before, (int, float)) and isinstance(val_after, (int, float)):
                variation = val_after - val_before
                var_str = f"{'+' if variation > 0 else ''}{variation}°"
            else:
                var_str = "N/A"

            data.append([
                name,
                f"{val_before}°" if isinstance(val_before, (int, float)) else str(val_before),
                f"{val_after}°" if isinstance(val_after, (int, float)) else str(val_after),
                var_str
            ])

        t = Table(data, colWidths=[4*cm, 3*cm, 3*cm, 3*cm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ]))
        return t

    def _create_adjustments_table(self, adjustments: Dict) -> Table:
        """Cria tabela de ajustes realizados"""
        adjustment_names = {
            "selim": "Altura do Selim",
            "selim_altura": "Altura do Selim",
            "selim_recuo": "Recuo do Selim",
            "guidao": "Guidão",
            "guidao_altura": "Altura do Guidão",
            "guidao_reach": "Reach do Guidão",
            "avanço": "Avanço",
            "taco": "Posição do Taco",
            "mesa": "Mesa"
        }

        data = [["Componente", "Ajuste"]]

        for key, value in adjustments.items():
            name = adjustment_names.get(key, key)
            data.append([name, str(value)])

        t = Table(data, colWidths=[5*cm, 8*cm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7C3AED')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ]))
        return t
