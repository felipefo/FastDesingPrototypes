from abc import ABC, abstractmethod
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from dotenv import load_dotenv


class AgenteNodeTemplate(ABC):
    
    
    prompt = ""
    agent : AgentExecutor
    tools : list
    novo_estado: str
    system_message : str
    human: str
    model: str
    
    def __init__(self, system: str = "", human: str = "",novo_estado: str = "",tools: list = None, model: str="gemini-2.5-flash-preview-04-17" ):
     
        self.system = system
        self.human = human
        self.novo_estado = novo_estado
        self.tools = tools or []
        self.model = model
    
    def run(self, state: dict) -> dict:
        print(f"▶️ Executando node: {self.__class__.__name__}")
        
        self.agent = self.build_agent() 
        result = self.run_agent(state)
        resultado = self.outputParser(result)
        return resultado 

   
    def build_agent(self):   
        load_dotenv()  # Carrega as variáveis do .env
        os.environ["GOOGLE_API_KEY"] =  os.getenv("GOOGLE_API_KEY")
        if os.getenv("GOOGLE_MODEL"):
            self.model =  os.getenv("GOOGLE_MODEL")
        
        # Modelo   #
        llm = ChatGoogleGenerativeAI(model=self.model)
        # Lista de tools
        tools = self.tools
        self.prompt = ChatPromptTemplate.from_messages([
          ("system", self.system),
          ("human", self.human),
            MessagesPlaceholder(variable_name="agent_scratchpad")])
        # Criar agente com suporte a tools
        agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=self.prompt)
        # Armazenar um executor
        self.agent = AgentExecutor(agent=agent, tools=tools, verbose=False,  max_iterations=5 )
        return self.agent

    @abstractmethod
    def preparar_prompt(self, state: dict) -> dict:
        return state 

    def run_agent(self, state: dict):
        entrada = self.preparar_prompt(state)
        #resultado = ""
        resultado = self.agent.invoke(entrada)
        #print("🧾 Resultado do agente:", resultado)
        return resultado


    def outputParser(self, state: dict) -> dict:
        # Detecta chave relevante
        state[self.novo_estado] = state.get("output", None)
        return state    
   
