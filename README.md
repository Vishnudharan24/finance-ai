# Financial AI Analyzer

## Requirements
- Python 3.8+
- Ollama installed locally
- Model: `gpt-oss:20b`

## Installation

```bash
pip install pandas langchain-core langchain-community markdown2 weasyprint
```

Install Ollama model:
```bash
ollama pull gpt-oss:20b
```

## Input File Format

CSV file with these columns:
- `date` - Date in any standard format
- `revenue` - Monthly revenue (numeric)
- `expenses` - Monthly expenses (numeric)
- `profit` - Monthly profit (numeric)

Example: `sample_financials.csv`

## How to Run

```bash
python main.py
```

Enter your CSV file path when prompted.

## Output Files

- `metrics_summary.json` - Aggregate metrics
- `mom_trends.json` - Month-over-month trends
- `ai_engine/financial_analysis.txt` - AI analysis (text)
- `ai_engine/financial_analysis.md` - AI analysis (markdown)
- `ai_engine/financial_analysis.html` - AI analysis (HTML)
- `ai_engine/financial_analysis.pdf` - AI analysis (PDF)

## Change Model

Edit `ai_engine/ai_analyzer.py` line 86:

```python
llm = Ollama(
    model = "gpt-oss:20b",  # Change this to your model name
    temperature = "0.3"
)
```

## Change Output Formats

Edit `main.py` where `generate_ai_insights()` is called:

```python
ai_insights = generate_ai_insights(output_formats=['txt', 'md', 'html', 'pdf'])
```

Remove formats you don't need.
