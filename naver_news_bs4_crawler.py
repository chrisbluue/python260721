import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import time

# 네이버 뉴스 검색 URL
query = "반도체"
search_url = f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={quote(query)}"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8"
}


def get_news_items(search_url, max_count=5):
    res = requests.get(search_url, headers=headers, timeout=20)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    items = []

    # 검색 결과의 기사 제목 링크
    for title_a in soup.select('a[data-heatmap-target=".tit"]'):
        href = title_a.get("href")
        if not href:
            continue

        # 제목에서 텍스트 추출
        title = title_a.get_text(" ", strip=True)

        # 같은 기사 묶음에서 요약문 추출
        parent = title_a.find_parent("div", class_=lambda c: c and "sds-comps-vertical-layout" in c)
        if parent:
            summary_tag = parent.select_one('a[data-heatmap-target=".body"]')
            summary = summary_tag.get_text(" ", strip=True) if summary_tag else ""

            press_tag = parent.select_one('.sds-comps-profile-info-title-text')
            press = press_tag.get_text(" ", strip=True) if press_tag else ""

            items.append({
                "title": title,
                "url": href,
                "summary": summary,
                "press": press
            })

        if len(items) >= max_count:
            break

    return items


def extract_article_text(article_url):
    try:
        res = requests.get(article_url, headers=headers, timeout=20)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        selectors = [
            "#articleBody",
            "article",
            "#newsEndContents",
            "#articleView",
            ".news_body",
            ".article_body",
            ".article-body",
            ".view_con",
            ".news_cnt"
        ]

        for selector in selectors:
            tag = soup.select_one(selector)
            if tag:
                text = tag.get_text("\n", strip=True)
                if text:
                    return text

        body = soup.select_one("body")
        if body:
            text = body.get_text("\n", strip=True)
            if text:
                return text

        return ""

    except Exception as e:
        return f"본문 추출 실패: {e}"


# 1) 네이버 검색 결과에서 기사 링크 수집
news_items = get_news_items(search_url, max_count=5)

for i, item in enumerate(news_items, start=1):
    print(f"\n[{i}] {item['press']}")
    print("제목:", item["title"])
    print("링크:", item["url"])
    print("요약:", item["summary"][:200])

    # 2) 기사 본문 추출
    content = extract_article_text(item["url"])
    print("본문 미리보기:")
    print(content[:600])
    print("-" * 80)

    time.sleep(1)
