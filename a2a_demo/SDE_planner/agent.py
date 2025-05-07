from google.adk import Agent
from SDE_planner.subagents.plan_agent import plan_agent
from SDE_planner.subagents.design_agent import design_agent
from SDE_planner.subagents.dev_agent import dev_agent
from SDE_planner.subagents.test_agent import test_agent

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

openai_model = LiteLlm(model="openai/deepseek-chat")

today = datetime.today().date()

coordinator_agent = LlmAgent(
    name="SDECoordinator",
    model=openai_model,
    description="主要的协调员代理，收集客户需求并查询子代理。",
    instruction=f"""
        你是一个软件开发项目协调员。
        你的任务是从用户/产品经理处收集需求，并与子代理协同完成软件交付。
        
        处理流程：
        1. 接收自然语言需求输入（示例："我们需要一个电商平台，支持用户注册、商品搜索和支付功能"）
        2. 提取关键业务要素：
           - 核心功能模块（必须实现的功能列表）
           - 技术栈偏好（如未指定则推荐默认方案）
           - 交付时间线（精确到周）
           - 资源约束（团队规模/服务器预算）
        3. 缺失信息处理：
           - 若技术栈未明确，提供3种选项供确认（示例：Python/Django vs Java/Spring）
           - 若交付时间模糊，根据功能复杂度推算建议时间（参考COCOMO模型）
        4. 
           1. 需求分析 转发给 plan_agent
           2. 系统设计 转发给 design_agent
           3. 编码 转发给 dev_agent
           4. 测试 转发给 test_agent
        """,
    sub_agents=[plan_agent, design_agent, dev_agent, test_agent]
)

root_agent = coordinator_agent
