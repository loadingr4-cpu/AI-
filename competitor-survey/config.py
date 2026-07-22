COMPETITORS = [
    {
        "name": "明光義塾",
        "search_keywords": ["明光義塾", "明光 個別指導 講師 大阪", "明光義塾 バイト 関西"],
        "recruitment_url": "https://www.meiko-flap.jp/recruit/",
    },
    {
        "name": "個別指導Axis",
        "search_keywords": ["個別指導Axis", "アクシス 講師 大阪", "Axis 個別指導 バイト 関西"],
        "recruitment_url": "https://www.axis-net.jp/teacher/",
    },
    {
        "name": "個別指導塾スタンダード",
        "search_keywords": ["個別指導塾スタンダード", "スタンダード 講師 大阪", "スタンダード 個別指導 バイト 関西"],
        "recruitment_url": "https://standard-ac.jp/teacher/",
    },
    {
        "name": "個別指導WAM",
        "search_keywords": ["個別指導WAM", "WAM 講師 大阪", "WAM 個別指導 バイト 関西"],
        "recruitment_url": "https://www.wam-tochigi.com/",
    },
    {
        "name": "個別指導学院ヒーローズ",
        "search_keywords": ["ヒーローズ 講師 大阪", "個別指導学院ヒーローズ バイト 関西"],
        "recruitment_url": "https://heroes-t.net/recruit/",
    },
    {
        "name": "個別教室のトライ",
        "search_keywords": ["個別教室のトライ 講師 大阪", "トライ 個別指導 バイト 関西"],
        "recruitment_url": "https://www.trygroup.co.jp/recruit/",
    },
    {
        "name": "個別指導学院フリーステップ",
        "search_keywords": ["フリーステップ 講師 大阪", "個別指導学院フリーステップ バイト 関西"],
        "recruitment_url": "https://www.hamasemi.com/freestep/",
    },
    {
        "name": "東進個別指導学院",
        "search_keywords": ["東進個別指導学院 講師 大阪", "東進 個別指導 バイト 関西"],
        "recruitment_url": "https://www.toshinkobetsu.jp/teacher/",
    },
    {
        "name": "ITTO個別指導学院",
        "search_keywords": ["ITTO 講師 大阪", "ITTO個別指導学院 バイト 関西"],
        "recruitment_url": "https://www.itto.jp/teacher/",
    },
    {
        "name": "学研個別指導教室",
        "search_keywords": ["学研個別指導教室 講師 大阪", "学研 個別指導 バイト 関西"],
        "recruitment_url": "https://brand.gakken-plus.co.jp/kyoshitsu/",
    },
]

JOB_BOARDS = [
    "https://jp.indeed.com/jobs?q={query}&l=%E5%A4%A7%E9%98%AA%E5%BA%9C",
    "https://baito.mynavi.jp/search/?keyword={query}&pref=27",
]

SURVEY_SCHEMA = {
    "name": "str - 塾名",
    "teaching_format": "str - 指導形態（例: 1:1, 1:2, 1:3, 1:4）",
    "hourly_pay_min": "int|null - 時給（下限）円",
    "hourly_pay_max": "int|null - 時給（上限）円",
    "session_pay": "int|null - コマ給 円",
    "session_minutes": "int|null - 1コマの授業時間（分）",
    "benefits": "list[str] - 福利厚生リスト",
    "employment_type": "str - 雇用形態",
    "target_grades": "str - 対象学年",
    "source_url": "str - 参照URL",
    "notes": "str - 備考・特記事項",
}
