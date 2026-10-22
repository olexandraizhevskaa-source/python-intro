import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file_path', type=str)
args = parser.parse_args()

df = pd.read_csv(args.file_path)

avg_price = np.mean(df['price_per_unit'])
median_quantity = np.median(df['quantity'])
std_price = np.std(df['price_per_unit'])

df['total_revenue'] = df['quantity'] * df['price_per_unit']
supplier_profit = df.groupby('supplier')['total_revenue'].sum()
top_supplier = supplier_profit.idxmax()

category_quantity = df.groupby('category')['quantity'].sum()

low_supply = df[df['quantity'] < 100]
low_supply.to_csv('low_supply.csv', index=False)

df['total_price'] = df['quantity'] * df['price_per_unit']
sorted_df = df.sort_values(by='total_price', ascending=False)
print(sorted_df.head(3))

with open('report.txt', 'w') as f:
    f.write(f"Середня ціна всіх препаратів: {avg_price}\n")
    f.write(f"Медіана кількості: {median_quantity}\n")
    f.write(f"Стандартне відхилення ціни: {std_price}\n")
    f.write(f"Постачальник з найбільшим прибутком: {top_supplier}\n")
    f.write("Назва створеного файлу з дефіцитними поставками: low_supply.csv\n")

plt.figure(figsize=(8, 5))
category_quantity.plot(kind='bar', color='skyblue')
plt.title('Розподіл кількості препаратів за категоріями')
plt.xlabel('Категорія')
plt.ylabel('Кількість')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('category_distribution.png')
plt.close()