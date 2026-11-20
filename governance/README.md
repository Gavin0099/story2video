# story2video 開發治理

AI Governance Framework 固定於 `additional/ai-governance-framework`。[`framework.lock.json`](framework.lock.json) 記錄來源與 commit。[`contract.yaml`](../contract.yaml) 保留 Episode v1 驗證器並接上治理基線。一般 `s2v` 指令與 M0 測試仍可獨立執行。

## 新 checkout

在 repo 根目錄初始化框架並安裝 Git hooks。Windows 使用 Git for Windows。

```sh
git submodule update --init -- additional/ai-governance-framework
cd additional/ai-governance-framework
python -X utf8 -m governance_tools.hook_installer --repo ../.. --framework-root . --hooks-only
cd ../..
```

`pre-commit` 會檢查計畫的更新日期與治理訊號。計畫超過 60 天未更新時，框架會擋下 commit。`pre-push` 會掃描本次 push 將新增可達的 Git JSON 物件，並執行框架 runtime smoke。兩支 hook 均安裝在目前 clone 的 `.git/hooks/`。

## 驗收

```sh
python -X utf8 additional/ai-governance-framework/governance_tools/hook_install_validator.py --repo . --framework-root additional/ai-governance-framework --format human
python -X utf8 additional/ai-governance-framework/governance_tools/governance_drift_checker.py --repo . --framework-root additional/ai-governance-framework --format human
python -X utf8 additional/ai-governance-framework/governance_tools/external_repo_smoke.py --repo . --contract contract.yaml --format human
uv run --locked python governance/verify.py
```

Episode v1 契約驗證涵蓋合法、非法與缺少證據三種情境。故事審核、媒體品質與公開發布權限屬於後續產品里程碑。
