import matplotlib
matplotlib.use('Agg')
display = print


# Analysing Pharmaceutical Sales Data
import pandas as pd
import matplotlib.pyplot as plt
import os

plt.rcParams['figure.figsize'] = (10, 5)
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3
os.makedirs('outputs', exist_ok=True)


# Step 1 - Load the data
df = pd.read_csv('data/salesdaily.csv')
df['datum'] = pd.to_datetime(df['datum'])
df = df.sort_values('datum').reset_index(drop=True)
df.head()


# Step 2 - Explore and clean the data
print('Shape:', df.shape)
print('Date range:', df['datum'].min().date(), 'to', df['datum'].max().date())
print('\nMissing values:\n', df.isna().sum())
print('\nDuplicate rows:', df.duplicated().sum())
df.describe().round(2)


# Step 3 - Define drug columns and helper fields
drug_cols = ['M01AB', 'M01AE', 'N02BA', 'N02BE', 'N05B', 'N05C', 'R03', 'R06']
drug_cols = [c for c in drug_cols if c in df.columns]
df['Year'] = df['datum'].dt.year
df['Month'] = df['datum'].dt.month
df['MonthName'] = df['datum'].dt.month_name()
print(drug_cols)


# Q1 - Total sales quantity for each drug category (ATC code)
q1 = df[drug_cols].sum().sort_values(ascending=False).round(1)
q1_table = q1.rename('Total quantity').to_frame()
q1_table['Share %'] = (q1_table['Total quantity'] / q1_table['Total quantity'].sum() * 100).round(1)
q1_table.to_csv('outputs/q1_total_by_category.csv')
display(q1_table)

ax = q1.plot(kind='bar', color='steelblue', edgecolor='black')
ax.set_title('Q1: Total Sales Quantity by Drug Category (ATC)')
ax.set_xlabel('ATC code'); ax.set_ylabel('Total quantity sold')
plt.xticks(rotation=0); plt.tight_layout()
plt.savefig('outputs/q1_total_by_category.png', dpi=150); plt.show()

print(f"INSIGHT: {q1.index[0]} is the best-selling category with {q1.iloc[0]:,.0f} units "
      f"({q1_table['Share %'].iloc[0]}% of all sales). {q1.index[-1]} sells the least.")


# Q2 - Which individual drug brands have the highest total sales?
top_n = 5
q2 = q1.head(top_n)
q2_table = q2.rename('Total quantity').to_frame()
q2_table.index.name = 'Drug (ATC)'
q2_table.to_csv('outputs/q2_top_drugs.csv')
display(q2_table)

ax = q2.sort_values().plot(kind='barh', color='darkorange', edgecolor='black')
ax.set_title(f'Q2: Top {top_n} Drugs by Total Sales')
ax.set_xlabel('Total quantity sold')
plt.tight_layout(); plt.savefig('outputs/q2_top_drugs.png', dpi=150); plt.show()

print('INSIGHT: Top 3 drugs overall are', ', '.join(q2.index[:3]),
      f"- together {q2.iloc[:3].sum()/q1.sum()*100:.1f}% of all quantity sold.")


# Q3 - Top three drugs in January 2015, July 2016 and September 2017
periods = [(2015, 1, 'January 2015'), (2016, 7, 'July 2016'), (2017, 9, 'September 2017')]
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), sharey=False)
rows = []
for ax, (yr, mo, label) in zip(axes, periods):
    sub = df[(df['Year'] == yr) & (df['Month'] == mo)]
    top3 = sub[drug_cols].sum().sort_values(ascending=False).head(3).round(1)
    for rank, (drug, qty) in enumerate(top3.items(), 1):
        rows.append({'Period': label, 'Rank': rank, 'Drug': drug, 'Quantity': qty})
    top3.plot(kind='bar', ax=ax, color=['#2e7d32', '#66bb6a', '#a5d6a7'], edgecolor='black')
    ax.set_title(label); ax.set_xlabel('ATC code'); ax.set_ylabel('Quantity')
    ax.tick_params(axis='x', rotation=0)
fig.suptitle('Q3: Top 3 Drugs in Selected Months')
plt.tight_layout(); plt.savefig('outputs/q3_top3_selected_months.png', dpi=150); plt.show()

q3_table = pd.DataFrame(rows)
q3_table.to_csv('outputs/q3_top3_selected_months.csv', index=False)
display(q3_table)

for label, g in q3_table.groupby('Period', sort=False):
    print(f"INSIGHT: {label} - #1 is {g.iloc[0]['Drug']} ({g.iloc[0]['Quantity']:,.0f} units).")


# Q4 - Which drug has sold the most often in 2017?
d17 = df[df['Year'] == 2017]
q4_table = pd.DataFrame({
    'Days with sales': (d17[drug_cols] > 0).sum(),
    'Total quantity': d17[drug_cols].sum().round(1)
}).sort_values(['Days with sales', 'Total quantity'], ascending=False)
q4_table.to_csv('outputs/q4_most_frequent_2017.csv')
display(q4_table)

ax = q4_table['Days with sales'].plot(kind='bar', color='mediumpurple', edgecolor='black')
ax.set_title('Q4: Number of Days with Sales per Drug (2017)')
ax.set_xlabel('ATC code'); ax.set_ylabel(f'Days with sales (of {len(d17)} days recorded)')
plt.xticks(rotation=0); plt.tight_layout()
plt.savefig('outputs/q4_most_frequent_2017.png', dpi=150); plt.show()

print(f"INSIGHT: {q4_table.index[0]} sold most often in 2017 "
      f"({q4_table['Days with sales'].iloc[0]} days). Total quantity leader: {q4_table['Total quantity'].idxmax()}.")


# Q5 - Which drug category has the highest average daily sales?
q5 = df[drug_cols].mean().sort_values(ascending=False).round(2)
q5_table = q5.rename('Average daily sales').to_frame()
q5_table.to_csv('outputs/q5_avg_daily_sales.csv')
display(q5_table)

ax = q5.plot(kind='bar', color='teal', edgecolor='black')
ax.set_title('Q5: Average Daily Sales by Drug Category')
ax.set_xlabel('ATC code'); ax.set_ylabel('Average units per day')
for i, v in enumerate(q5.values):
    ax.text(i, v, f'{v:.1f}', ha='center', va='bottom')
plt.xticks(rotation=0); plt.tight_layout()
plt.savefig('outputs/q5_avg_daily_sales.png', dpi=150); plt.show()

print(f"INSIGHT: {q5.index[0]} has the highest average daily sales ({q5.iloc[0]:.1f} units/day), "
      f"about {q5.iloc[0]/q5.iloc[-1]:.1f}x the lowest category ({q5.index[-1]}).")


# Q6 - Are respiratory drugs (R03) sold more during specific months?
month_order = ['January','February','March','April','May','June','July','August',
               'September','October','November','December']
r03 = df.groupby('MonthName')['R03'].mean().reindex(month_order).round(2)
r03_table = r03.rename('Avg daily R03 sales').to_frame()
r03_table.to_csv('outputs/q6_r03_by_month.csv')
display(r03_table)

colors = ['crimson' if v == r03.max() else 'lightcoral' for v in r03.values]
ax = r03.plot(kind='bar', color=colors, edgecolor='black')
ax.axhline(r03.mean(), color='black', linestyle='--', label=f'Yearly mean ({r03.mean():.1f})')
ax.set_title('Q6: R03 (Respiratory) - Average Daily Sales by Month')
ax.set_xlabel('Month'); ax.set_ylabel('Average units per day'); ax.legend()
plt.xticks(rotation=45, ha='right'); plt.tight_layout()
plt.savefig('outputs/q6_r03_by_month.png', dpi=150); plt.show()

# Month x Year heatmap-style line chart to check the pattern repeats every year
pivot = df.pivot_table(index='Month', columns='Year', values='R03', aggfunc='mean')
ax = pivot.plot(marker='o')
ax.set_title('R03 Average Daily Sales by Month, per Year')
ax.set_xlabel('Month'); ax.set_ylabel('Average units per day'); ax.set_xticks(range(1, 13))
plt.tight_layout(); plt.savefig('outputs/q6_r03_month_by_year.png', dpi=150); plt.show()

print(f"INSIGHT: R03 peaks in {r03.idxmax()} ({r03.max():.1f}/day) and is lowest in {r03.idxmin()} ({r03.min():.1f}/day). "
      f"The peak is {(r03.max()/r03.min()-1)*100:.0f}% above the low, so R03 is {'clearly seasonal' if r03.max()/r03.min() > 1.2 else 'only mildly seasonal'}.")


# Bonus - Overall trend over time
monthly = df.set_index('datum')[drug_cols].resample('MS').sum()
ax = monthly.sum(axis=1).plot(color='navy')
ax.set_title('Total Monthly Sales, All Categories'); ax.set_xlabel('Date'); ax.set_ylabel('Quantity')
plt.tight_layout(); plt.savefig('outputs/bonus_monthly_trend.png', dpi=150); plt.show()
