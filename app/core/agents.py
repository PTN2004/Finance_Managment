import asyncio
from langgraph.prebuilt import create_react_agent
from langchain.agents import Tool
from langchain.tools import StructuredTool
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from app.core.memory_store import get_memory_for_user
from langchain.prompts import ChatPromptTemplate
from app.core.llm import get_gemini_llm

from app.tools.transaction_tool import RecordTransactionTool, RecordTransactionInput

# 1. Khởi tạo mô hình ngôn ngữ
llm = get_gemini_llm()
# 2. Định nghĩa công cụ ví dụ
def get_current_balance() -> str:
    return "Số dư hiện tại là 5.000.000 VND."

tools = [
   RecordTransactionTool(user_id=123)
]

# prompt = """
# You are a smart financial assistant, helping users manage their personal finances.

# You can:
# 1. Record spending transactions
# 2. Analyze spending and provide insights
# 3. Create and manage budget plans
# 4. Create and track spending goals
# 5. Analyze spending trends
# Final Answer: final answer to the user's question

# Note:
# - Always answer in Vietnamese
# - Number format money with thousands separator
# - Provide useful insights and specific recommendations
# - If there are errors, explaining clearly and suggesting solutions
# - Only when the action is successfully performed will feedback be created for the user
# """

prompt = """
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
- If there are errors, explaining clearly and suggesting solutions
- Only when the action is successfully performed will feedback be created for the user
"""

custom_prompt = ChatPromptTemplate.from_messages([
    ("system", prompt),
    ("user", "{messages}")
])

# 3. Khởi tạo memory để dùng checkpoint
# memory = MemorySaver()

memory = get_memory_for_user(123)
# 4. Tạo agent với LangGraph
agent = create_react_agent(
    model=llm,
    tools=tools,
    checkpointer=memory,
    prompt=custom_prompt

)

# 5. Hàm chạy agent
def run_agent(messages):
    config = {"configurable": {"thread_id": "abc123"}}
    result = agent.stream({
        "messages": [HumanMessage(content=messages)]},
        config
    )
    for i in result:
        print(i)
# 6. Chạy chương trình

test_inputs = [
    "Tôi ăn sáng hết 40k",
    "Tôi ăn một ổ bánh mì 12k ở trước trường trả bằng tiền tài khoản.",
]

# 7. Hàm chạy test như người dùng chat
def test_agent_messages():
    config = {"configurable": {"thread_id": "123"}}

    for i, input_text in enumerate(test_inputs, 1):
        print(f"\n--- Test case {i}: {input_text}")
        result = agent.stream(
            {   "messages": [HumanMessage(content=input_text)],
            },
            config
        )
        for i in result:
            print(i)
        # print("✅ Agent response:", result["messages"][-1].content)
test_agent_messages()
# run_agent("Tôi ăn một ổ bánh mì 12k ở trước trường, ghi chi tiêu bằng tài khoản.")
