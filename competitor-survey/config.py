SURVEY_REGION = "大阪府"
SURVEY_REGION_NOTE = "大阪府内の複数求人を収集し、最頻値（最もよく見る時給）と範囲（最低〜最高）を記録する"

COMPETITORS = [
    {
        "name": "アップ学習会",
        "is_own_company": True,
        "search_keywords": ["アップ学習会 講師 大阪", "アップ学習会 バイト 大阪府"],
        "recruitment_url": "https://www.up-gakushukai.co.jp/",
    },
    {
        "name": "明光義塾",
        "search_keywords": ["明光義塾 講師 大阪府", "明光義塾 バイト 大阪 時給"],
        "recruitment_url": "https://www.meiko-flap.jp/recruit/",
    },
    {
        "name": "個別指導Axis",
        "search_keywords": ["個別指導Axis 講師 大阪府", "アクシス 塾講師 バイト 大阪 時給"],
        "recruitment_url": "https://www.axis-net.jp/teacher/",
    },
    {
        "name": "個別指導塾スタンダード",
        "search_keywords": ["個別指導塾スタンダード 講師 大阪府", "スタンダード 塾講師 バイト 大阪 時給"],
        "recruitment_url": "https://standard-ac.jp/teacher/",
    },
    {
        "name": "個別指導WAM",
        "search_keywords": ["個別指導WAM 講師 大阪府", "WAM 塾講師 バイト 大阪 時給"],
        "recruitment_url": "https://www.e-wam.jp/",
    },
    {
        "name": "個別指導学院ヒーローズ",
        "search_keywords": ["個別指導学院ヒーローズ 講師 大阪府", "ヒーローズ 塾講師 バイト 大阪 時給"],
        "recruitment_url": "https://heroes-t.net/recruit/",
    },
    {
        "name": "個別教室のトライ",
        "search_keywords": ["個別教室のトライ 講師 大阪府", "トライ 家庭教師 バイト 大阪 時給"],
        "recruitment_url": "https://www.trygroup.co.jp/recruit/",
    },
    {
        "name": "個別指導学院フリーステップ",
        "search_keywords": ["個別指導学院フリーステップ 講師 大阪府", "フリーステップ 塾講師 バイト 大阪 時給"],
        "recruitment_url": "https://www.hamasemi.com/freestep/",
    },
    {
        "name": "東進個別指導学院",
        "search_keywords": ["東進個別指導学院 講師 大阪府", "東進個別 塾講師 バイト 大阪 時給"],
        "recruitment_url": "https://www.toshinkobetsu.jp/teacher/",
    },
    {
        "name": "ITTO個別指導学院",
        "search_keywords": ["ITTO個別指導学院 講師 大阪府", "ITTO 塾講師 バイト 大阪 時給"],
        "recruitment_url": "https://www.itto.jp/teacher/",
    },
    {
        "name": "ファロス",
        "search_keywords": ["ファロス 個別指導 講師 大阪府", "ファロス 塾講師 バイト 大阪 時給"],
        "recruitment_url": None,
    },
    {
        "name": "スクールIE",
        "search_keywords": ["スクールIE 講師 大阪府", "スクールIE 塾講師 バイト 大阪 時給"],
        "recruitment_url": "https://www.schoolie-net.jp/teacher/",
    },
    {
        "name": "トライプラス",
        "search_keywords": ["トライプラス 講師 大阪府", "トライプラス 塾講師 バイト 大阪 時給"],
        "recruitment_url": "https://www.trygroup.co.jp/tryplus/",
    },
    {
        "name": "ゴールフリー",
        "search_keywords": ["ゴールフリー 講師 大阪府", "ゴールフリー 塾講師 バイト 大阪 時給"],
        "recruitment_url": "https://www.goalfree.jp/",
    },
    {
        "name": "関西個別指導学院",
        "search_keywords": ["関西個別指導学院 講師 大阪府", "関西個別 塾講師 バイト 大阪 時給"],
        "recruitment_url": None,
    },
    {
        "name": "京進スクールONE",
        "search_keywords": ["京進スクールONE 講師 大阪府", "京進 スクールワン 塾講師 バイト 大阪 時給"],
        "recruitment_url": "https://www.schoolone.jp/teacher/",
    },
    {
        "name": "第一ゼミナール",
        "search_keywords": ["第一ゼミナール 講師 大阪府", "第一ゼミナール 塾講師 バイト 大阪 時給"],
        "recruitment_url": "https://www.daiichi-seminar.co.jp/",
    },
    {
        "name": "KEC個別指導メビウス",
        "search_keywords": ["KEC個別 講師 大阪府", "KEC メビウス 塾講師 バイト 大阪 時給"],
        "recruitment_url": "https://www.kec.ne.jp/",
    },
    {
        "name": "キャンパス",
        "search_keywords": ["個別指導キャンパス 講師 大阪府", "キャンパス 塾講師 バイト 大阪 時給"],
        "recruitment_url": None,
    },
    {
        "name": "まなび",
        "search_keywords": ["まなび 個別指導 講師 大阪府", "まなび 塾講師 バイト 大阪 時給"],
        "recruitment_url": None,
    },
    {
        "name": "まなびプラス",
        "search_keywords": ["まなびプラス 個別指導 講師 大阪府", "まなびプラス 塾講師 バイト 大阪 時給"],
        "recruitment_url": None,
    },
]

SURVEY_SCHEMA = {
    "name": "str - 塾名",
    "teaching_format": "str - 指導形態（例: 1:1, 1:2, 1:3, 1:4）",
    "hourly_pay_min": "int|null - 時給（最低値）円",
    "hourly_pay_max": "int|null - 時給（最高値）円",
    "hourly_pay_mode": "int|null - 時給（最頻値・最もよく見る額）円",
    "session_pay": "int|null - コマ給 円",
    "session_minutes": "int|null - 1コマの授業時間（分）",
    "benefits": "list[str] - 福利厚生リスト",
    "employment_type": "str - 雇用形態",
    "target_grades": "str - 対象学年",
    "source_url": "str - 参照URL",
    "notes": "str - 備考・特記事項（大阪府内の地域差など）",
}
