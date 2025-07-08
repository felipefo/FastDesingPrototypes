from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableLambda
from typing import TypedDict
from pydantic import BaseModel
from agents_builder.AgenteNodeAtualizarCodigo import AgenteNodeAtualizarCodigo

class EstadoInputPrototipoUpdate(BaseModel):
    ajustes: str
    pasta: str

class EstadoPrototipoUpdate(TypedDict):
    ajustes: str
    input: str
    pasta: str
    codigo: str

async def update_prototipo(data: EstadoInputPrototipoUpdate):
    
    print("informacoes recebidas:")
    print(data.ajustes)
    print(data.pasta)
    
    estado: EstadoPrototipoUpdate = {
        "ajustes": data.ajustes,
        "input": "",
        "pasta": data.pasta,
        "codigo": "",
    }

    workflow = StateGraph(EstadoPrototipoUpdate)
    workflow.add_node("update_codigo", RunnableLambda(AgenteNodeAtualizarCodigo().run))
    workflow.set_entry_point("update_codigo")
    workflow.set_finish_point("update_codigo")
    resultado = workflow.compile().invoke(estado)
    print(resultado)
    return resultado