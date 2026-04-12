# -*- coding: utf-8 -*-
import sys
import os
import logging

# 配置日志输出到终端
logging.basicConfig(level=logging.INFO)

# 确保能加载 src 模块
sys.path.append(os.getcwd())

from src.analyzer import GeminiAnalyzer
from src.config import get_config
from unittest.mock import patch

def test_routing():
    config = get_config()
    
    # 强制设置主模型为 gemini-cli，触发我们的新逻辑
    config.litellm_model = "gemini-cli/gemini-2.0-flash"
    config.litellm_fallback_models = [] # 清空 fallback
    
    analyzer = GeminiAnalyzer(config=config)
    
    prompt = "Stock: AAPL, Price: 180, Trend: Up"
    system_prompt = "You are a financial analyst. Analyze the data. Return JSON only."
    
    print(f"--- Initiating Routing Test for Model: {config.litellm_model} ---")
    try:
        # 调用核心方法
        # 注意：这里我们直接调用 _call_litellm，它内部会根据 config.litellm_model 进行路由
        text, model_used, usage = analyzer._call_litellm(
            prompt,
            generation_config={"temperature": 0.7},
            system_prompt=system_prompt
        )
        
        print(f"\nSUCCESS!")
        print(f"Model Used: {model_used}")
        print(f"Usage Metadata: {usage}")
        print(f"Raw Output Snippet: {text[:200]}...")
        
        # 验证清洗逻辑
        if "```" in text:
             print("WARNING: Response still contains backticks. Logic might be flawed.")
        else:
             print("CLEANING: Response looks clean (no backticks).")
             
    except Exception as e:
        print(f"\nROUTING FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_routing()
