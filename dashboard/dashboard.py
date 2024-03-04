import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

#Membuat fungsi 
def create_weekday_df(df):
    weekday_df = df.groupby('weekday_y')['cnt_y'].sum().reset_index()
    weekday_df['weekday_y'] = weekday_df['weekday_y'].replace({0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5:'Jumat', 6: 'Sabtu'})
    weekday_df = weekday_df.sort_values(by='cnt_y', ascending=False).reset_index(drop=True)
    return weekday_df

def compare_registered_casual(df):
    total_casual = df["casual_y"].sum()
    total_registered = df["registered_y"].sum()
    total_users = total_casual + total_registered

    percent_casual = (total_casual / total_users) * 100
    percent_registered = (total_registered / total_users) * 100

    print(f"Total casual users: {total_casual} ({percent_casual:.2f}%)")
    print(f"Total registered users: {total_registered} ({percent_registered:.2f}%)")

def humidity_analysis(df):
    humidity_analisis = df.groupby(by="hum_y")["cnt_y"].sum()
    sorted_hum_data = humidity_analisis.sort_values(ascending=False).reset_index()

    bins = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    labels = [f"{i:.2f}-{i+0.10:.2f}" for i in bins[:-1]]

    sorted_hum_data["humidity_range"] = pd.cut(sorted_hum_data['hum_y'], bins=bins, labels=labels)

    rentang_summary = sorted_hum_data.groupby("humidity_range")["cnt_y"].sum()

    print(rentang_summary)

all_data = pd.read_csv("all_data.csv")

datetime_columns = ["dteday"]
all_data.sort_values(by="dteday", inplace=True)
all_data.reset_index(inplace=True)
 
for column in datetime_columns:
    all_data[column] = pd.to_datetime(all_data[column])

min_date = all_data["dteday"].min()
max_date = all_data["dteday"].max()

#Membuat sidebar
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://static.vecteezy.com/system/resources/thumbnails/009/383/627/small_2x/bicycle-clipart-design-illustration-free-png.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_data[(all_data["dteday"] >= str(start_date)) & 
                (all_data["dteday"] <= str(end_date))]

day_user_df = create_weekday_df(main_df)
comparison_df = compare_registered_casual(main_df)
humidity_df = humidity_analysis(main_df) 

def display_highest_rental_day(day_user_df):
    highest_day = day_user_df.loc[0, 'weekday_y']
    highest_count = day_user_df.loc[0, 'cnt_y']

    # Plot Diagram Batang 
    plt.figure(figsize=(10, 6))
    sns.barplot(x='weekday_y', y='cnt_y', data=day_user_df, palette='viridis')
    plt.xlabel('Day of the Week')
    plt.ylabel('Total Rentals')
    plt.title('Bike Rental Analysis by Day of the Week')
    plt.xticks(rotation=45)
    st.pyplot(plt)

    st.write(f"Highest rental day: {highest_day}")
    st.write(f"Total rentals on {highest_day}: {highest_count}")

# Fungsi untuk Perbandingan Casual dan Registered
def compare_registered_casual(df):
    total_casual = df["casual_y"].sum()
    total_registered = df["registered_y"].sum()
    total_users = total_casual + total_registered

    percent_casual = (total_casual / total_users) * 100
    percent_registered = (total_registered / total_users) * 100

    results = {
        "Total Casual Users": total_casual,
        "Percent Casual Users": percent_casual,
        "Total Registered Users": total_registered,
        "Percent Registered Users": percent_registered
    }

    return pd.DataFrame([results])

# Fungsi menampilkan diagram lingkaran dan persentase
def display_user_percentages(comparison_df):
    total_casual = comparison_df["Total Casual Users"].iloc[0]
    percent_casual = comparison_df["Percent Casual Users"].iloc[0]
    total_registered = comparison_df["Total Registered Users"].iloc[0]
    percent_registered = comparison_df["Percent Registered Users"].iloc[0]

    # Membuat Pie Chart
    fig, ax = plt.subplots(figsize=(8, 8))
    labels = ['Casual Users', 'Registered Users']
    sizes = [percent_casual, percent_registered]
    colors = ['#ff9999', '#66b3ff']
    explode = (0.1, 0) 

    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  

    st.pyplot(fig)

    st.write(f"Total casual users: {total_casual} ({percent_casual:.2f}%)")
    st.write(f"Total registered users: {total_registered} ({percent_registered:.2f}%)")

#FUNGSI 3
# Fungsi untuk analisis tingkat kelembapan
def humidity_analysis(df):
    humidity_analisis = df.groupby(by="hum_y")["cnt_y"].sum()
    sorted_hum_data = humidity_analisis.sort_values(ascending=False).reset_index()

    bins = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    labels = [f"{i:.2f}-{i+0.10:.2f}" for i in bins[:-1]]

    sorted_hum_data["humidity_range"] = pd.cut(sorted_hum_data['hum_y'], bins=bins, labels=labels)

    return sorted_hum_data[['humidity_range', 'cnt_y']]

# Menampilkan diagram dan top 3 
def display_top_humidity_ranges(humidity_df):
    if "humidity_range" not in humidity_df.columns:
        st.warning("The 'humidity_range' column is missing. Please check the 'humidity_analysis' function.")
        return

    top_3_ranges = humidity_df.sort_values(by="cnt_y", ascending=False).head(3)

    palette = ["#1f78b4" if row["humidity_range"] in top_3_ranges["humidity_range"].values else "#33a02c" for _, row in humidity_df.iterrows()]

    plt.figure(figsize=(10, 6))
    sns.barplot(x='humidity_range', y='cnt_y', data=humidity_df, palette=palette)
    plt.xlabel('Humidity Range')
    plt.ylabel('Total Rentals')
    plt.title('Top 3 Humidity Ranges with Highest Bike Rentals')
    st.pyplot(plt)

    # Menampilkan detail top 3
    st.write("Top 3 Humidity Ranges with Highest Bike Rentals:")
    st.write(top_3_ranges[['humidity_range', 'cnt_y']].reset_index(drop=True))


st.header(' Dashboard Visualisasi dan Hasil Analisis Data Bike Sharing :bike:')
st.caption('Oleh Ahmad Taufiq Ramadhan | Bangkit 2024 Machine Learning Cohort')

st.subheader('Tingkat penyewaan sepeda tertinggi dalam hari')
display_highest_rental_day(day_user_df)
st.caption('Tingkat penyewaan sepeda tertinggi terdapat di hari jumat yaitu sebanyak 487790 tetapi tren peningkatan sudah dimulai dari hari kamis dengan peringkat kedua yaitu sebanyak 485395 dengan puncak hari Jumat sehingga perlu persediaan unit yang lebih banyak di hari kamis-jumat')

st.subheader('Perbandingan Pengguna yang sudah Registrasi dan Biasa')
comparison_df = compare_registered_casual(main_df)
display_user_percentages(comparison_df)
st.caption('Perbandingan antara penyewa yang sudah terdaftar dan penyewa biasa cukup jauh dimana sudah 81,17% penyewa sudah terdaftar dengan jumlah sebanyak 2.672.662 dalam total data sementara 620.017 penyewa belum terdaftar dengan persentase sebesar 18,83% sehingga perlu peningkatan promosi dan manfaat dari menjadi penyewa pendaftar sehingga semakin banyak penyewa yang pendaftar akan semakin banyak pelanggan yang setia kepada perusahaan')

st.subheader('Pengaruh Tingkat Kelembapan Udara Terhadap Tingkat penyewaan Sepeda')
humidity_df = humidity_analysis(main_df)
display_top_humidity_ranges(humidity_df)
st.caption('Berdasarkan hasil analisis dan visualisasi data dapat dilihat tingkat penyewaan paling tinggi berada di tiga rentang, yaitu 40%-50%, 50%-60%, 60%-70% dimana tingkat kelembapan yang baik berada di rentang 45%-65% sehingga tingkat kelembapan yang baik akan mendorong untuk melakukan penyewaan sepeda dimana perusahaan juga dapat ikut andil menjaga tingkat kelembapan di sekitarnya seperti penerapan kebijakan yang berdampak pada lingkungan')