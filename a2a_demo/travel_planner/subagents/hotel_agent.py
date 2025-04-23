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

hotel_agent = LlmAgent(  
    name="hotel_agent",  
    model=openai_model,  
    description="在给定的旅行日期内找到符合目的地和预算的酒店。",  
    instruction="""  
                  你是一个酒店预订代理。协调员会给你以下信息：  
                  - 目的地  
                  - 起始日期  
                  - 结束日期  
                  - 预算金额  
                  - 预算货币  
                    
                  返回1-2个模拟酒店建议，包括：  
                  - 酒店名称  
                  - 每晚价格和总成本（以给定货币表示）  
                  - 主要设施  
                    
                  确保总价格符合预算。  
                 """  
)