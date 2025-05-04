from google.adk import Agent
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
import os

from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# LiteLLM uses different ENV variables for OpenAI and OpenTelemetry fields.
# os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE")
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

openai_model = LiteLlm(model="openai/gpt-3.5-turbo")

plan_agent = LlmAgent(
    name="plan_agent",
    model=openai_model,
    description="根据原始需求提供技术方案规划。",
    instruction="""
        你是一个技术方案规划专家。
        协调员会提供原始需求，你需要：
        
        输入处理：
        - 解析用户需求中的功能关键词（如"支付"→支付网关对接、交易记录管理）
        - 识别非功能性需求（性能：支持1000 QPS / 安全：PCI DSS合规）
        
        输出要求：
        1. 生成模块化拆分方案（示例格式）：
           ```json
           {
            "modules": [
               {
            "name": "user-service",
                 "scope": "身份验证/权限管理",
                 "dependency": ["database-service"],
                 "complexity": "High"
               }
             ],
             "milestones": [
               {
            "phase": "设计",
                 "duration": "2周",
                 "deliverable": "系统架构图"
               }
             ]
           }
        2. 技术选型建议：
        数据库：根据事务频率推荐SQL/NoSQL
        部署架构：单体 vs 微服务
        3. 风险评估：
        标注第三方API依赖风险
        识别潜在的技术债务
   """
)
