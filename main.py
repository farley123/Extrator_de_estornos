import flet as ft

from formatar_planilha import FormatarPlanilha


# Supondo que essas classes estejam em arquivos separados no seu projeto
from formatar_planilha import FormatarPlanilha
from gerar_pdf import GerarPdf

def main(page: ft.Page):
    page.title = "Extrator de estornos"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window.width = 1400
    page.window.height = 300
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.resizable = False
    page.window.maximizable = False

    #
    lista_de_dados=None
    destino_path= None

    progress = ft.ProgressBar(width=400, visible=False)

    selecionar_planilha = ft.TextField(label='Selecionar planilha', text_align=ft.TextAlign.LEFT, width=600)
    selecionar_destino = ft.TextField(label='selecionar destino', text_align=ft.TextAlign.LEFT, width=600)


    async def handle_pick_files(e: ft.Event[ft.Button]):
        files =await  ft.FilePicker().pick_files()
        selecionar_planilha.value =files[0].path
        nonlocal lista_de_dados
        lista_de_dados=FormatarPlanilha(selecionar_planilha.value).gerar_lista_de_dados()

    async def handle_get_directory_path(e: ft.Event[ft.Button]):
        selecionar_destino.value = await ft.FilePicker().get_directory_path()
        nonlocal destino_path
        destino_path =selecionar_destino.value




    async def gerar_pdf_async():


        GerarPdf(lista_de_dados).salvar_pdf(destino_path)

        progress.visible = False
        snack_bar = ft.SnackBar(ft.Text("PDF gerado com sucesso!"))
        page.overlay.append(snack_bar)
        snack_bar.open=True
        page.update()

    def criar_pdf(e):
        progress.visible = True
        page.update()
        page.run_task(gerar_pdf_async)

    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.START,
            controls=[
                selecionar_planilha,
                ft.IconButton(ft.Icons.PLAY_CIRCLE,
                              on_click=handle_pick_files),
                selecionar_destino,
                ft.IconButton(ft.Icons.PLAY_CIRCLE, on_click=handle_get_directory_path)
            ],
        ),
        ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Button(content=ft.Text('Gerar Pdf'), bgcolor=ft.Colors.GREEN, on_click=criar_pdf)
            ]
        ),
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[progress]
        )
    )


# CORREÇÃO: ft.run em vez de ft.app
ft.run(main)