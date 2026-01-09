from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import json

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

financial_data = load_financial_data()

financial_data_str = json.dumps(financial_data, indent = 4)

# print(financial_data)

llm = Ollama(
    model = "deepseek-r1:1.5b",
    temperature = "0.3"
)

chain = prompt | llm | StrOutputParser()

response = chain.invoke(
    {
        "financial_data" : financial_data_str
    }
)

print(response)

