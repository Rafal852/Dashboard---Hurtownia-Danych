import pandas as pd

df = pd.read_excel('zamowienia_hurtownia_danych.xlsx', engine='openpyxl')
print("File loaded successfully. Number of records:", len(df))

print("\nSummary of missing values per column:")
missing_data = df.isnull().sum()
print(missing_data)


print("\nChecking for duplicates:")
duplicates = df.duplicated().sum()
print("Number of duplicates:", duplicates)


print("\nStatistics for numerical columns:")
print(df.describe())


if 'Kraj' in df.columns:
    df['Kraj'] = df['Kraj'].str.strip().str.title()

if 'Data zamówienia' in df.columns:
    df['Data zamówienia'] = pd.to_datetime(df['Data zamówienia'], errors='coerce')
    invalid_dates = df[df['Data zamówienia'].isnull()]
    if not invalid_dates.empty:
        print("\nInvalid dates:\n", invalid_dates)

if 'Sprzedaż (netto)' in df.columns:
    df['Sprzedaż (netto)'] = df['Sprzedaż (netto)'].replace('[\$,]', '', regex=True).astype(float)

if 'Sprzedaż (brutto)' in df.columns:
    df['Sprzedaż (brutto)'] = df['Sprzedaż (brutto)'].replace('[\$,]', '', regex=True).astype(float)

if 'VAT' in df.columns:
    df['VAT'] = df['VAT'].replace('[\$,]', '', regex=True).astype(float)

df_clean = df.drop_duplicates()

if 'Kanał Sprzedaży' in df_clean.columns:
    df_clean['Kanał Sprzedaży'] = df_clean['Kanał Sprzedaży'].fillna('Nieokreślony')

df_clean['Rok'] = df_clean['Data zamówienia'].dt.year
df_clean['Miesiąc'] = df_clean['Data zamówienia'].dt.month_name(locale='pl') 

df_clean['Dzień tygodnia'] = df_clean['Data zamówienia'].dt.day_name(locale='pl')

bins = [0, 1000, 5000, float('inf')]
labels = ['Niska', 'Średnia', 'Wysoka']
df_clean['Kategoria sprzedaży'] = pd.cut(df_clean['Sprzedaż (netto)'], bins=bins, labels=labels)

def okres_sezonowy(miesiac):
    if miesiac in [12, 1, 2]:
        return 'Zima'
    elif 3 <= miesiac <= 5:
        return 'Wiosna'
    elif 6 <= miesiac <= 8:
        return 'Lato'
    else:
        return 'Jesień'

df_clean['Sezon'] = df_clean['Data zamówienia'].dt.month.apply(okres_sezonowy)

df_clean['Przedział cenowy'] = pd.qcut(df_clean['Sprzedaż (netto)'], q=4, labels=['Ekonomiczny', 'Standard', 'Premium', 'Premium Plus'])

df_clean.to_excel('cleaned_data_with_columns.xlsx', index=False)
print("\nCleaned and transformed data saved to file: cleaned_data.xlsx")

print("\nData Cleaning Report:")
print(f"Initial number of records: {len(df)}")
print(f"Number of records after removing duplicates: {len(df_clean)}")
print(f"Missing values:\n{missing_data}")
