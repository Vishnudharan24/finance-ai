from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import json
import os

system_prompt = """
PERSONA:

You are a senior financial analyst advising founders and finance teams.

BACKGROUND CONTEXT:

The financial data represents monthly operating performance of a startup over a period.

The dataset contains:

Aggregated financial metrics such as total revenue, average monthly revenue, total expenses, total profit, average profit margin, and average growth rate.
Month-over-month(mom) percentage changes for revenue, expenses, and profit, calculated deterministically using historical values.
The first month has no month-over-month values, as it serves as the baseline period.
Positive MoM(mom) percentages indicate growth, while negative values indicate decline relative to the previous month.
All numerical metrics have been pre-computed and validated.
You must not recalculate, infer missing numbers, or introduce new financial metrics.
Your task is to interpret trends, explain business implications, and provide insights and recommendations based strictly on the provided data.

DATA FIELD DEFINITION:

total_revenue: Sum of monthly revenue over the period.

avg_monthly_revenue: Arithmetic mean of monthly revenue values.

total_expenses: Sum of monthly operating expenses.

total_profit: Sum of monthly profit values.

avg_profit_margin: Average of monthly profit margins (profit ÷ revenue).

avg_growth_pct: Average of month-over-month revenue growth percentages.

*_mom_pct: Month-over-month percentage change relative to the immediately preceding month.

TASK:

1. Explain key insights
2. Prioritize risks
3. Explain why they matter
4. Give recommendations

OUTPUT FORMAT:

1.Overview
2.Key Metrics
3.Risks
4.Recommendations

"""

prompt = PromptTemplate(
    input_variables = ["financial_data"],
    template = system_prompt + """

DATA(JSON):
{financial_data}
"""
)

def load_financial_data():
    
    with open('metrics_summary.json', 'r') as f:
        metrics = json.load(f)
    
    with open('mom_trends.json', 'r') as f:
        mom_trends = json.load(f)
    
    financial_data = {
        'summary': metrics,  
        'monthly_trends': mom_trends
    }
    
    return financial_data

def generate_ai_insights():
    
    financial_data = load_financial_data()
    financial_data_str = json.dumps(financial_data, indent = 4)

    llm = Ollama(
        model = "gpt-oss:20b",
        temperature = "0.3"
    )

    chain = prompt | llm | StrOutputParser()

    response = chain.invoke(
        {
            "financial_data" : financial_data_str
        }
    )

    # output_path = os.path.join(os.path.dirname(__file__), "output.txt")
    # with open(output_path, "w", encoding="utf-8") as f:
    #     f.write(response)
    
    return response

def save_response(response, output_dir = None, formats = ["txt", "md", "html", "pdf"]):

    import markdown2
    from weasyprint import HTML as WeasyHTML

    if output_dir is None:
        output_dir = os.getcwd()

    print(f"the output dir {output_dir}")

    os.makedirs(output_dir, exist_ok = True)

    base_path = os.path.join(output_dir, "financial_analysis")

    if 'txt' in formats:
        with open(f"{base_path}.txt", "w", encoding="utf-8") as f:
            f.write(response)
    
    if 'md' in formats:
        with open(f"{base_path}.md", "w", encoding="utf-8") as f:
            f.write(response)
    
    if 'html' in formats:
       
        html_content = markdown2.markdown(response, extras=['tables'])
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Financial Analysis Report</title>
            <style>
                body {{ font-family: Poppins; margin: 40px; line-height: 1.6; }}
                h1 {{ color: #2c3e50; }}
                h2 {{ color: #34495e; }}
                table {{ 
                    border-collapse: collapse; 
                    width: 100%; 
                    margin: 20px 0; 
                }}
                th {{ 
                    background-color: #2c3e50; 
                    color: white; 
                    padding: 12px; 
                    text-align: left; 
                }}
                td {{ 
                    border: 1px solid #ddd; 
                    padding: 10px; 
                }}
                tr:nth-child(even) {{ 
                    background-color: #f2f2f2; 
                }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        with open(f"{base_path}.html", "w", encoding="utf-8") as f:
            f.write(html_template)
    
    if 'pdf' in formats:
     
        html_content = markdown2.markdown(response, extras=['tables'])
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Poppins; margin: 40px; line-height: 1.6; }}
                h1 {{ color: #2c3e50; }}
                h2 {{ color: #34495e; }}
                table {{ 
                    border-collapse: collapse; 
                    width: 100%; 
                    margin: 20px 0; 
                }}
                th {{ 
                    background-color: #2c3e50; 
                    color: white; 
                    padding: 12px; 
                    text-align: left; 
                }}
                td {{ 
                    border: 1px solid #ddd; 
                    padding: 10px; 
                }}
                tr:nth-child(even) {{ 
                    background-color: #f2f2f2; 
                }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        WeasyHTML(string=html_template).write_pdf(f"{base_path}.pdf")



