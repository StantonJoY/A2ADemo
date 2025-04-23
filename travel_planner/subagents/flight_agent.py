from google.adk import Agent  
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
import os

from dotenv import load_dotenv


# 加载 .env 文件
load_dotenv()
 
# LiteLLM uses different ENV variables for OpenAI and OpenTelemetry fields.
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE")    # deepseek 的 API 地址
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

openai_model=LiteLlm(model="openai/deepseek-chat")

flight_agent = LlmAgent(  
    name="flight_agent",  
    model=openai_model,  
    description="根据出发地、目的地、旅行日期和预算提供建议的航班。",  
    instruction="""  
                  你是一个航班预订代理。协调员会给你以下信息：  
                  - 出发地  
                  - 目的地  
                  - 起始日期  
                  - 结束日期  
                  - 预算金额  
                  - 预算货币  
                    
                  返回1-2个模拟航班选项，包括：  
                  - 航空公司名称  
                  - 出发和返回日期/时间  
                  - 价格（以指定货币表示）  
                  - 班级（经济舱/商务舱）  
                    
                  确保总价格在预算范围内。  
                 """  
)