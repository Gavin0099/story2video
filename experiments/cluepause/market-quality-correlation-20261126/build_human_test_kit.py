"""Build the human blind-test kit from scripts that already have AI evidence.

Reuses the same six frozen scripts the reliability benchmark scored, so every
human answer lands next to 6 existing AI reads of the same text. Nothing new is
generated and no model is called.

The participant pack carries neutral codes only: no AI score, no gate result,
no band, no story id. Everything identifying lives in the facilitator key,
which is a separate file the participant must not see.

Writes human-test/ with one directory per script, a blank record form, the
facilitator key and the protocol.
"""
import csv
import hashlib
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "human-test")
S2V = r"D:\story2video"
GP = r"D:\s2v-gp"
TEXT_FIELDS = ("first", "second", "reveal", "english")

# Published masters for scripts that also exist as finished video.
VIDEO = {
    "04-v7": ("9rt4gNnVGTw", "刪除試鏡"),
    "05-v6": ("pSsjWQ3I51Y", "舞台門縫"),
    "06-v7": ("bkN-xFKj5nc", "鑰匙複製"),
    "07-v5": ("gspKu9kvup4", "27 號訂單"),
}


def story_sha256(obj):
    return hashlib.sha256(
        "|".join(str(obj.get(k, "")) for k in TEXT_FIELDS).encode("utf-8")
    ).hexdigest()


def load_draft(row):
    src = row["source_path"].replace("\\", "/")
    name = row["version_id"] + ".json"
    if row["source_kind"] == "git":
        ref = row["source_commit"]
        blob = subprocess.run(
            ["git", "show", ref + ":" + os.path.dirname(src) + "/" + name],
            cwd=GP, capture_output=True, text=True, encoding="utf-8")
        if blob.returncode:
            raise RuntimeError("git show failed for " + name)
        draft = json.loads(blob.stdout)
    else:
        with open(os.path.join(S2V, os.path.dirname(src), name),
                  encoding="utf-8-sig") as f:
            draft = json.load(f)
    got = story_sha256(draft)
    if got != row["story_sha256"]:
        raise RuntimeError("%s: story hash mismatch" % row["version_id"])
    return draft


def neutral_code(index):
    return "S%02d" % (index + 1)


PARTICIPANT_QUESTIONS = """\
## 請依序回答，**不要先往下翻**

每一段讀完才翻下一段。沒有標準答案，答不出來就寫「不知道」，那也是有用的資料。

### 第一段讀完

1. 你覺得發生了什麼事？為什麼會這樣？
2. 你有多確定？（0–100）
3. 你想繼續看下去嗎？（1 完全不想 – 5 非常想）為什麼？

### 第二段讀完

4. 現在你的猜測是什麼？和剛才有改變嗎？
5. 是哪一句話或哪一個細節讓你改變或更確定？
6. 除了你的猜測，還有沒有其他同樣說得通的解釋？請寫出來。
7. 你想繼續看下去嗎？（1–5）

### 揭曉讀完

8. 用你自己的話說一次：到底為什麼會這樣？
9. 前面有哪些地方現在回頭看就懂了？
10. 這個答案**公平嗎**？前面給的線索夠不夠讓你推出來？（1 完全不夠 – 5 非常夠）為什麼？
11. 揭曉的那一刻，你覺得**有趣嗎**？（1 無感 – 5 很有意思）為什麼？
12. 你會想再看同一個系列的另一篇嗎？（1–5）為什麼？
13. 看完之後，你心裡還有沒有沒被解釋到、覺得卡卡的地方？
"""


def main():
    with open(os.path.join(HERE, "reliability-sample.csv"), encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["reduced_set"] == "yes"]
    rows.sort(key=lambda r: r["story_sha256"])  # deterministic, hides the band

    os.makedirs(OUT, exist_ok=True)
    key_rows = []
    for i, row in enumerate(rows):
        code = neutral_code(i)
        draft = load_draft(row)
        d = os.path.join(OUT, code)
        os.makedirs(d, exist_ok=True)

        with open(os.path.join(d, "part1.md"), "w", encoding="utf-8") as f:
            f.write("# %s — 第一段\n\n%s\n\n---\n\n讀完請先回答第 1–3 題，"
                    "再翻 part2。\n" % (code, draft["first"]))
        with open(os.path.join(d, "part2.md"), "w", encoding="utf-8") as f:
            f.write("# %s — 第二段\n\n%s\n\n---\n\n讀完請先回答第 4–7 題，"
                    "再翻 reveal。\n" % (code, draft["second"]))
        with open(os.path.join(d, "reveal.md"), "w", encoding="utf-8") as f:
            f.write("# %s — 揭曉\n\n%s\n\n---\n\n請回答第 8–13 題。\n"
                    % (code, draft["reveal"]))
        with open(os.path.join(d, "questions.md"), "w", encoding="utf-8") as f:
            f.write("# %s\n\n%s" % (code, PARTICIPANT_QUESTIONS))

        vid = VIDEO.get(row["version_id"])
        key_rows.append({
            "neutral_code": code,
            "version_id": row["version_id"],
            "band": row["band"],
            "story_sha256": row["story_sha256"],
            "original_readers": row["original_readers"],
            "ai_panel_a": "", "ai_panel_b": "",
            "video_id": vid[0] if vid else "",
            "video_title_zh": vid[1] if vid else "",
            "intended_answer": " ; ".join(draft["cores"].keys()),
            "answer_detail": " ; ".join(str(v) for v in draft["cores"].values()),
        })

    # fill the panel verdicts from the benchmark, for the facilitator only
    res = os.path.join(HERE, "reliability-results.csv")
    if os.path.exists(res):
        with open(res, encoding="utf-8") as f:
            reads = list(csv.DictReader(f))
        for k in key_rows:
            for panel in ("A", "B"):
                v = [r for r in reads
                     if r["version_id"] == k["version_id"] and r["panel"] == panel]
                if len(v) == 3:
                    ok = all(float(x["total"]) >= 90 and x["clear"] == "True"
                             for x in v)
                    k["ai_panel_" + panel.lower()] = "%s %s" % (
                        ",".join(x["total"] for x in v), "PASS" if ok else "FAIL")

    with open(os.path.join(OUT, "facilitator-key.csv"), "w", encoding="utf-8",
              newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(key_rows[0].keys()))
        w.writeheader()
        w.writerows(key_rows)

    # blank record form: one row per participant per script
    fields = ["participant", "neutral_code", "mode", "ran_at_taipei",
              "q1_first_guess", "q2_confidence", "q3_keep_reading",
              "q4_locked_guess", "q5_what_changed_it", "q6_alternatives",
              "q7_keep_reading", "q8_retelling", "q9_recontextualised",
              "q10_fairness_1to5", "q10_why", "q11_interest_1to5", "q11_why",
              "q12_watch_another_1to5", "q12_why", "q13_left_unexplained",
              "core_understood", "raised_the_same_alternative", "facilitator_note"]
    form = os.path.join(OUT, "record-form.csv")
    if not os.path.exists(form):
        with open(form, "w", encoding="utf-8", newline="") as f:
            csv.DictWriter(f, fieldnames=fields).writeheader()

    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as f:
        f.write(PROTOCOL)

    print("scripts prepared: %d" % len(key_rows))
    for k in key_rows:
        print("  %s  (video: %s)" % (k["neutral_code"], k["video_id"] or "none"))
    print("participant pack: human-test/S*/   — no score, no verdict, no band")
    print("facilitator only: human-test/facilitator-key.csv")
    print("->", OUT)


PROTOCOL = """\
# 真人盲測材料（未執行）

重用評審穩定性實驗的同六篇凍結稿，所以每一筆真人回答都能直接對照**同一份文字**
已有的 6 筆 AI 盲評。本目錄只是材料與記錄表，**沒有招募任何人，也沒有執行測試**。

## 給受測者的東西

只有 `S01`–`S06` 六個資料夾，每個含 `part1.md`、`part2.md`、`reveal.md`、
`questions.md`。裡面**沒有** AI 分數、沒有 gate 結果、沒有分數區間、沒有原始
story id，檔名也是中性代碼。

分段順序必須照 part1 → 回答 → part2 → 回答 → reveal → 回答，與 AI 盲評的三階段
相同，否則兩邊不可比。

## 給主持人的東西

`facilitator-key.csv`：中性代碼對照表，含原始版本 id、分數區間、AI 兩組的分數與
判定、預定答案與其題面依據，以及對應的成片 video id（四篇有成片）。
**這個檔案不得讓受測者看到。**

## 記錄

`record-form.csv` 每位受測者每篇一列，欄位對應 `questions.md` 的 13 題，另加三個
由主持人事後編碼的欄位：

- `core_understood`：受測者是否說出預定答案的因果（yes / partial / no）
- `raised_the_same_alternative`：受測者是否自己提出 AI 讀者在 `cores=partial` 時
  提到的那個替代動機（yes / no / n-a）
- `facilitator_note`：原話以外的觀察

編碼口徑要在收資料前先寫定，並保留原話，不要只留編碼。

## 這份測試要回答什麼

**第一個問題：AI 的分數與真人的感受是否一致。** 六篇橫跨三個分數區間，若真人在
82–87 的稿子上給出和 91 分稿子一樣高的「有趣」與「想再看」，那現在投入強化 90 分
門檻的方向就需要重新考慮。

**第二個問題：`cores=partial` 的分歧，真人站哪一邊。** 02-v3、04-v7、06-v7 三篇
有 AI 讀者認為「線索支持預定答案，但無法排除另一個動機」（見
[cores-divergence.md](../cores-divergence.md)）。第 6 題和 `raised_the_same_alternative`
就是為此設計：如果真人也自己提出同一個替代動機，那是規約要求太嚴；如果真人完全
沒想到、而且覺得答案很公平，那是 AI 讀者過度嚴格。

## 這份測試不能回答什麼

- 不能證明市場表現。觀看、留存、訂閱要看 Studio 數據，與此無關。
- 不能用來宣告 gate 有效或無效。樣本小、受測者非隨機、沒有對照組。
- 四篇有成片的可另做有聲首看，但**文字盲測與影片首看要用不同的人**，看過文字的人
  不能再當影片的首次觀看者。

## 規模建議

每篇 3–5 位從未接觸過該故事任何版本的受測者。六篇全做需要 18–30 人次；若人力有限，
先做 `facilitator-key.csv` 裡分數區間最低與最高的各一篇，直接測「82 分 vs 95 分，
真人分得出來嗎」。

執行前需要 Owner 確認招募方式與個資處理；本目錄不含任何受測者資料。
"""


if __name__ == "__main__":
    main()
