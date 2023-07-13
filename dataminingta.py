# -*- coding: utf-8 -*-
"""DataMiningTA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TsxgEOWxMKQKVZl52m35iqj-4KmOam5a
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import seaborn as sns

# Membaca data dari file CSV
data = pd.read_csv('hotel_booking.csv')

# Preprocessing data
data = data.drop(['company', 'reservation_status', 'reservation_status_date', 'name', 'email', 'phone-number', 'credit_card'], axis=1)
data['children'] = data['children'].fillna(0)
data['country'] = data['country'].fillna('Unknown')
data['agent'] = data['agent'].fillna(0)
data['country'] = data['country'].fillna('Unknown')
data['children'] = data['children'].astype(int)
data['is_canceled'] = data['is_canceled'].astype(int)

"""Mengubah nilai-nilai kategorikal menjadi numerik menggunakan LabelEncoder# New Section"""

# Inisialisasi objek LabelEncoder
label_encoder = LabelEncoder()

# Mengubah nilai-nilai kategorikal menjadi numerik menggunakan LabelEncoder
for col in data.select_dtypes(include='object').columns:
    data[col] = label_encoder.fit_transform(data[col])

"""SPLIT DATA MENJJADI PELATIHAN DAN PENGUJIAN"""

# Split data menjadi data pelatihan dan data pengujian
X = data.drop(['is_canceled'], axis=1)
y = data['is_canceled']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Mengisi missing values dengan SimpleImputer
imputer = SimpleImputer(strategy='most_frequent')
X_train = imputer.fit_transform(X_train)
X_test = imputer.transform(X_test)

# Bangun model prediktif dengan K-Nearest Neighbors
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

# Evaluasi model
y_pred = knn.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
confusion = confusion_matrix(y_test, y_pred)

# Print hasil evaluasi
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-score:", f1)
print("Confusion Matrix:")
print(confusion)

# Hitung jumlah data yang dibatalkan dan tidak dibatalkan
total_canceled = y_test.value_counts()[1]
total_not_canceled = y_test.value_counts()[0]

# Tampilkan keterangan jumlah data yang dibatalkan dan tidak dibatalkan
print("Total Canceled:", total_canceled)
print("Total Not Canceled:", total_not_canceled)

# Visualisasi Confusion Matrix
labels = ['Not Canceled', 'Canceled']
sns.heatmap(confusion, annot=True, fmt='d', cmap='Reds', xticklabels=labels, yticklabels=labels)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

# Calculate ratio of cancellation of Booking
cancelled_perc = data['is_canceled'].value_counts(normalize=True)
print(cancelled_perc)

# Calculate ratio of cancellation of Booking
cancelled_perc = data['is_canceled'].value_counts(normalize=True)
print(cancelled_perc)

plt.figure(figsize=(5, 4))
plt.title('Reservation Status Count')
plt.bar(['Not Canceled', 'Canceled'], data['is_canceled'].value_counts(), edgecolor='k', width=0.7)
plt.show()

cancel_data = data[data['is_canceled'] == 1]
plt.figure(figsize=(8, 8))
cancel_countries = cancel_data['country'].value_counts()[:10]
labels = [data[data['country'] == country]['country'].iloc[0] for country in cancel_countries.index]
plt.pie(cancel_countries, labels=labels, autopct='%.1f%%')
plt.title('Top 10 countries with reservation canceled')
plt.show()

cancel = data['is_canceled'].value_counts(normalize=True) * 100
cancel_index = ['Reserved', 'Cancelled']
print(cancel)

plt.pie(cancel, labels=['Reserved', 'Cancelled'], startangle=40, autopct='%1.f%%')
plt.legend(['Reserved', 'Cancelled'])
plt.title('Reserve Status Percent')
plt.show()

"""Faktor yang mempengaruhi pembatalan menjadi fokus pada eksperimen tugas data mining ini

"""

# Analisis faktor-faktor yang mempengaruhi pembatalan pemesanan
factors = ['lead_time', 'arrival_date_year', 'arrival_date_month', 'arrival_date_week_number', 'arrival_date_day_of_month', 'stays_in_weekend_nights', 'stays_in_week_nights', 'adults', 'children', 'babies', 'meal', 'country', 'market_segment', 'distribution_channel', 'is_repeated_guest', 'previous_cancellations', 'previous_bookings_not_canceled', 'reserved_room_type', 'assigned_room_type', 'booking_changes', 'deposit_type', 'agent', 'days_in_waiting_list', 'customer_type', 'adr', 'required_car_parking_spaces', 'total_of_special_requests']
canceled_data = data[data['is_canceled'] == 1]
not_canceled_data = data[data['is_canceled'] == 0]
canceled_data_mean = canceled_data[factors].mean()
not_canceled_data_mean = not_canceled_data[factors].mean()

plt.figure(figsize=(10, 6))
plt.bar(factors, not_canceled_data_mean, alpha=0.5, label='Not Canceled')
plt.bar(factors, canceled_data_mean, alpha=0.5, label='Canceled')
plt.xticks(rotation=90)
plt.xlabel('Factors')
plt.ylabel('Mean Value')
plt.title('Mean Values of Factors for Canceled and Not Canceled Bookings')
plt.legend()
plt.show()

"""Melihat perbandingan berapa banyak orang menginap  di waktu malam hari kerja atau waktu malam weekend"""

from sklearn.cluster import KMeans

# Select the features for the experiment
X = data[['stays_in_week_nights', 'stays_in_weekend_nights']]
y = data['is_canceled']



# Get the cluster labels
labels = kmeans.labels_

# Visualize the clusters
plt.scatter(X['stays_in_week_nights'], X['stays_in_weekend_nights'], c=labels, cmap='viridis')
plt.xlabel('Stays in Week Nights')
plt.ylabel('Stays in Weekend Nights')
plt.title('Clustering of Hotel Bookings')
plt.show()

# Count the number of canceled and not canceled bookings in each cluster
cluster_df = pd.DataFrame({'stays_in_week_nights': X['stays_in_week_nights'], 'stays_in_weekend_nights': X['stays_in_weekend_nights'], 'label': labels, 'is_canceled': y})
cluster_summary = cluster_df.groupby(['label', 'is_canceled']).size().unstack()

print('Cluster Summary:')
print(cluster_summary)
