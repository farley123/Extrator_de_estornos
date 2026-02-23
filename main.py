import flet as ft
from formatar_planilha import FormatarPlanilha
from  gerar_pdf import GerarPdf

def main(page: ft.Page):
    page.title = "Extrator de estornos"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window.width=1400
    page.window.height=300
    page.theme_mode=ft.ThemeMode.LIGHT
    page.window.resizable=False
    page.window.maximizable=False
    picker_planilha=ft.FilePicker()
    picker_destino=ft.FilePicker()
    page.session.set("lista_de_dados", None)
    page.session.set("destino_path", None)

    progress = ft.ProgressBar(
        width=400,
        visible=False
    )
    selecionar_planilha = ft.TextField(label='Selecionar planilha', text_align=ft.TextAlign.LEFT, width=600)
    selecionar_destino = ft.TextField(label='selecionar destino', text_align=ft.TextAlign.LEFT, width=600)
    def selecionar_planilha_picker(e: ft.FilePickerResultEvent):
        if e.files:
            selecionar_planilha.value = e.files[0].path
            page.session.set(
                "lista_de_dados",
                FormatarPlanilha(selecionar_planilha.value).gerar_lista_de_dados()
            )
            page.update()
    def selecionar_destino_picker(e: ft.FilePickerResultEvent):
        if e.path:
            selecionar_destino.value = e.path
            page.session.set("destino_path", selecionar_destino.value)
            page.update()


    picker_planilha.on_result = selecionar_planilha_picker
    picker_destino.on_result = selecionar_destino_picker

    page.overlay.append(picker_planilha)
    page.overlay.append(picker_destino)




    async def gerar_pdf_async():
        lista = page.session.get("lista_de_dados")
        destino = page.session.get("destino_path")
        GerarPdf(lista).salvar_pdf(destino)

        progress.visible = False
        page.snack_bar = ft.SnackBar(
            ft.Text("PDF gerado com sucesso!")
        )
        page.snack_bar.open = True
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
                ft.IconButton(ft.icons.PLAY_CIRCLE, on_click=lambda e: picker_planilha.pick_files(
                        allow_multiple=False
                    )),
                selecionar_destino,
                ft.IconButton(ft.icons.PLAY_CIRCLE, on_click=lambda e: picker_destino.get_directory_path()),
            ],
        ),
        ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.ElevatedButton(text='Gerar pdf',bgcolor=ft.colors.GREEN,on_click=criar_pdf)
            ]
        ),
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[progress]
        )

    )

ft.app(target=main)