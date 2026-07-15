import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Paths
BASE = Path(__file__).resolve().parents[1]
DATA_FILE = BASE / "studentdata" / "student.csv"
OUT_DIR = BASE / "output"
OUT_DIR.mkdir(exist_ok=True)

# Load dataset
df = pd.read_csv(DATA_FILE)

# Quick look
print(df.head())
print(df.info())

# Create average grade
df['average_grade'] = df[['G1','G2','G3']].mean(axis=1)

# Top 10 students
top_students = df.sort_values('average_grade', ascending=False).head(10)
print("Top students:\n", top_students[['school','sex','age','average_grade']])

# Normalize payment status for clearer labels
# The dataset uses 'yes'/'no', so we map them to 'Paid'/'Unpaid'
df['payment_status'] = df['paid'].replace({'yes': 'Paid', 'no': 'Unpaid'})

# paid students
paid_students = df[df['payment_status'] == 'Paid']
unpaid_students = df[df['payment_status'] == 'Unpaid']
print("Paid students:\n", paid_students[['school','sex','age','average_grade']])
print("Unpaid students:\n", unpaid_students[['school','sex','age','average_grade']])

# Save summary
top_students.to_csv(OUT_DIR / 'top_students.csv', index=False)
paid_students.to_csv(OUT_DIR / 'paid_students.csv', index=False)
unpaid_students.to_csv(OUT_DIR / 'unpaid_students.csv', index=False)

# Plot average grade distribution
plt.figure(figsize=(8,6))
sns.histplot(df['average_grade'], bins=15, kde=True)
plt.title('Average Grade Distribution')
plt.savefig(OUT_DIR / 'average_grade_distribution.png')
plt.close()

# pie chart for paid students vs unpaid students
payment_counts = df['payment_status'].value_counts()
plt.figure(figsize=(6,6))
plt.pie(payment_counts, labels=payment_counts.index, autopct='%1.1f%%', startangle=120, colors=['#66b3ff','#ff9999'])
plt.title('Payment Status Distribution')
plt.savefig(OUT_DIR / 'payment_status_distribution.png')
plt.close()

print("Project complete. Check the output folder for results.")
