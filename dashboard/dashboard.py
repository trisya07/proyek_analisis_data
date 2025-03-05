import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
all_df = pd.read_csv('dashboard/main_data.csv')

# Streamlit page configuration
st.set_page_config(page_title="Analisis Peminjaman Sepeda", layout="wide")

# Title
st.title("Dashboard Analisis Peminjaman Sepeda")

all_df['date_day'] = pd.to_datetime(all_df['date_day'], errors='coerce')

# Filtering: Date Range
st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Start Date", all_df['date_day'].min())
end_date = st.sidebar.date_input("End Date", all_df['date_day'].max())

# Filter berdasarkan rentang tanggal, jika tidak ada filter, tampilkan seluruh data
if start_date and end_date:
    filtered_df = all_df[(all_df['date_day'] >= pd.to_datetime(start_date)) & (all_df['date_day'] <= pd.to_datetime(end_date))]
else:
    filtered_df = all_df

# Filtering: Musim (Season)
season_filter = st.sidebar.multiselect("Filter berdasarkan musim", options=["All"] + list(all_df['season'].unique()), default=["All"])
if "All" not in season_filter and season_filter:
    filtered_df = filtered_df[filtered_df['season'].isin(season_filter)]

# Filtering: Cuaca (Weather)
weather_filter = st.sidebar.multiselect("Filter berdasarkan cuaca", options=["All"] + list(all_df['weathersit'].unique()), default=["All"])
if "All" not in weather_filter and weather_filter:
    filtered_df = filtered_df[filtered_df['weathersit'].isin(weather_filter)]

# Rata-rata Peminjaman Berdasarkan Musim
st.header("Rata-rata Peminjaman Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(8, 5))
season_avg = filtered_df.groupby('season')['total_rentals_agg'].mean().sort_values()
colors = ['lightblue'] * len(season_avg)
colors[-1] = 'blue'
season_avg.plot(kind='bar', color=colors, ax=ax)
ax.set_ylabel('Jumlah Peminjaman')
ax.set_xlabel('Musim')
ax.set_xticklabels(season_avg.index, rotation=0)
st.pyplot(fig)

# Rata-rata Peminjaman Berdasarkan Kondisi Cuaca
st.header("Rata-rata Peminjaman Berdasarkan Kondisi Cuaca")
fig, ax = plt.subplots(figsize=(8, 5))
weather_avg = filtered_df.groupby('weathersit')['total_rentals_agg'].mean().sort_values()
colors = ['lightblue'] * len(weather_avg)
colors[-1] = 'blue'
weather_avg.plot(kind='bar', color=colors, ax=ax)
ax.set_ylabel('Jumlah Peminjaman')
ax.set_xticklabels(weather_avg.index, rotation=0)
st.pyplot(fig)

# Rata-rata Peminjaman: Hari Kerja vs Hari Libur
st.header("Rata-rata Peminjaman: Hari Kerja vs Hari Libur")
fig, ax = plt.subplots(figsize=(8, 5))
workingday_avg = filtered_df.groupby('workingday')['total_rentals_agg'].mean()
colors = ['lightblue', 'blue']
workingday_avg.plot(kind='bar', color=colors, ax=ax)
ax.set_ylabel('Jumlah Peminjaman')
ax.set_xticklabels(['Non-Working Day', 'Working Day'], rotation=0)
st.pyplot(fig)

# Rata-rata Peminjaman Berdasarkan Bulan
st.header("Rata-rata Peminjaman Berdasarkan Bulan")
fig, ax = plt.subplots(figsize=(10, 5))
month_avg = filtered_df.groupby('month')['total_rentals_agg'].mean().sort_values()
colors = ['lightgray'] * len(month_avg)
colors[-1] = 'blue'
ax.barh(month_avg.index, month_avg, color=colors)
st.pyplot(fig)

# Rata-rata Peminjaman Berdasarkan Hari dalam Seminggu
st.header("Rata-rata Peminjaman Berdasarkan Hari dalam Seminggu")
fig, ax = plt.subplots(figsize=(8, 5))
weekday_avg = filtered_df.groupby('weekday')['total_rentals_agg'].mean().sort_values()
colors = ['gray'] * len(weekday_avg)
colors[-1] = 'red'
ax.plot(weekday_avg.index, weekday_avg, marker='o', linestyle='-', color='gray')
ax.scatter(weekday_avg.index[-1], weekday_avg.iloc[-1], color='red', s=100, label='Tertinggi')
ax.set_ylabel('Jumlah Peminjaman')
ax.set_xlabel('Hari')
ax.set_xticklabels(weekday_avg.index, rotation=45)
ax.legend()
st.pyplot(fig)

# Pie Chart - Rasio Peminjaman Casual vs Registered
st.header("Rasio Peminjaman Casual vs Registered")
fig, ax = plt.subplots(figsize=(6, 6))
labels = ['Casual', 'Registered']
sizes = [filtered_df['casual_agg'].mean(), filtered_df['registered_agg'].mean()]
colors = ['lightblue', 'royalblue']
ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
ax.set_title('Rasio Peminjaman Casual vs Registered')
st.pyplot(fig)

# Tentukan kategori berdasarkan jumlah peminjaman
st.header("Kategori Peminjaman Sepeda")
st.markdown("""Tujuan dari teknik analisa ini adalah untuk mengklasifikasikan jumlah peminjaman sepeda ke dalam beberapa kategori berdasarkan nilai total_rentals_agg.""")
bins = [0, 1000, 5000, 10000]
labels = ['Low', 'Medium', 'High']
filtered_df['Rental_Category'] = pd.cut(filtered_df['total_rentals_agg'], bins=bins, labels=labels)

# Hitung frekuensi setiap kategori
category_counts = filtered_df['Rental_Category'].value_counts()

# Gabungkan frekuensi ke dalam DataFrame
filtered_df = filtered_df.merge(category_counts.rename('frequency'), left_on='Rental_Category', right_index=True, how='left')

# Analisis berdasarkan kategori
category_summary = filtered_df.groupby('Rental_Category').agg({'total_rentals_agg': 'mean', 'frequency': 'mean'})
st.write(category_summary)