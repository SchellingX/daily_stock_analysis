# -*- coding: utf-8 -*-
import subprocess
import json
import os
import sys

def test_gemini_cli_headless():
    print("=== Testing Gemini CLI Headless Mode ===")
    
    # 1. 基础环境检查
    try:
        version_res = subprocess.run(["gemini", "--version"], capture_output=True, text=True)
        print(f"Gemini CLI Version: {version_res.stdout.strip()}")
    except FileNotFoundError:
        print("ERROR: 'gemini' command not found in PATH.")
        return False

    # 2. 构造模拟上下文 (Stdin)
    mock_context = {
        "stock": "AAPL",
        "price": 180.5,
        "ma5": 178.0,
        "ma10": 175.0,
        "indicator": "Golden Cross (Bullish)"
    }
    stdin_input = json.dumps(mock_context, indent=2)
    
    # 3. 构造 Prompt (-p)
    # 明确要求 JSON 输出，且不带 Markdown 反引号
    prompt = "Analyze the technical data provided in stdin. Return a JSON with 'sentiment' (0-100) and 'summary' (string). Output ONLY raw JSON."

    # 4. 执行调用
    print(f"Sending context via Stdin (length: {len(stdin_input)} chars)...")
    try:
        # 移除 --output-format json，直接获取纯净 stdout
        cmd = ["gemini", "-p", prompt]
        
        env = os.environ.copy()
        
        res = subprocess.run(
            cmd,
            input=stdin_input,
            capture_output=True,
            text=True,
            encoding='utf-8',
            env=env,
            timeout=60
        )
        
        # 5. 结果校验
        if res.returncode != 0:
            print(f"FAILURE: Return code {res.returncode}")
            print(f"Stderr: {res.stderr}")
            return False
            
        # 直接拿文本
        output = res.stdout.strip()
        print(f"Raw Output: {output}")
        
        # 即使直接拿文本，由于我们的 Prompt 要求 JSON，AI 还是可能返回带有反引号的内容
        # 我们在这里模拟清洗逻辑
        content = output
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        try:
            data = json.loads(content)
            print(f"SUCCESS: Parsed JSON -> {data}")
            return True
        except json.JSONDecodeError:
            print("FAILURE: Output is not valid JSON even after cleaning.")
            return False

    except subprocess.TimeoutExpired:
        print("FAILURE: Request timed out (60s)")
        return False
    except Exception as e:
        print(f"FAILURE: Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_gemini_cli_headless()
    sys.exit(0 if success else 1)
