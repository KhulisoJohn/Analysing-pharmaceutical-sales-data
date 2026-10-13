import matplotlib
matplotlib.use('Agg')
display = print



# Analysing Pharmaceutical Sales Data
import pandas as pd
import matplotlib.pyplot as plt
import os

# Step 1 - Load the data
df = pd.read_csv('data/salesdaily.csv')
df['datum'] = pd.to_datetime(df['datum'])
df = df.sort_values('datum').reset_index(drop=True)
df.head()


# Step 2 - Explore and clean the data
print('Shape:', df.shape)
print('Date range:', df['datum'].min().date(), 'to', df['datum'].max().date())
print('\nMissing values:\n', df.isna().sum())
print('\nDuplicate rows:', df.duplicated.sum())
df.describe().round(2)

#Step 3 - Define drug columns and helper fields
drug_cols = ['M01AB', 'M01AE', 'N02BA', 'N02BE','N05B','N05C','R03', 'R06']
drug_cols = [c for c in drug_cols if c in df.columns]
df['Year'] = df['datum'].dt.year
df['Month'] = df['datum'].dt.month
df['MonthName'] = df['datum'].dt.month_name()
print(drug_cols)


# Q1 - Total sales quantity for each drug category (ATC code)
q1 = df[drug_cols].sum().sort_values(ascending=False).round(1)
q1_table = q1,rename('Total quantiy').to_frame()
q1_table['share %'] = (q1_table['Total quantity'] / q1_table['Total quantity'].sum() * 100).round(1)
q1_table.to_csv('outputs/q1_table_by_category.csv')
display(q1_table)

ax = q1.plot(kind='bar', color='steelblue', edgecolor='black')
ax.set_title('Q1: Total Sales Quantity by Drug Category (ATC)')
ax.set_xlabel('ATC code'); ax.set_ylabel('Total quantity sold')
plt.xticks(rotation=0); plt.tight_layout()
plt.savefig('outputs/q1_total_by_category.png', dpi=150); plt.show()

print(f"INSIGHT: {q1.index[0]} is the best selling cartegory with {q1.iloc[0]} units"
      f"({q1_table['share %'].iloc[0]}% of all sales). {q1.index[-1]} sells the latest."
      )


# Q2 - Which individual drug brand have the highest total sales?
top_n = 5
q2 = q1.head(top_n)
q2_table = q2.rename('Total queantity').to_frame()
q2_table.index.name = 'Drug (ATC)'
q2_table.to_csv('outputs/q2_top_drugs.csv')
display(q1_table)

ax = q2.sort_values().plot(kind='barh', color='darkorange', edgecolor='black')
ax.set_title(f'Q2: Top {top_n} Drugs by Total Sales')
ax.set_xlabel('Total quantity sold')
plt.tight_layout(); plt.savefig('outputs/q2_top_drugs.png', dpi=150); plt.show()

print('INSIGHT: Top 3 drugs overall are', ','.join(q2.index[:3]),
      f"- together {q2.iloc[:3].sum()/q1.sum()*100:.1f}% of all quantity sold.")

# Q3 Top three drugs in Januaery 2015, July 2016 and September 2017
periods = [(2015, 1, 'January 2015'), (2016, 7, 'July 2016'), (2017, 9, 'September 2017')]
fig, axes = plt.subplot(1, 3, figsize = (15, 4.5), sharey= False)
rows = []
for ax, (yr, mo, label) in zip(axes, periods):
    sub = df[(df['Year'] == yr) & (df['Month'] == mo)]
    top3 = sub[drug_cols].sum().sort_values(ascending=False).head(3).round(1)
    for rank, (drug, qty) in enumerate(top3.items(),1):
        rows.append({'period':label, 'Rank':rank, 'Drug':drug, 'Quantity':qty})
    top3.plot(kind='bar', ax=ax, color=['#2e7d32', '#66bb6a', '#a5d6a7'], edgecolor='black')
    ax.set_title(label); ax.set_xlabel('ATC code'); ax.set_ylabel('Quantity')
    ax.tick_params(axis='x', rotation=0)

fig.subtitle('Q3: Top 3 Drugs in Selected Months')
plt.tight_layout(); plt.savefig('outputs/q3_top_selected_months.png', dpi=150); plt.show()

q3_table = pd.DataFrame(rows)
q3_table.to_csv('outputs/q3_top3_selected_months.csv', index=False)
display(q3_table)


