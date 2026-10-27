import pandas as pd

# ===== 1. 讀取合併好的資料 =====
setup = pd.read_csv("../data/processed/setup_all.csv", dtype=str)
dissolve = pd.read_csv("../data/processed/dissolve_all.csv", dtype=str)


# ===== 2. 民國日期轉西元 =====
def roc_to_date(text):
    try:
        year = int(text[:3]) + 1911
        return pd.Timestamp(f"{year}-{text[3:5]}-{text[5:7]}")
    except Exception:
        return pd.NaT

setup["setup_date"] = setup["核准設立日期"].apply(roc_to_date)
dissolve["dissolve_date"] = dissolve["核准解散日期"].apply(roc_to_date)

print("設立日期轉換失敗：", setup["setup_date"].isna().sum(), "筆")
print("解散日期轉換失敗：", dissolve["dissolve_date"].isna().sum(), "筆")


# ===== 3. 處理重複：都保留日期最早的 =====
setup = setup.sort_values("setup_date").drop_duplicates("統一編號", keep="first")
dissolve = dissolve.sort_values("dissolve_date").drop_duplicates("統一編號", keep="first")


# ===== 4. 篩選 2015 年設立的公司 =====
cohort = setup[setup["setup_date"].dt.year == 2015].copy()
print("2015 年設立的公司：", len(cohort), "家")


# ===== 5. 用統編配對解散資料 =====
df = cohort.merge(
    dissolve[["統一編號", "dissolve_date"]],
    on="統一編號",
    how="left",
)


# ===== 6. 計算 event 和存活月數 =====
CUTOFF = pd.Timestamp("2026-09-30")

df["event"] = df["dissolve_date"].notna().astype(int)
df["end_date"] = df["dissolve_date"].fillna(CUTOFF)
df["duration_months"] = (df["end_date"] - df["setup_date"]).dt.days / 30.44


# ===== 7. 整理共變數 =====
df["county"] = df["公司所在地"].str[:3]
df["capital"] = pd.to_numeric(df["資本額"], errors="coerce")


# ===== 8. 檢查異常並存檔 =====
print("存活月數 <= 0 的公司：", (df["duration_months"] <= 0).sum(), "家")
df = df[df["duration_months"] > 0]

final = df[[
    "統一編號", "公司名稱", "county", "capital",
    "setup_date", "dissolve_date", "end_date",
    "duration_months", "event",
]]
final.to_csv("../data/processed/survival_2015.csv", index=False)

print()
print("最終公司數：", len(final))
print("已解散：", final["event"].sum(), "家")
print("解散比例：", round(final["event"].mean() * 100, 1), "%")
print()
print(final.head())