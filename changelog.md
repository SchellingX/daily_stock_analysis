# Changelog - daily_stock_analysis

## [3.13.0] - 2026-04-03

### Added
- **Phase 5: 全量数据接入与 WebUI 渲染**：将“多专家共识架构”（Multi-Expert Ensemble Architecture）完整推向前端。
- **高维评分雷达图**：基于 `recharts` 实现技术、基本、情绪、资金、风险五维评分可视化。
- **大师投票盘 (MasterVotingDisk)**：直观展示多专家系统的多空博弈与权重分布。
- **专家战绩排行 (ExpertLeaderboard)**：动态展示各分析师模块的实时胜率与历史表现。
- **后端适配器**：增强 `AnalysisResult` 逻辑，支持雷达图数据自动聚合与 API 接口下发。

## [3.12.3] - 2026-04-03

### Fixed
- **Git 索引清理**：移除了被忽略但仍在追踪的 `.env.example` 文件，确保符合 `.gitignore` 规范。

## [3.12.2] - 2026-04-03

### Added
- **Gemini CLI Headless 接入支持**：新增通过子进程调用本地 gemini-cli 的适配逻辑，支持 `gemini-cli/...` 前缀模型名。
- **Stdin 上下文注入**：实现 System/User Prompt 自动合并并通过标准输入传递，规避命令行长度限制。
- **响应自动清洗**：内置 Markdown 反引号自动剥离逻辑，确保 JSON 解析稳定性。
- **集成测试套件**：新增 `tests/test_gemini_integration.py` 验证子进程链路。

## [3.12.1] - 2026-04-02

### Changed
- **分支重构**：从 `upstream/main` 强制同步并切换至新实验分支 `experiment-gemini-cli`。
- **清理**：永久删除旧有的 `gemini-cli` 分支。
- **集成准备**：编写了针对 Headless 模式调用 Gemini CLI 的集成测试计划 `test-plan.md`。
