import csv
from pathlib import Path

from fastapi import FastAPI, HTTPException

app = FastAPI(title="Zoo Visitors API - Mee 035")

DATA_FILE = Path(__file__).parent / "zoo.csv"


@app.get("/api/zoo-visitors")
def get_zoo_visitors():
    if not DATA_FILE.exists():
        raise HTTPException(status_code=503, detail="ไม่พบไฟล์ zoo.csv")

    records = []

    with DATA_FILE.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if not row.get("สวนสัตว์", "").strip():
                continue

            monthly = {}
            for column, value in row.items():
                if not column or column in (
                    "รายการ", "สวนสัตว์", "ปีงบประมาณ"
                ):
                    continue

                text = (value or "").strip().replace(",", "")
                # ช่องว่างหรือเครื่องหมายขีดคงเป็น null ไม่เดาว่าเป็นศูนย์
                monthly[column.strip()] = (
                    int(text) if text.isdigit() else None
                )

            records.append({
                "zoo": row["สวนสัตว์"].strip(),
                "visitor_type": row["รายการ"].strip(),
                "fiscal_year": int(row["ปีงบประมาณ"].strip()),
                "monthly_visitors": monthly,
            })

    return {
        "source": {
            "organization": "องค์การสวนสัตว์แห่งประเทศไทย ในพระบรมราชูปถัมภ์",
            "dataset": "zoo-visitors2569",
            "url": "https://data.go.th/dataset/zoo-visitors2569",
            "file": DATA_FILE.name,
        },
        "fiscal_year": 2569,
        "total_records": len(records),
        "records": records,
    }