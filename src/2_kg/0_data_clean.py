import pandas as pd
import json


def data_clean():
    """
    路径抽取
    :return:
    """
    input_path = "../../data/2_kg/fd_data_clean_20250414.json"

    with open(input_path, "r", encoding="utf-8") as f:
        fd_data = json.load(f)

    records = []

    # a2ap2r2s
    a2ap2r2s = fd_data["a2ap2r2s"]
    for a, ap2r2s in a2ap2r2s.items():
        for ap, r2s in ap2r2s.items():
            for r, s in r2s.items():
                records.append([a, ap, r, s])
    # a2r2s
    a2r2s = fd_data["a2r2s"]
    for a, r2s in a2r2s.items():
        for r, s in r2s.items():
            records.append([a, None, r, s])

    # ap2r2s
    ap2r2s = fd_data["ap2r2s"]
    for ap, r2s in ap2r2s.items():
        for r, s in r2s.items():
            records.append([None, ap, r, s])

    print("计数", len(records))

    df = pd.DataFrame(records, columns=["a", "ap", "r", "s"])
    df.to_csv(
        "../../data/2_kg/fd_data_clean_20250414.csv", index=False, encoding="utf-8"
    )


if __name__ == "__main__":
    data_clean()
