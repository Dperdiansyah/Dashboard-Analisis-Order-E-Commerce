import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Dashboard Analisis Order", layout="wide")
st.title("📊 Dashboard Analisis Order E-Commerce")

# Cek apakah file all_data.csv ada di lokasi yang diharapkan
if not os.path.exists("all_data.csv"):
    st.error("File 'all_data.csv' tidak ditemukan. Pastikan file berada di direktori yang benar.")
else:
# Load data hanya jika file ada
    df = pd.read_csv("all_data.csv", nrows=50000, low_memory=False, parse_dates=["order_purchase_timestamp"])

# Sidebar - Filter Tanggal
st.sidebar.header("📅 Filter Tanggal")
min_date = df["order_purchase_timestamp"].min()
max_date = df["order_purchase_timestamp"].max()

start_date, end_date = st.sidebar.date_input(
    "Pilih rentang tanggal:",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Filter DataFrame berdasarkan tanggal
filtered_df = df[
    (df["order_purchase_timestamp"] >= pd.to_datetime(start_date)) &
    (df["order_purchase_timestamp"] <= pd.to_datetime(end_date))
]

st.markdown(f"Menampilkan data dari **{start_date}** sampai **{end_date}**")

# Visualisasi 1: Jumlah Order per Bulan
st.subheader("📈 Jumlah Orderan per Bulan")
monthly_orders = (
    filtered_df["order_purchase_timestamp"]
    .dt.to_period("M")
    .value_counts()
    .sort_index()
    .to_frame()
    .reset_index()
)
monthly_orders.columns = ["order_month", "total_orders"]
monthly_orders["order_month"] = monthly_orders["order_month"].astype(str)

fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.lineplot(data=monthly_orders, x="order_month", y="total_orders", marker="o", ax=ax1)
ax1.set_title("Jumlah Order per Bulan")
ax1.set_xlabel("Bulan")
ax1.set_ylabel("Jumlah Order")
plt.xticks(rotation=45)
st.pyplot(fig1)

# Visualisasi 2: Kota dengan orderan terbanyak
st.subheader("🏙️ 5 Kota dengan Jumlah Order Terbanyak")
city_orders = filtered_df["customer_city"].value_counts().reset_index()
city_orders.columns = ["customer_city", "total_orders"]
top_cities = city_orders.head(5)

fig2, ax2 = plt.subplots(figsize=(12, 6))
sns.barplot(data=top_cities, x="customer_city", y="total_orders", ax=ax2)
ax2.set_title("5 Kota dengan Order Terbanyak")
ax2.set_xlabel("Kota")
ax2.set_ylabel("Jumlah Order")
plt.xticks(rotation=45)
st.pyplot(fig2)

# Visualisasi 3: Metode Pembayaran
st.subheader("💳 Metode Pembayaran Terpopuler")
payment_counts = filtered_df["payment_type"].value_counts()

fig3, ax3 = plt.subplots(figsize=(9, 9))
ax3.pie(payment_counts, labels=payment_counts.index, autopct="%1.1f%%", startangle=140)
ax3.set_title("Distribusi Metode Pembayaran")
ax3.axis("equal")
st.pyplot(fig3)

# Visualisasi 4: Kategori Produk dengan Penjualan Tertinggi
st.subheader("📦 Kategori Produk dengan Penjualan Tertinggi")
category_counts = filtered_df["product_category_name"].value_counts().reset_index()
category_counts.columns = ["Category", "Count"]

fig4, ax4 = plt.subplots(figsize=(12, 6))
sns.barplot(data=category_counts.head(10), x="Category", y="Count", ax=ax4)
ax4.set_title("Top 10 Kategori Produk")
ax4.set_xlabel("Kategori Produk")
ax4.set_ylabel("Jumlah Produk")
plt.xticks(rotation=45)
st.pyplot(fig4)

st.caption('Copyright © Dian Perdiansyah 2025')
