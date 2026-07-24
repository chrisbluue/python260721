from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager


BASE = Path.cwd()
XLSX_PATH = BASE / '출생아수__합계출산율__자연증가_등_20260724153629.xlsx'
CLEANED_CSV = BASE / 'birth_rate_cleaned.csv'
PLOT_PATH = BASE / 'births_by_year.png'


def main():
    # 한글 폰트 설정 (시스템에 설치된 한글 폰트 사용)
    preferred_fonts = ['Malgun Gothic', 'Noto Sans KR', 'NanumGothic', 'Batang', 'Gulim']
    available = {f.name for f in font_manager.fontManager.ttflist}
    selected_font = next((font for font in preferred_fonts if font in available), 'DejaVu Sans')
    plt.rcParams['font.family'] = selected_font
    plt.rcParams['axes.unicode_minus'] = False

    df = pd.read_excel(XLSX_PATH, sheet_name='데이터', header=0)

    # 1) 컬럼 정리
    df.columns = [str(col).strip() for col in df.columns]
    if '2025 p)' in df.columns:
        df = df.rename(columns={'2025 p)': '2025'})

    # 2) wide -> long 형태로 변환
    long_df = df.melt(id_vars=['기본항목별'], var_name='year', value_name='value')
    long_df['year'] = pd.to_numeric(long_df['year'], errors='coerce')
    long_df['value'] = pd.to_numeric(long_df['value'], errors='coerce')
    long_df = long_df.dropna(subset=['year', 'value']).sort_values(['기본항목별', 'year']).reset_index(drop=True)

    # 3) 정리된 데이터 저장
    long_df.to_csv(CLEANED_CSV, index=False, encoding='utf-8-sig')

    # 4) 출생아수 시계열 분석
    births = long_df[long_df['기본항목별'] == '출생아수(명)'].copy()
    births['yoy_change_pct'] = births['value'].pct_change() * 100
    births['ma_5'] = births['value'].rolling(window=5, min_periods=1).mean()

    fertility = long_df[long_df['기본항목별'] == '합계출산율(명)'].copy()
    merged = births.merge(fertility, on='year', suffixes=('_births', '_fertility'))

    # 5) 여러 관점의 추가 분석
    pre_2000 = births[births['year'] < 2000]
    post_2000 = births[births['year'] >= 2000]
    summary = {
        '시작년도': int(births['year'].min()),
        '종료년도': int(births['year'].max()),
        '평균출생아수': births['value'].mean(),
        '중앙값': births['value'].median(),
        '최대출생아수': births['value'].max(),
        '최대출생년도': int(births.loc[births['value'].idxmax(), 'year']),
        '최소출생아수': births['value'].min(),
        '최소출생년도': int(births.loc[births['value'].idxmin(), 'year']),
        '출생아수증감률_최초~최종': round((births['value'].iloc[-1] - births['value'].iloc[0]) / births['value'].iloc[0] * 100, 2),
        '2000년이후평균출생아수': round(post_2000['value'].mean(), 2),
        '2000년이전평균출생아수': round(pre_2000['value'].mean(), 2),
        '출생아수와합계출산율상관계수': round(merged['value_births'].corr(merged['value_fertility']), 4),
    }

    print('=== 데이터 정리 결과 ===')
    print(f'원본 행 수: {df.shape[0]} / 원본 열 수: {df.shape[1]}')
    print(f'정리 후 long-form 행 수: {len(long_df)}')
    print(f'저장 파일: {CLEANED_CSV}')
    print('\n=== 출생아수 기본 통계 ===')
    print(births['value'].describe().round(2))
    print('\n=== 분석 요약 ===')
    for k, v in summary.items():
        print(f'{k}: {v}')

    # 6) 라인그래프 생성
    plt.figure(figsize=(12, 6))
    plt.plot(births['year'], births['value'], color='tab:blue', marker='o', linewidth=2, label='연도별 출생아수')
    plt.plot(births['year'], births['ma_5'], color='tab:orange', linewidth=2, linestyle='--', label='5년 이동평균')
    plt.title('대한민국 연도별 출생아수 추이', fontsize=14)
    plt.xlabel('년도')
    plt.ylabel('출생아수(명)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOT_PATH, dpi=200)
    plt.close()

    print(f'\n그래프 저장 완료: {PLOT_PATH}')


if __name__ == '__main__':
    main()
