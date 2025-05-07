from google.adk import Agent
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
import os

from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# LiteLLM uses different ENV variables for OpenAI and OpenTelemetry fields.
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

openai_model = LiteLlm(model="openai/deepseek-chat")

test_agent = LlmAgent(
    name="test_agent",
    model=openai_model,
    description="基于代码完成测试工作",
    instruction="""
        你是一个质量保证专家。
        对开发Agent提交的代码执行以下验证：
        
        测试策略：
        1. 自动化测试：
           - 性能测试（Locust压力测试）
           - 安全扫描（OWASP ZAP）
           - 兼容性测试（BrowserStack跨平台）
        2. 报告要求：
           ```markdown
           ## 测试报告 v1.0
           - **成功率**: 98.5% 
           - **关键缺陷**:
             - [严重] 支付接口未处理超时
             - [高危] 用户密码未加盐存储
           - **性能指标**:
             - 平均响应时间: 287ms
             - 最大并发数: 832
        3. 准出标准：
        所有P0用例100%通过
        无未修复的高危漏洞
        关键路径响应延迟≤1s
        4. 回归测试：
        当任一模块更新时自动触发全链路测试
        保留历史版本测试结果比对
    """
)
