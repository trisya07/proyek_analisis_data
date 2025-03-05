import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Baca dataset
all_df = pd.read_csv('dashboard/main_data.csv')

# Set title untuk web
st.title('Dashboard Analisis Peminjaman Sepeda')

# Menambahkan bagian deskripsi
st.markdown("""
### Analisis Peminjaman Sepeda
Berikut adalah analisis data peminjaman sepeda berdasarkan berbagai faktor seperti hari, bulan, cuaca, dan lain-lain.
""")

# Histogram distribusi pengguna berdasarkan total peminjaman
st.subheader('Distribusi Total Peminjaman Pengguna')
fig, ax = plt.subplots()
sns.histplot(all_df['total_rentals_agg'], bins=20, color='gray', kde=True, ax=ax)
plt.axvline(all_df['total_rentals_agg'].mean(), color='red', linestyle='dashed', linewidth=2)
ax.set_xlabel('Total Peminjaman')
ax.set_ylabel('Jumlah Pengguna')
st.pyplot(fig)

# Analisis Tren Peminjaman Sepeda (Time Series)
st.subheader('Tren Peminjaman Sepeda')
fig, ax = plt.subplots(figsize=(12, 5))
all_df.groupby('date_day')['total_rentals_agg'].sum().rolling(window=7).mean().plot(color='blue', ax=ax)
st.pyplot(fig)

# Analisis Rasio Casual vs Registered
st.subheader('Rasio Peminjaman Casual vs Registered')
labels = ['Casual', 'Registered']
sizes = [all_df['casual_ratio'].mean(), all_df['registered_ratio'].mean()]
colors = ['lightblue', 'royalblue']
fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
st.pyplot(fig)

# Rata-rata Peminjaman Berdasarkan Hari dalam Seminggu
st.subheader('Rata-rata Peminjaman Berdasarkan Hari dalam Seminggu')
fig, ax = plt.subplots(figsize=(8, 5))
weekday_avg = all_df.groupby('weekday')['total_rentals_agg'].mean().sort_values()
colors = ['gray'] * len(weekday_avg)
colors[-1] = 'red'
ax.plot(weekday_avg.index, weekday_avg, marker='o', linestyle='-', color='gray')
ax.scatter(weekday_avg.index[-1], weekday_avg.iloc[-1], color='red', s=100, label='Tertinggi')
ax.legend()
ax.set_xticks(weekday_avg.index)
ax.set_xticklabels(weekday_avg.index, rotation=45)
st.pyplot(fig)

# Rata-rata Peminjaman Berdasarkan Bulan
st.subheader('Rata-rata Peminjaman Berdasarkan Bulan')
fig, ax = plt.subplots(figsize=(10, 5))
month_avg = all_df.groupby('month')['total_rentals_agg'].mean().sort_values()
colors = ['lightgray'] * len(month_avg)
colors[-1] = 'blue'
ax.barh(month_avg.index, month_avg, color=colors)
st.pyplot(fig)

# Rata-rata Peminjaman Berdasarkan Hari Kerja vs Hari Libur
st.subheader('Rata-rata Peminjaman: Hari Kerja vs Hari Libur')
fig, ax = plt.subplots(figsize=(8, 5))
workingday_avg = all_df.groupby('workingday')['total_rentals_agg'].mean()
colors = ['lightblue', 'blue']
workingday_avg.plot(kind='bar', color=colors, ax=ax)
ax.set_ylabel('Jumlah Peminjaman')
ax.set_xticklabels(['Non-Working Day', 'Working Day'], rotation=0)
st.pyplot(fig)

# Rata-rata Peminjaman Berdasarkan Kondisi Cuaca
st.subheader('Rata-rata Peminjaman Berdasarkan Kondisi Cuaca')
fig, ax = plt.subplots(figsize=(8, 5))
weather_avg = all_df.groupby('weathersit')['total_rentals_agg'].mean().sort_values()
colors = ['lightblue'] * len(weather_avg)
colors[-1] = 'blue'
weather_avg.plot(kind='bar', color=colors, ax=ax)
ax.set_ylabel('Jumlah Peminjaman')
ax.set_xticklabels(weather_avg.index, rotation=0)
st.pyplot(fig)

# Rata-rata Peminjaman Berdasarkan Musim
st.subheader('Rata-rata Peminjaman Berdasarkan Musim')
fig, ax = plt.subplots(figsize=(8, 5))
season_avg = all_df.groupby('season')['total_rentals_agg'].mean().sort_values()
colors = ['lightblue'] * len(season_avg)
colors[-1] = 'blue'
season_avg.plot(kind='bar', color=colors, ax=ax)
ax.set_ylabel('Jumlah Peminjaman')
ax.set_xlabel('Musim')
ax.set_xticklabels(season_avg.index, rotation=0)
st.pyplot(fig)