---
name: analyze-cse
description: Fetch and analyze financial announcements from the Colombo Stock Exchange (CSE). Downloads PDFs, extracts financial data, and generates comprehensive investment analysis reports as PDFs. Use when user wants to analyze Sri Lankan stocks, CSE filings, or financial announcements.
argument-hint: "[SYMBOL] or leave blank for all"
allowed-tools: Bash, Read, Write, Grep, Glob, WebFetch, Agent
---

# CSE Financial Announcement Analyzer

Analyze financial filings from the Colombo Stock Exchange and generate investment analysis PDF reports.

## Input

- `$ARGUMENTS` may contain a stock symbol (e.g., `SAMP`, `SLFL`) or be empty
- If empty, fetch all available announcements and let user choose, or process all

## Step 1: Fetch Announcements

Fetch the latest financial announcements from CSE:

```bash
curl -s -X POST https://www.cse.lk/api/getFinancialAnnouncement -H "Content-Type: application/json" -d '{}' > /tmp/cse_announcements.json
```

Parse the JSON response. The key is `reqFinancialAnnouncemnets` (note the typo — that's the actual API field name).

Filter for relevant filings only:
- INCLUDE: "Audited Financial Statements", "Interim Financial Statements", "Annual Report"
- EXCLUDE: "Errata", "Prospectus", "Trust Deed", "Bond Framework", "KEY INVESTOR INFORMATION", "Accountants Report"

If `$ARGUMENTS` contains a symbol, filter to only that symbol. Otherwise list all and ask the user which to process.

## Step 2: Download PDF

Download the PDF from CDN. The URL pattern is:
```
https://cdn.cse.lk/{path}
```
where `{path}` is the `path` field from the announcement JSON.

Save to `/tmp/cse_{SYMBOL}_{id}.pdf`

## Step 3: Extract Text

Use `pdftotext` (already installed via poppler) to extract text:

```bash
pdftotext -layout /tmp/cse_{SYMBOL}_{id}.pdf /tmp/cse_{SYMBOL}_{id}.txt
```

Check the file size. For large files (>100K chars), use `Grep` and `Read` with offsets to find and read only the key sections:
- Key Financial Highlights / Financial Snapshot
- Statement of Profit or Loss
- Statement of Financial Position
- Statement of Changes in Equity
- Key Performance Indicators / Ratios
- Investor Information / Top 20 Shareholders
- Share Trading information
- Capital Adequacy ratios

## Step 4: Analyze

Read the extracted financial sections using the Read tool (with offset/limit for large files) and Grep to find specific data points.

Produce a comprehensive investment analysis covering ALL of these sections:

### 1. COMPANY OVERVIEW
- Company name, sector, market position, rating, key milestones

### 2. PROFIT & LOSS ANALYSIS
- Build a comparison table with at least 2 years: Gross Income, Net Interest Income (banks), Total Operating Income, Impairment, Operating Expenses, Taxes, PAT
- YoY change percentages
- NIM trends, fee income, cost drivers, effective tax rate

### 3. BALANCE SHEET ANALYSIS
- Table: Total Assets, Loans, Deposits, Equity with YoY changes
- Loan-to-deposit ratio, CASA ratio, investment portfolio

### 4. ASSET QUALITY (banks/finance)
- Stage 3 (NPL) ratio, Stage 2, coverage ratio, cost of risk
- For non-banks: receivables, inventory quality

### 5. CAPITAL ADEQUACY & LIQUIDITY (banks/finance)
- CET1, Tier 1, Total CAR vs regulatory minimums
- LCR, NSFR
- For non-banks: debt/equity, current ratio

### 6. KEY FINANCIAL RATIOS
- Table: ROE, ROA, EPS, DPS, P/E, P/BV, Dividend Yield, Payout, CIR, NIM
- Multiple years if available

### 7. VALUATION ASSESSMENT
- P/E, P/BV context, dividend yield vs deposit rates
- Fair value estimate with reasoning

### 8. OWNERSHIP STRUCTURE
- Top shareholders, institutional vs retail, director holdings, public float

### 9. KEY RISKS & CONCERNS
- Table: Risk | Description | Severity (HIGH/MEDIUM/LOW)

### 10. INVESTMENT VERDICT
- Clear BUY / HOLD / SELL with rationale
- Bull and bear cases
- Catalysts, entry price, stop loss, expected return

## Step 5: Generate PDF Report

Use the Python script at `report_generator.py` in the project directory to generate a PDF.

First, save the analysis markdown to a temp file:
```bash
cat > /tmp/cse_analysis_{SYMBOL}.md << 'ANALYSIS_EOF'
{the full analysis markdown}
ANALYSIS_EOF
```

Then generate the PDF:
```python
# Run this via: .venv/bin/python -c "..."
import sys
sys.path.insert(0, '/Users/janakas/Documents/stocks/dashboard')
from report_generator import generate_report
from models import AnalysisResult
from datetime import datetime

result = AnalysisResult(
    symbol="{SYMBOL}",
    company_name="{COMPANY_NAME}",
    period="{PERIOD}",
    analysis_text=open("/tmp/cse_analysis_{SYMBOL}.md").read(),
    generated_at=datetime.now(),
)
path = generate_report(result)
print(f"Report saved: {path}")
```

The PDF will be saved to `data/reports/{SYMBOL}_analysis_{date}.pdf`.

## Important Notes

- Use specific numbers from the financial statements — never make up data
- If data for a section is not available, state "Data not available in this filing"
- Compare current vs prior periods wherever possible
- Be analytical, not merely descriptive
- Think as an investor with 50 years of experience on the Colombo Stock Exchange
- The analysis should be institutional-grade quality
