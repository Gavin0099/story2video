# AI Governance Framework 導入

本專案採用上游定義的 [external contract repo](https://github.com/Gavin0099/ai-governance-framework/blob/b8a16828481e6b537c474d4e2e4be4d3e047e3e8/docs/ADOPTION_MODEL.md#3-external-contract-repo)。`contract.yaml` 引用專案工作指引、計畫與 Episode v1 validator。CLI 與一般 CI 可獨立執行。框架 checkout 僅用於手動驗證契約。

| 能力 | M0 狀態 |
| --- | --- |
| 工作範圍與驗收指引 | 見 `AGENTS.md` 與 `PLAN.md` |
| 框架契約與 Episode v1 validator | 可隨指定上游 commit 手動驗證 |
| 框架 runtime、Git hooks、F-7 更新與記憶治理 | 留待另行決定 |

## 契約驗收

在本 repo 根目錄執行。框架 checkout 放在 repo 外或 gitignored 的 `artifacts/`。

```sh
git clone https://github.com/Gavin0099/ai-governance-framework.git artifacts/governance-framework
git -C artifacts/governance-framework checkout --detach b8a16828481e6b537c474d4e2e4be4d3e047e3e8
uv run --locked python governance/verify.py --framework-root artifacts/governance-framework
```

驗證器使用上游勘驗介面載入契約，執行合法、非法與缺少證據三種情境。結果涵蓋分集格式、授權欄位和旁白 ID。故事合理性、媒體品質與人員發布權限由後續里程碑驗收。
