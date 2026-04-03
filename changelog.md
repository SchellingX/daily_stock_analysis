## [3.12.2] - 2026-04-03

### Added
- **Gemini CLI Headless 接入支持**：新增通过子进程调用本地 gemini-cli 的适配逻辑，支持 gemini-cli/ 前缀模型名。
- **Stdin 上下文注入**：实现 System/User Prompt 自动合并并通过标准输入传递，规避命令行长度限制。
- **响应自动清洗**：内置 Markdown 反引号自动剥离逻辑，确保 JSON 解析稳定性。
- **集成测试套件**：新增 tests/test_gemini_integration.py 验证子进程链路。

## [3.12.2] - 2026-04-03

### Added
- **Gemini CLI Headless 接入支持**：新增通过子进程调用本地  的适配逻辑，支持  前缀模型名。
- **Stdin 上下文注入**：实现 System/User Prompt 自动合并并通过标准输入传递，规避命令行长度限制。
- **响应自动清洗**：内置 Markdown 反引号自动剥离逻辑，确保 JSON 解析稳定性。
- **集成测试套件**：新增  验证子进程链路。

# Changelog - daily_stock_analysis

## [3.12.1] - 2026-04-02

### Changed

- **分支重构**：从 `upstream/main` 强制同步并切换至新实验分支 `experiment-gemini-cli`。
- **清理**：永久删除旧有的 `gemini-cli` 分支。
- **集成准备**：编写了针对 Headless 模式调用 Gemini CLI 的集成测试计划 `test-plan.md`。
