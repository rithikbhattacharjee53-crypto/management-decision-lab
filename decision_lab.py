from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data" / "team_operations.csv")
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

LABOUR_RATE = 155
SERVICE_TARGET = 0.90

df["capacity_hours"] = df["employees"] * df["productive_hours_per_employee"]
df["utilization"] = df["required_hours"] / df["capacity_hours"]
df["capacity_gap"] = df["required_hours"] - df["capacity_hours"]
df["labour_cost"] = df["capacity_hours"] * LABOUR_RATE
df["contribution"] = df["revenue"] - df["variable_cost"] - df["labour_cost"]
df["contribution_margin_pct"] = df["contribution"] / df["revenue"]
df["estimated_service_level"] = (1.04 - 0.16 * df["utilization"]).clip(0.70, 0.99)
df["service_risk"] = (SERVICE_TARGET - df["estimated_service_level"]).clip(lower=0)

def scenario(frame, name, demand=1.0, productivity=1.0, extra=0):
    x = frame.copy()
    x["scenario"] = name
    x["employees_scenario"] = x["employees"] + extra
    x["capacity_scenario"] = x["employees_scenario"] * x["productive_hours_per_employee"] * productivity
    x["required_hours_scenario"] = x["required_hours"] * demand
    x["utilization_scenario"] = x["required_hours_scenario"] / x["capacity_scenario"]
    x["capacity_gap_scenario"] = x["required_hours_scenario"] - x["capacity_scenario"]
    x["labour_cost_scenario"] = x["capacity_scenario"] * LABOUR_RATE
    x["contribution_scenario"] = x["revenue"]*demand - x["variable_cost"]*demand - x["labour_cost_scenario"]
    x["service_level_scenario"] = (1.04 - 0.16*x["utilization_scenario"]).clip(0.70,0.99)
    x["decision_index"] = x["contribution_scenario"]/1000 - x["utilization_scenario"]*25 - (SERVICE_TARGET-x["service_level_scenario"]).clip(lower=0)*100
    return x

all_scenarios = pd.concat([
    scenario(df,"Baseline"),
    scenario(df,"Productivity +10%",productivity=1.10),
    scenario(df,"Demand +15%",demand=1.15),
    scenario(df,"Balanced: Hire + Productivity",productivity=1.05,extra=1)
], ignore_index=True)

hire = []
for team in df["team"]:
    x = scenario(df, f"Hire 1: {team}")
    mask = x["team"].eq(team)
    x.loc[mask,"employees_scenario"] += 1
    x.loc[mask,"capacity_scenario"] = x.loc[mask,"employees_scenario"] * x.loc[mask,"productive_hours_per_employee"]
    x.loc[mask,"utilization_scenario"] = x.loc[mask,"required_hours_scenario"] / x.loc[mask,"capacity_scenario"]
    x.loc[mask,"capacity_gap_scenario"] = x.loc[mask,"required_hours_scenario"] - x.loc[mask,"capacity_scenario"]
    x.loc[mask,"labour_cost_scenario"] = x.loc[mask,"capacity_scenario"] * LABOUR_RATE
    x.loc[mask,"contribution_scenario"] = x.loc[mask,"revenue"] - x.loc[mask,"variable_cost"] - x.loc[mask,"labour_cost_scenario"]
    x.loc[mask,"service_level_scenario"] = (1.04 - 0.16*x.loc[mask,"utilization_scenario"]).clip(0.70,0.99)
    x.loc[mask,"decision_index"] = x.loc[mask,"contribution_scenario"]/1000 - x.loc[mask,"utilization_scenario"]*25 - (SERVICE_TARGET-x.loc[mask,"service_level_scenario"]).clip(lower=0)*100
    hire.append(x)

cols = ["team","scenario","employees_scenario","utilization_scenario","capacity_gap_scenario","contribution_scenario","service_level_scenario","decision_index"]
all_scenarios[cols].to_csv(OUT/"management_decision_summary.csv",index=False)
pd.concat(hire)[cols].to_csv(OUT/"one_employee_tests.csv",index=False)

print("Created outputs/management_decision_summary.csv")
print("Created outputs/one_employee_tests.csv")
