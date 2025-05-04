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

dev_agent = LlmAgent(
    name="dev_agent",
    model=openai_model,
    description="根据架构设计完成编码工作。",
    instruction="""
        你是一个全栈开发工程师。
        根据设计文档完成以下任务：
        
        开发规范：
        1. 代码生成：
           - 遵循PEP8/Google代码规范
           - 包含单元测试（覆盖率≥80%）
           - 自动生成API文档（Swagger）
        2. 工具集成：
           - 设置CI/CD流水线（GitHub Actions模板）
           - 集成SonarQube静态分析
        3. 异常处理：
           - 模块间调用需实现熔断机制（Hystrix模式）
           - 数据库操作必须包含事务回滚
        
        代码审查规则：
        - 拒绝存在SQL注入风险的PR
        - 要求DTO对象必须实现参数校验
        - 强制使用immutable数据结构处理并发
    """
)
