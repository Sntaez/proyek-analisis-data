import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
file_path = "dashboard/main_data.csv"
df = pd.read_csv(file_path)

# Pastikan kolom tanggal dalam format datetime
df["dteday"] = pd.to_datetime(df["dteday"])

# Mapping nama bulan, musim, dan hari
bulan_mapping = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "Mei", 6: "Jun",
                 7: "Jul", 8: "Agu", 9: "Sep", 10: "Okt", 11: "Nov", 12: "Des"}

musim_mapping = {1: "Semi", 2: "Panas", 3: "Gugur", 4: "Dingin"}

hari_mapping = {0: "Minggu", 1: "Senin", 2: "Selasa", 3: "Rabu", 
                4: "Kamis", 5: "Jumat", 6: "Sabtu"}

weather_labels = {1: "Cerah", 2: "Berawan & Berkabut", 3: "Salju/Hujan Ringan"}
df["weathersit"] = df["weathersit"].replace(weather_labels)

# Sidebar
st.sidebar.title("Filter Data")

# Filter rentang tanggal
start_date = st.sidebar.date_input("Mulai Tanggal", df["dteday"].min(), min_value=df["dteday"].min(), max_value=df["dteday"].max())
end_date = st.sidebar.date_input("Sampai Tanggal", df["dteday"].max(), min_value=df["dteday"].min(), max_value=df["dteday"].max())

# Filter musim dan cuaca
selected_seasons = st.sidebar.multiselect("Pilih Musim", list(musim_mapping.values()), default=list(musim_mapping.values()))
selected_weather = st.sidebar.multiselect("Pilih Kondisi Cuaca", list(weather_labels.values()), default=list(weather_labels.values()))

# Filter dataset berdasarkan pilihan pengguna
filtered_df = df[(df["dteday"] >= pd.to_datetime(start_date)) & (df["dteday"] <= pd.to_datetime(end_date))]

if selected_seasons:
    filtered_df = filtered_df[filtered_df["season"].map(musim_mapping).isin(selected_seasons)]
if selected_weather:
    filtered_df = filtered_df[filtered_df["weathersit"].isin(selected_weather)]

# Main Page
st.title("Dashboard Bike Sharing 🚲")

## Ringkasan Data Penyewaan Sepeda
st.header("📌Ringkasan Data Penyewaan Sepeda")
st.write(filtered_df.describe())

# Distribusi Penyewaan Sepeda
st.subheader("Distribusi Penyewaan Sepeda")
fig, ax = plt.subplots()
sns.histplot(filtered_df["cnt"], bins=30, kde=True, ax=ax, color=sns.color_palette("viridis")[3])
    
# Mengubah label sumbu X
ax.set_xlabel("\nJumlah Penyewaan")
ax.set_ylabel("Jumlah Hari\n")
st.pyplot(fig)

# Tren Penyewaan Sepeda Sepanjang Tahun
st.subheader("Tren Rata-rata Penyewaan Sepeda Per Bulan")
monthly_avg = filtered_df.groupby(['yr', 'mnth'])['cnt'].mean().reset_index()
monthly_avg['yr'] = monthly_avg['yr'].map({0: 2011, 1: 2012})

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=monthly_avg['mnth'], y=monthly_avg['cnt'], hue=monthly_avg['yr'], marker="o", palette={2011: "blue", 2012: "orange"})
ax.set_xticks(range(1, 13))
ax.set_xticklabels([bulan_mapping[i] for i in range(1, 13)])
ax.set_xlabel("Bulan")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
ax.set_title("Tren Rata-rata Penyewaan Sepeda Per Bulan pada 2011 & 2012")
ax.legend(title="Tahun")
st.pyplot(fig)

# Filter Tampilkan Data Berdasarkan
st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Kategori")
options = st.multiselect("Tampilkan Data Berdasarkan:", ["Hari", "Bulan", "Musim", "Cuaca"], default=["Hari", "Bulan", "Musim", "Cuaca"])

fig, ax = plt.subplots(figsize=(10, 5))

if "Hari" in options:
    avg_by_weekday = filtered_df.groupby("weekday")["cnt"].mean()
    sns.barplot(x=[hari_mapping[i] for i in avg_by_weekday.index], y=avg_by_weekday.values, palette="magma", ax=ax)
    ax.set_xlabel("Hari")
    ax.set_ylabel("Rata-rata Penyewaan Sepeda")
    ax.set_title("Rata-rata Penyewaan Sepeda per Hari")
    st.pyplot(fig)
    fig, ax = plt.subplots(figsize=(10, 5))

if "Bulan" in options:
    avg_by_month = filtered_df.groupby("mnth")["cnt"].mean()
    sns.barplot(x=[bulan_mapping[i] for i in avg_by_month.index], y=avg_by_month.values, palette="viridis", ax=ax)
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Rata-rata Penyewaan Sepeda")
    ax.set_title("Rata-rata Penyewaan Sepeda per Bulan")
    st.pyplot(fig)
    fig, ax = plt.subplots(figsize=(10, 5))

if "Musim" in options:
    avg_by_season = filtered_df.groupby("season")["cnt"].mean()
    sns.barplot(x=[musim_mapping[i] for i in avg_by_season.index], y=avg_by_season.values, palette="coolwarm", ax=ax)
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Penyewaan Sepeda")
    ax.set_title("Rata-rata Penyewaan Sepeda per Musim")
    st.pyplot(fig)
    fig, ax = plt.subplots(figsize=(10, 5))

if "Cuaca" in options:
    weather_avg = filtered_df.groupby("weathersit")["cnt"].mean().reset_index()
    sns.barplot(x='weathersit', y='cnt', data=weather_avg, palette='viridis', ax=ax)
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Rata-rata Penyewaan Sepeda")
    ax.set_title("Rata-rata Penyewaan Sepeda pada Setiap Cuaca")
    st.pyplot(fig)
