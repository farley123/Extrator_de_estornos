from formatar_planilha import FormatarPlanilha
from  gerar_pdf import GerarPdf
if __name__ == '__main__':
    lista_de_dados= FormatarPlanilha('/home/farley/Downloads/estornosatualizado/estornos_declaracao_01_01_24_31_01_26.xlsx')
    gerar_pdf= GerarPdf(lista_de_dados.gerar_lista_de_dados())
    gerar_pdf.salvar_pdf('/home/farley/Downloads')

