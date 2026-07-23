SURVEY_REGION = "大阪市（大阪府）"
SURVEY_REGION_NOTE = "大阪市内の教室に絞って調査。梅田・なんばなど超繁華街の特殊案件より、住宅地域の一般的な相場を重視"

COMPETITORS = [
    {
        "name": "アップ学習会",
        "is_own_company": True,
        "search_keywords": ["アップ学習会 講師 大阪市", "アップ学習会 バイト 大阪市 時給"],
        "recruitment_url": "https://www.up-gakushukai.co.jp/",
        "source_urls": ["https://www.juku.st/brand/632"],
    },
    {
        "name": "明光義塾",
        "search_keywords": ["明光義塾 講師 大阪市", "明光義塾 バイト 大阪市 時給"],
        "recruitment_url": "https://www.meiko-flap.jp/recruit/",
        "source_urls": ["https://www.juku.st/classrooms/119"],
    },
    {
        "name": "個別指導Axis",
        "search_keywords": ["個別指導Axis 講師 大阪市", "アクシス 塾講師 バイト 大阪市 時給"],
        "recruitment_url": "https://www.axis-net.jp/teacher/",
        "source_urls": ["https://jukunavi.com/job/axis/osaka/"],
    },
    {
        "name": "個別指導塾スタンダード",
        "search_keywords": ["個別指導塾スタンダード 講師 大阪市", "スタンダード 塾講師 バイト 大阪市 時給"],
        "recruitment_url": "https://standard-ac.jp/teacher/",
        "source_urls": ["https://jukunavi.com/job/standard/aeontownhirano/"],
    },
    {
        "name": "個別指導WAM",
        "search_keywords": ["個別指導WAM 講師 大阪市", "WAM 塾講師 バイト 大阪市 時給"],
        "recruitment_url": "https://www.e-wam.jp/",
        "source_urls": ["https://www.juku.st/classroom/28528"],
    },
    {
        "name": "個別指導学院ヒーローズ",
        "search_keywords": ["個別指導学院ヒーローズ 講師 大阪市", "ヒーローズ 塾講師 バイト 大阪市 時給"],
        "recruitment_url": "https://heros.fuerubooubo.com/",
        "source_urls": [],  # job IDは失効するためPhase2のweb_searchに委ねる
    },
    {
        "name": "個別教室のトライ",
        "search_keywords": ["個別教室のトライ 講師 大阪市", "トライ 家庭教師 バイト 大阪市 時給"],
        "recruitment_url": "https://www.trygroup.co.jp/recruit/",
        "source_urls": ["https://www.trygroup.co.jp/recruit/"],
    },
    {
        "name": "個別指導学院フリーステップ",
        "search_keywords": ["個別指導学院フリーステップ 講師 大阪市", "フリーステップ 塾講師 バイト 大阪市 時給"],
        "recruitment_url": "https://kaiseigroup-saiyo.com/-/top/kobetsu.html",
        "source_urls": ["https://jukunavi.com/job/seigakusya/nishitanabe/"],
    },
    {
        "name": "東進個別指導学院",
        "search_keywords": ["東進個別指導学院 講師 大阪市", "東進個別 塾講師 バイト 大阪市 時給"],
        "recruitment_url": "https://jukunavi.com/g/toshineiseiyobiko/",
        "source_urls": ["https://jukunavi.com/g/toshineiseiyobiko/"],
    },
    {
        "name": "ITTO個別指導学院",
        "search_keywords": ["ITTO個別指導学院 講師 大阪市", "ITTO 塾講師 バイト 大阪市 時給"],
        "recruitment_url": "https://www.itto.jp/teacher/",
        "source_urls": [],  # 吹田市（大阪市外）のためPhase2のweb_searchに委ねる
    },
    {
        "name": "ファロス個別指導学院",
        "search_keywords": ["ファロス個別指導 講師 大阪市", "ファロス 塾講師 バイト 大阪市 時給"],
        "recruitment_url": "https://www.daiichisemi.net/jinzai/requirement_pharos.php",
        "source_urls": ["https://jukunavi.com/job/with-us/tamaidekimae/"],
    },
    {
        "name": "スクールIE",
        "search_keywords": ["スクールIE 講師 大阪市", "スクールIE 塾講師 バイト 大阪市 時給"],
        "recruitment_url": "http://schoolie-job.net/",
        "source_urls": ["https://www.juku.st/brand/22"],
    },
    {
        "name": "トライプラス",
        "search_keywords": ["トライプラス 講師 大阪市", "トライプラス 塾講師 バイト 大阪市 時給"],
        "recruitment_url": "https://www.trygroup.co.jp/tryplus/",
        "source_urls": ["https://jukunavi.com/g/kobetsushidojukutryplus/"],
    },
    {
        "name": "ゴールフリー",
        "search_keywords": ["ゴールフリー 講師 大阪市", "ゴールフリー 塾講師 バイト 大阪市 時給"],
        "recruitment_url": "https://www.goalfree.jp/",
        "source_urls": [],  # job IDは失効するためPhase2のweb_searchに委ねる
    },
    {
        "name": "関西個別指導学院",
        "search_keywords": ["関西個別指導学院 講師 大阪市", "関西個別 塾講師 バイト 大阪市 時給"],
        "recruitment_url": "https://baito.mynavi.jp/brand/brand-490/",
        "source_urls": [
            "https://jukunavi.com/job/tkg/tennoji/",
            "https://baito.mynavi.jp/brand/brand-490/",
        ],
    },
    {
        "name": "京進スクールONE",
        "search_keywords": ["京進スクールONE 講師 大阪市", "京進 スクールワン 塾講師 バイト 大阪市 時給"],
        "recruitment_url": "https://www.schoolone.jp/teacher/",
        "source_urls": ["https://jukunavi.com/job/kyoshin/hanshinnoda/"],
    },
    {
        "name": "第一ゼミナール",
        "search_keywords": ["第一ゼミナール 講師 大阪市", "第一ゼミナール 塾講師 バイト 大阪市 時給"],
        "recruitment_url": "https://www.daiichisemi.net/jinzai/",
        "source_urls": ["https://jukunavi.com/job/with-us/uehommachi/"],
    },
    {
        "name": "KEC個別指導メビウス",
        "search_keywords": ["KEC個別 講師 大阪市", "KEC メビウス 塾講師 バイト 大阪市 時給"],
        "recruitment_url": "https://www.mebius-kobetsu.jp/",
        "source_urls": ["https://www.juku.st/brand/966"],
    },
    {
        "name": "キャンパス",
        "search_keywords": ["個別指導キャンパス 講師 大阪市", "キャンパス 塾講師 バイト 大阪市 時給"],
        "recruitment_url": "https://kobetsu-canpass-recruit.net/jobfind-pc/",
        "source_urls": ["https://jukunavi.com/job/canpass/tamatsukuri/"],
    },
    {
        "name": "まなび",
        "search_keywords": ["まなび 個別指導 講師 大阪市", "まなび 塾講師 バイト 大阪市 時給"],
        "recruitment_url": "https://www.manabi-recruit.info/part/",
        "source_urls": ["https://www.juku.st/reviews/brand/340"],
    },
    {
        "name": "まなびプラス",
        "search_keywords": ["まなびプラス 個別指導 講師 大阪市", "まなびプラス 塾講師 バイト 大阪市 時給"],
        "recruitment_url": "https://www.manabi-recruit.info/part/",
        "source_urls": ["https://www.juku.st/classroom/24930"],
    },
]

SURVEY_SCHEMA = {
    "name": "str - 塾名",
    "teaching_format": "str - 指導形態（例: 1:1, 1:2, 1:3, 1:4）",
    "hourly_pay_min": "int|null - 時給（最低値）円",
    "hourly_pay_max": "int|null - 時給（最高値）円",
    "hourly_pay_mode": "int|null - 時給（代表値: 公式採用ページ記載の基本額、または確認できた最頻値）円",
    "session_pay": "int|null - コマ給 円",
    "session_minutes": "int|null - 1コマの授業時間（分）",
    "benefits": "list[str] - 福利厚生リスト",
    "employment_type": "str - 雇用形態",
    "target_grades": "str - 対象学年",
    "source_url": "str - 参照URL（塾講師ステーション・塾講師ナビ・Indeed等の実際の求人票URL）",
    "notes": "str - 備考・特記事項（大阪市内の地域差など）",
}
