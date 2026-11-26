"""Why five of the 36 reads marked a core `partial`.

Reads only the evidence already on disk. Makes no model calls.

A core verdict is one half of the gate: `clear` requires every core to be
`supported`, so a single `partial` fails a panel whatever the scores are. This
pulls each disagreement next to the reads that marked the same core supported,
so the two readings can be compared in their own words.

Writes cores-divergence.md.
"""
import glob
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def final_reply(path):
    """The last stage's parsed reply, wherever the transcript nests it."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    found = []

    def walk(obj):
        if isinstance(obj, dict):
            if isinstance(obj.get("cores"), list) and "scores" in obj:
                found.append(obj)
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for v in obj:
                walk(v)
        elif isinstance(obj, str) and '"cores"' in obj:
            try:
                walk(json.loads(obj))
            except Exception:
                pass

    walk(data)
    return found[-1] if found else None


def collect():
    reads = []
    for path in sorted(glob.glob(os.path.join(HERE, "evidence", "panel-*",
                                              "*", "reader-*.json"))):
        rel = os.path.relpath(path, os.path.join(HERE, "evidence"))
        parts = rel.replace("\\", "/").split("/")
        reply = final_reply(path)
        if not reply:
            continue
        reads.append({
            "panel": parts[0].replace("panel-", ""),
            "version": parts[1],
            "reader": parts[2].replace(".json", ""),
            "cores": {c.get("label"): c for c in reply["cores"]},
            "critical_issues": reply.get("critical_issues") or [],
            "path": "evidence/" + rel.replace("\\", "/"),
        })
    return reads


def main():
    reads = collect()
    divergent = [(r, label) for r in reads for label, c in r["cores"].items()
                 if c.get("support") != "supported"]

    L = ["# `cores` 分歧：五筆 partial 的原因", "",
         "只讀既有 %d 筆盲評證據，**沒有新增任何模型呼叫**。" % len(reads), "",
         "`cores` 是 gate 的另一半必要條件：`clear` 要求每個 core 都是 `supported`，",
         "所以單一個 `partial` 就會讓整組不通過，不論分數多高。04-v7 的 B 組",
         "三位讀者都給 91 分仍然 FAIL，原因就在這裡。", ""]

    by_version = {}
    for r, label in divergent:
        by_version.setdefault(r["version"], []).append((r, label))

    L += ["## 分歧分布", "",
          "| 劇本 | partial 次數 | 爭議的 core |", "| --- | ---: | --- |"]
    for ver in sorted(by_version):
        items = by_version[ver]
        labels = sorted({label for _, label in items})
        L.append("| %s | %d / %d | %s |"
                 % (ver, len(items),
                    sum(1 for r in reads if r["version"] == ver),
                    "、".join(labels)))
    L.append("")

    L += ["**五筆的 `critical_issues` 全部為空。**", "",
          "沒有任何一筆說故事有缺陷、說不通或讀不懂。五筆的結構完全一樣：",
          "線索**支持**預定答案，但**無法排除**另一個同樣成立的動機。", ""]

    for ver in sorted(by_version):
        L += ["## %s" % ver, ""]
        for r, label in by_version[ver]:
            c = r["cores"][label]
            L += ["### %s 組 %s — `%s`" % (r["panel"], r["reader"], label), "",
                  "> %s" % c.get("reason", "").strip(), "",
                  "判定：`%s`　critical_issues：%s　證據：[%s](%s)"
                  % (c.get("support"), r["critical_issues"] or "無",
                     r["path"], r["path"]), ""]
        # the same core, as read by everyone who marked it supported
        labels = {label for _, label in by_version[ver]}
        supported = [(r, label, r["cores"][label])
                     for r in reads if r["version"] == ver
                     for label in labels
                     if label in r["cores"]
                     and r["cores"][label].get("support") == "supported"]
        if supported:
            L += ["### 同一個 core 被判為 supported 的讀法", ""]
            for r, label, c in supported:
                L += ["**%s 組 %s**：%s" % (r["panel"], r["reader"],
                                            c.get("reason", "").strip()), ""]

    L += ["## 觀察", "",
          "五筆的理由都不是「看不懂」或「故事有破綻」，而是「題面還不能排除",
          "另一個動機」。以 04-v7 為例，該讀者明確寫出修正搶進聲音是**合理解釋**，",
          "只是認為拖延截止的動機也仍然成立。",
          "",
          "這指向一個規約層面的張力，而不是讀者的錯誤：",
          "",
          "- 海龜湯要求揭曉前讓觀眾有**多種合理猜測**；",
          "- `cores` 要求謎底有**充分的題面證據支持**。",
          "",
          "若讀者把「充分支持」理解成「排除所有其他答案」，刻意保留的懸疑就會",
          "被記成缺陷。同一份稿在不同組之間 supported ↔ partial 的擺盪，可能就是",
          "這個理解差異，而不是故事品質的差異。",
          "",
          "**本文件不主張修改規約。** 要判斷哪一種理解才對，需要真人讀者是否也",
          "提出同樣的替代動機 — 那是真人盲測要回答的問題，不是再跑一輪 AI 盲評",
          "能回答的。評審穩定性研究已標記為 PAUSED。"]

    out = os.path.join(HERE, "cores-divergence.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("reads: %d   divergent core verdicts: %d" % (len(reads), len(divergent)))
    for ver in sorted(by_version):
        print("  %s: %d" % (ver, len(by_version[ver])))
    print("->", out)


if __name__ == "__main__":
    main()
