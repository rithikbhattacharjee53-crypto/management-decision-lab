# Management Decision Lab

**Workforce Capacity & Service Profitability Simulator**

A practical management analytics portfolio project by **Rithik Bhattacharjee**. It connects workload, workforce capacity, service risk and contribution margin to support management scenario analysis.

## Business questions
- Which teams are under capacity pressure?
- Where could one additional employee reduce operational pressure?
- What happens if productivity improves by 10%?
- What happens if demand rises by 15%?
- How does a balanced hiring + productivity scenario compare with the baseline?

## Core metrics
- Capacity hours = employees × productive hours per employee
- Utilization = required work hours ÷ capacity hours
- Capacity gap = required hours − available capacity
- Contribution = revenue − variable cost − labour cost
- Service-risk proxy = transparent function of utilization

## Scenarios
1. Baseline
2. Productivity +10%
3. Demand +15%
4. Balanced: Hire + Productivity
5. One-employee test for each team

## Structure
```text
management-decision-lab/
├── data/
│   └── team_operations.csv
├── outputs/
│   ├── management_decision_summary.csv
│   └── one_employee_tests.csv
├── src/
│   └── decision_lab.py
├── README.md
├── PROJECT_SUMMARY.md
├── requirements.txt
├── .gitignore
└── LICENSE
```

## Run
```bash
pip install -r requirements.txt
python src/decision_lab.py
```

The dataset is **synthetic portfolio data**, not company data.

## Resume bullet
> Built a Python-based management decision simulator integrating capacity utilization, service risk, labour economics and scenario analysis to evaluate workforce and productivity decisions.

## GitHub description
> Python management analytics simulator for workforce capacity, service risk, profitability and hiring/productivity scenarios.
