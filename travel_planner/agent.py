from google.adk import Agent  
from travel_planner.subagents.flight_agent import flight_agent  
from travel_planner.subagents.hotel_agent import hotel_agent  
from datetime import datetime, timedelta  


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

today = datetime.today().date()  

coordinator_agent = LlmAgent(  
    name="TravelCoordinator",  
    model=openai_model,  
    description="主要的协调员代理，收集旅行偏好并查询子代理。",  
    instruction=f"""  
                    你是一个旅行规划协调员。  
                    你的任务是从用户那里收集旅行偏好，并与子代理协调，提供航班、酒店建议和日程安排。  
                    你会收到用户的自然语言输入，并需要提取以下详细信息：  
                      
                    注意，总预算应用于航班和酒店建议，不应超过总额。  
                    如果用户没有指定起始日期，而是提到“下周”、“下个月”或“明年”，则通过取今天的日期作为 {today} 来转换为日期格式。  
                      
                    步骤1：从用户的输入中提取以下详细信息：  
                    - 出发地（出发地点）  
                    - 目的地  
                    - 起始日期（格式：YYYY-MM-DD）  
                    - 结束日期（格式：YYYY-MM-DD）  
                    - 预算金额（数字）  
                    - 预算货币（例如，USD，LKR，$）  
                      
                    步骤2：如果有任何细节缺失或不清楚：  
                    - 对于起始日期：如果用户没有提供，请询问他们是否愿意使用 {today} 或指定首选起始日期。  
                    - 对于结束日期：如果用户只提供了天数，请根据 {today} 或提供的起始日期计算结束日期。  
                      如果没有提供起始日期，请询问用户指定一个首选日期或默认为今天的日期。  
                    - 如果用户未提供预算货币，默认假设为“USD”，除非另有说明。  
                      
                    步骤3：一旦收集到所有详细信息：  
                    - 向用户确认旅行偏好（出发地、目的地、起始日期、结束日期、预算）。  
                    - 如果有任何模糊之处，请向用户确认。  
                      
                    步骤4：将数据发送给相应的代理：  
                    - `flight_agent`用于航班建议  
                    - `hotel_agent`用于酒店建议  
                      
                    步骤5：呈现最终结果，结合两个代理的结果和一天的计划，包括：  
                    - 包含所有详细信息的旅行摘要（出发地、目的地、起始日期、结束日期、预算）  
                    - 注意，总预算应用于航班和酒店建议。它不应超过总额。  
                    - 航班建议  
                    - 酒店建议  
                    - 总估算成本  
                    - 旅行的一天计划示例，包括目的地的活动和参观地点。  
                      
                    在引导用户时，请简洁、清晰且友好。如果遇到任何缺失信息，请要求用户澄清。  
                 """,  
    sub_agents=[flight_agent, hotel_agent]  
)  

root_agent = coordinator_agent