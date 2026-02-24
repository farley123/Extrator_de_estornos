from pypdf import PdfReader,PdfWriter
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter, PageObject
from reportlab.pdfgen import canvas
import sys
import os


class GerarPdf:
    def __init__(self,lista_de_dados):
        self.template_pdf = PdfReader(self.resource_path("formulario_estorno.pdf"))
        self.writer = PdfWriter()
        self.lista_de_dados = lista_de_dados


    def __merge_template_com_template_temporario(self,overlay_pdf):
        template_page = self.template_pdf.pages[0]
        page_copy = PageObject.create_blank_page(
            width=template_page.mediabox.width,
            height=template_page.mediabox.height
        )
        page_copy.merge_page(template_page)  # primeiro template
        page_copy.merge_page(overlay_pdf.pages[0])  # depois overlay
        templates_mesclados=page_copy
        return templates_mesclados

    def __criar_pdf(self):
        for dados in self.lista_de_dados:
            # Criar PDF temporário em memória para overlay
            packet = BytesIO()
            c = canvas.Canvas(packet)

            # 🔹 Ajuste as coordenadas conforme seu layout
            c.drawString(250,705,f"{dados['Work Center Resource']}")
            c.drawString(250, 670, f"{dados['Production Order']}")
            c.drawString(250, 635, f"{dados['Material Code']}")
            c.setFont("Helvetica", 10)
            # c.setFillColorRGB(2,3,4)
            c.drawString(250, 600, f"{dados['Material Description']}")
            c.setFont("Helvetica", 12)
            c.drawString(250, 565, f"{dados['Material Document No']}")
            c.drawString(250, 530, f"{dados['Posting Date']}")
            c.drawString(250, 495, f"{dados['Qty in KG']} KG")
            c.drawString(250, 460, f"{dados['User Name']}")
            c.drawString(250, 425, f"{dados['User Name']}")

            c.save()
            packet.seek(0)
            overlay_pdf = PdfReader(packet)
            self.writer.add_page(self.__merge_template_com_template_temporario(overlay_pdf))

    def salvar_pdf(self, output_dir):
        try:
            self.__criar_pdf()

            # cria uma pasta, NÃO um arquivo .pdf
            pasta_saida = os.path.join(output_dir, "estornos")
            os.makedirs(pasta_saida, exist_ok=True)

            # arquivo final
            output_final = os.path.join(pasta_saida, "todos_registros.pdf")

            with open(output_final, "wb") as f:
                self.writer.write(f)

        except Exception as e:
            # log de erro (essencial no executável)
            with open("erro_pdf.log", "w", encoding="utf-8") as f:
                f.write(str(e))
            raise

    def resource_path(self,relative_path):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.getcwd(), relative_path)