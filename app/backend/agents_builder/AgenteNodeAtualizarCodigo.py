from .AgenteNodeTemplate import AgenteNodeTemplate
import os
import sys



class AgenteNodeAtualizarCodigo(AgenteNodeTemplate):


    def __init__(self):
        system = "You are an expert senior developer in web interface development for html, css and javascript."
        human = (
            """Update the code to fit the changes required by the user, using HTML, CSS, and JavaScript but do not 
            mess with the previos features already implemented.


Necessary changes to be update in the code: {ajustes}
Code to be update: {codigo}

Attention with this:
-The system needs to be in portuguese. 
-Use the max font-size of 20 and min of 14. 
-The menu should be fixed in the header. 
-Use a color pallet for the buttons, etc. 
-Use localstorage for mocking the features.
-Dot not care about the backend its a frontend prototype.
-All features already implmented should keep working.

Return only a unique code using HTML, CSS, and JavaScript with all implemented.


"""
        )
        tools = []

        super().__init__(
            system=system,
            human=human,
            novo_estado="codigo",
            tools=tools
        )


    def preparar_prompt(self, state: dict) -> dict:
        pasta = state.get("pasta")
        ajustes = state.get("ajustes", "")
        
         
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # agents_builder
        APP_DIR = os.path.abspath(os.path.join(BASE_DIR, "../"))  # volta 1
        UPLOAD_DIR = os.path.join(APP_DIR, "uploads")
        caminho_resultado = os.path.join(UPLOAD_DIR, pasta)
    
        if not os.path.isfile(caminho_resultado):
            raise FileNotFoundError(f"Arquivo {caminho_resultado} não encontrado.")
        with open(caminho_resultado, "r", encoding="utf-8") as f:
            codigo_existente = f.read()

        return {
            "ajustes": ajustes,
            "codigo": codigo_existente
        }   


    def outputParser(self, state: dict) ->dict:
        # Executa a tool de salvar arquivos após o código ser gerado
        codigo = state.get('output')
        state['codigo'] = codigo
        return state



