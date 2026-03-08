# CSE Investment Analyzer

A Claude Code skill that fetches financial announcements from the Colombo Stock Exchange (CSE), analyzes them, and generates PDF investment reports.

## How It Works

This project uses a **Claude Code custom skill** (`/analyze-cse`) that runs directly inside Claude Code. When invoked, Claude:

1. Fetches the latest financial announcements from the CSE API
2. Downloads the PDF filing from `cdn.cse.lk`
3. Extracts text using `pdftotext`
4. Reads and analyzes key financial sections (P&L, Balance Sheet, Ratios, Shareholders, etc.)
5. Produces an institutional-grade investment analysis
6. Generates a formatted PDF report

## Prerequisites

- **Claude Code** installed and authenticated
- **poppler** for PDF text extraction: `brew install poppler`
- **Python 3.10+** with a virtual environment:

```bash
python3 -m venv .venv
.venv/bin/pip install fpdf2
```

## Usage

Start Claude Code in this directory, then use the skill:

```bash
cd /path/to/dashboard
claude
```

Inside Claude Code:

```
/analyze-cse SAMP          # Analyze Sampath Bank
/analyze-cse SLFL          # Analyze Siyapatha Finance
/analyze-cse               # List all available announcements
```

Reports are saved to `data/reports/{SYMBOL}_analysis_{date}.pdf`.

## Project Structure

```
dashboard/
├── .claude/
│   └── skills/
│       └── analyze-cse/
│           └── SKILL.md        # The skill definition
├── models.py                   # AnalysisResult data class
├── report_generator.py         # Markdown-to-PDF renderer (fpdf2)
├── data/
│   └── reports/                # Generated PDF reports
└── README.md
```

## Analysis Coverage

The generated report covers:

1. **Company Overview** - sector, rating, milestones
2. **Profit & Loss** - multi-year comparison tables with YoY changes
3. **Balance Sheet** - assets, loans, deposits, equity trends
4. **Asset Quality** - NPL ratios, provision coverage (banks)
5. **Capital Adequacy** - CET1, Tier 1, CAR vs regulatory minimums (banks)
6. **Key Ratios** - ROE, ROA, EPS, DPS, P/E, P/BV, NIM, CIR
7. **Valuation** - fair value estimate with reasoning
8. **Ownership** - top shareholders, institutional split
9. **Risks** - rated HIGH/MEDIUM/LOW with descriptions
10. **Investment Verdict** - BUY/HOLD/SELL with bull/bear cases

## CSE API

- **Announcements endpoint**: `POST https://www.cse.lk/api/getFinancialAnnouncement` (empty JSON body)
- **PDF CDN**: `https://cdn.cse.lk/{path}`
- Response key: `reqFinancialAnnouncemnets` (note the typo - that's the actual API field)
