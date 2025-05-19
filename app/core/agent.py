import asyncio
from langchain.agents import AgentExecutor, Tool, AgentType
from langchain.prompts import ChatPromptTemplate
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from app.core.memory_store import get_memory_for_user

from typing import List, Dict, Any, ClassVar

from app.core.llm import get_gemini_llm
from app.tools.transaction_tool import RecordTransactionTool



class FinanceAgent():
    def __init__(self, user_id):
        self.user_id = user_id
        self.llm = get_gemini_llm()
        self.prompt = self.custom_prompt()
        self.tools = self.initialize_tools()
        self.memory = get_memory_for_user(user_id)
        self.agent = self.create_agent_for_user()
    def initialize_tools(self):

        return [
            RecordTransactionTool(user_id=self.user_id)._run
        ]

    def create_agent_for_user(self):
        agent_executor = create_react_agent(
            model=self.llm,
            tools=self.tools,
            checkpointer=self.memory,
            prompt=self.prompt
        )

        return agent_executor

    def custom_prompt(self):
        
        prompt = prompt = """
You are a smart financial assistant, helping users manage their personal finances.

You can:
1. Record spending transactions
2. Analyze spending and provide insights
3. Create and manage budget plans
4. Create and track spending goals
5. Analyze spending trends
Final Answer: final answer to the user's question

Note:
- Always answer in Vietnamese and use icon
- Number format money with thousands separator
- Provide useful insights and specific recommendations
- Only ask users for REQUIRED fields if they are not present. For optional fields, infer them from the description.
- If there are errors, explaining clearly and suggesting solutions
- Only when the action is successfully performed will feedback be created for the user
"""


        return ChatPromptTemplate.from_messages([
            ("system", prompt),
            ("user", "{messages}")
        ])

    def proccess_message(self, message: str, user_id: int):
        try:
            config = {"configurable": {"thread_id": str(user_id)}}
            result = self.agent.invoke(
                {
                    "messages": [HumanMessage(content=message)],
                }, 
                config,
            )
            # for i in result:
            #     print(i)
            
            return {
                "status": "Oke",
                "respones": result['messages'][-1].content
            }
            
        except Exception as e:
            return { 
                "status": "Error",
                "respones": str(e)
            }


    