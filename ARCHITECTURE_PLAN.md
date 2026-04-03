# Daily Stock Analysis - 架构升级计划 (v4.0)
> 目标：将单一线性分析升级为“多专家共识引流”架构，并引入胜率跟踪机制。基于 `AI-Hedge-Fund` 理念，适配 A 股/港股数据源，并完全由本地 `gemini-cli` 驱动。

## 1. 核心架构设计

### 1.1 数据输入层 (Data Provider)
保持现有的数据提供者架构，但需确保能向不同的大师输出定制化的上下文：
*   **技术面 (Technicals)**: MACD, RSI, 均线系统 (现有功能)。
*   **基本面 (Fundamentals)**: 财报数据，PE/PB 估值，内部交易 (需针对 A/HK 股适配)。
*   **新闻舆情面 (News & Sentiment)**: 抓取最新新闻与社交情绪 (利用现有搜索引擎集成，并进行 NLP 预处理)。

### 1.2 多专家分析层 (Master Agents)
将 `Analyzer` 从单一调用重构为**并发调用**多个独立的“大师实例”。每个实例通过 `gemini-cli` 运行。

**提议的大师阵容**：
*   **Warren Buffett (基本面专家)**: 专注长期价值、护城河、财报质量。
*   **Paul Tudor Jones (技术/趋势专家)**: 专注均线突破、动量、MACD/RSI 背离。
*   **Cathie Wood (成长/舆情专家)**: 专注创新、新闻热度、社交情绪指标。
*   **Risk Manager (风控专家)**: 只看下行风险，提供强行否决权或缩减仓位建议。

**专家统一输出契约 (JSON)**:
```json
{
  "signal": "buy | sell | hold",
  "confidence": 85,
  "reasoning": "由于 MACD 底背离且支撑位确立，具备反弹动能..."
}
```

### 1.3 战绩追踪与权重引擎 (Performance Tracker)
核心创新点：打破原版 AI-Hedge-Fund 的静态权重，引入**动态胜率惩罚/奖励机制**。

*   **持久化 (SQLite/JSON)**: 引入 `analyst_track_record` 表，记录 `(analyst_id, ticker, date, predicted_signal, actual_5d_return, is_correct)`。
*   **动态置信度 (Dynamic Confidence)**:
    `Final_Confidence = Agent_Confidence * (Rolling_Accuracy_30d ^ 1.5)`
    *(注：使用幂函数放大高胜率专家的权重，削弱低胜率专家的噪音)*

### 1.4 共识决策引擎 (Consensus Aggregator)
类似 `AI-Hedge-Fund` 的 Portfolio Manager，但不做复杂的可用资金推算，专注**方向性评级**。

*   收集所有大师的 `Final_Confidence`。
*   **冲突解决**：如果技术专家看跌（高置信），基本面专家看涨（低置信），共识引擎将倾向于看跌或触发“意见分歧，强制 Hold”的安全阀。
*   **统一输出**：输出给现有的 WebUI 呈现。

---

## 2. 系统数据流向

1. **触发**: WebUI 提交 `[AAPL, 2026-04-03]` 分析请求。
2. **抓取**: Data Provider 并行获取（行情 + 财报 + 舆情）。
3. **分发**: 启动 `asyncio.gather` 并行调用 4 个 `gemini-cli` 实例。
4. **计算权重**: 从本地 DB 查询 4 位专家的近期胜率，对返回的 Confidence 乘算。
5. **共识**: 将加权后的建议喂给 `Consensus_Agent`（也是一个 gemini-cli 实例），得出最终 `[Strong Buy, Buy, Hold, Sell, Strong Sell]`。
6. **归档**: 将今日各专家的原始意见存入 DB，等待 5 个交易日后回填真实涨跌并计算胜率。

---

## 3. WebUI 展现层改造
在前端界面新增：
*   **多方博弈面板**：雷达图或投票柱状图，展示各大师的立场。
*   **胜率榜单**：展示本月预测最准的“分析师”。
*   **深度报告**：保留共识引擎的总结性文字。