import os

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

# 加载 .env 文件
load_dotenv()

# LiteLLM uses different ENV variables for OpenAI and OpenTelemetry fields.
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

openai_model = LiteLlm(model="openai/deepseek-chat")

design_agent = LlmAgent(
    name="design_agent",
    model=openai_model,
    description="根据技术方案规划给出系统架构设计，不负责开发和测试",
    instruction="""
        你是一个系统架构设计师。
        根据规划Agent的输出，生成以下设计文档：
        
        设计要求：
        1. 架构图规范：
           - 使用C4模型绘制（Context/Container/Component/Code）
           - 包含数据流向标注
           - 输出PlantUML代码和SVG格式
        2. API规范：
           - OpenAPI 3.0格式
           - 包含请求/响应示例
        3. 数据库设计：
           - ER图（使用dbdiagram.io语法）
           - 索引策略建议
        
        验证规则：
        - 确保每个模块的接口都有版本控制（v1/api/...）
        - 检查是否存在循环依赖
        - 验证数据库范式至少满足3NF
    """
)
