import pandas as pd

class FormatarPlanilha:
    def __init__(self,path):
        self.path = path

    def __formatar_planilha(self):
        database = pd.read_excel(self.path,
                                 engine='openpyxl',
                                 dtype={'Material Code': str, 'Material Document No': str, 'Production Order': str})
        database = database.dropna(subset=['Material Document No'])
        database['Posting Date'] = pd.to_datetime(database['Posting Date'])
        database["Posting Date"] = database["Posting Date"].dt.strftime("%d/%m/%Y")
        database['Qty in KG'] = database["Qty in KG"] * -1
        database["Production Order"] = database["Production Order"].fillna("Não possui ordem de produção")
        return database

    def gerar_lista_de_dados(self):
        lista_dados = []
        for i, row in self.__formatar_planilha().iterrows():
            dados = {
                "Production Order": row["Production Order"],
                "Material Code": row["Material Code"],
                "Material Description": row["Material Description"],
                "Material Document No": row["Material Document No"],
                "Posting Date": row["Posting Date"],
                "Qty in KG": row["Qty in KG"],
                "User Name": row["User Name"],
            }
            lista_dados.append(dados)
        return lista_dados