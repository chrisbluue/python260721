import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}


def get_kpi200_entry_top(max_page=20):
    result = []

    for page in range(1, max_page + 1):
        url = f"https://finance.naver.com/sise/entryJongmok.naver?type=KPI200&page={page}"
        res = requests.get(url, headers=headers, timeout=20)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")
        table = soup.find("table", class_="type_1")
        if not table:
            raise ValueError(f"{page}페이지의 편입종목상위 테이블을 찾지 못했습니다.")

        for tr in table.select("tr")[1:]:
            if tr.find("th"):
                continue

            tds = tr.find_all("td")
            if len(tds) < 7:
                continue

            row = {
                "종목별": tds[0].get_text(strip=True),
                "현재가": tds[1].get_text(strip=True),
                "전일비": tds[2].get_text(strip=True),
                "등락률": tds[3].get_text(strip=True),
                "거래량": tds[4].get_text(strip=True),
                "거래대금(백만)": tds[5].get_text(strip=True),
                "시가총액(억)": tds[6].get_text(strip=True),
            }

            stock_link = tds[0].find("a")
            if stock_link:
                row["종목코드"] = stock_link["href"].split("code=")[-1]

            result.append(row)

    return result


def save_to_excel(data, filename="kospi200.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws.title = "kospi200"

    columns = [
        "종목별",
        "현재가",
        "전일비",
        "등락률",
        "거래량",
        "거래대금(백만)",
        "시가총액(억)",
        "종목코드",
    ]

    ws.append(columns)
    for row in data:
        ws.append([
            row.get("종목별", ""),
            row.get("현재가", ""),
            row.get("전일비", ""),
            row.get("등락률", ""),
            row.get("거래량", ""),
            row.get("거래대금(백만)", ""),
            row.get("시가총액(억)", ""),
            row.get("종목코드", ""),
        ])

    wb.save(filename)
    print(f"저장 완료: {filename}")


if __name__ == "__main__":
    data = get_kpi200_entry_top(max_page=20)
    print(f"총 수집 건수: {len(data)}")
    save_to_excel(data, "kospi200.xlsx")

