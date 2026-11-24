import csv
import glob

files = sorted(glob.glob("results/eval_*.csv"))
if not files:
    print("results klasöründe sonuç dosyası yok. Önce evaluate.py'yi çalıştır.")
    raise SystemExit

latest = files[-1]
print(f"Dosya: {latest}\n")

stats = {}
with open(latest, encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        if row["error"]:
            continue
        s = stats.setdefault(row["model"], {"n": 0, "sec": 0.0, "tok": 0, "cost": 0.0})
        s["n"] += 1
        s["sec"] += float(row["seconds"])
        s["tok"] += int(row["completion_tokens"] or 0)
        s["cost"] += float(row["cost_usd"] or 0)

print(f"{'Model':<32}{'Ort. süre':>12}{'Ort. token':>12}{'Toplam $':>12}")
print("-" * 68)
for model, s in sorted(stats.items(), key=lambda x: x[1]["sec"] / x[1]["n"]):
    print(f"{model:<32}{s['sec'] / s['n']:>10.2f} sn{s['tok'] / s['n']:>12.0f}{s['cost']:>12.5f}")