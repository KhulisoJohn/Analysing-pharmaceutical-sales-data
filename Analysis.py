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
q2_table = q2


