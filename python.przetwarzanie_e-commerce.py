import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

# Ścieżka do pliku wejściowego
input_file = r"C:\Users\ceran\Downloads\przetwarzanie_e-commerce\Produkty_Hity_Dobre_Longtail_Rating_Last_3_months_kategorie_tylko_ecommerce.xlsx"
# Ścieżka do pliku wyjściowego
output_file = r"C:\Users\ceran\Downloads\przetwarzanie_e-commerce\E-commerce_hity_dobre_longtail_clean.xlsx"

def main():
    print(f"Rozpoczynam przetwarzanie pliku: {input_file}")
    
    # Wczytanie danych
    try:
        df = pd.read_excel(input_file)
        print(f"Wczytano dane. Liczba wierszy: {len(df)}")
    except Exception as e:
        print(f"Błąd podczas wczytywania pliku: {e}")
        return
        
    # Sprawdzenie struktury danych
    print("Kolumny w pliku:", df.columns.tolist())
    
    # Dostosowanie nazw kolumn jeśli to konieczne
    # Sprawdzamy, czy kolumny mają przedrostki (p., kat., itp.)
    column_mapping = {}
    for col in df.columns:
        if col.startswith('p.'):
            column_mapping[col] = col.replace('p.', '')
        elif col.startswith('kat.'):
            column_mapping[col] = col.replace('kat.', '')
        elif col.startswith('so.'):
            column_mapping[col] = col.replace('so.', '')
    
    # Jeśli mamy mapowanie, zmieniamy nazwy kolumn
    if column_mapping:
        df = df.rename(columns=column_mapping)
    
    # Upewniamy się, że mamy wszystkie potrzebne kolumny
    expected_columns = ['TOW_KOD', 'NAZWA', 'LONG_NAME_CLEAN', 'RATING']
    for col in expected_columns:
        if col not in df.columns:
            similar_cols = [c for c in df.columns if col.lower() in c.lower()]
            if similar_cols:
                print(f"Kolumna {col} nie znaleziona, ale znaleziono podobne: {similar_cols}")
            else:
                print(f"Uwaga: Brak kolumny {col} w danych")
    
    # Grupowanie i sumowanie wartości RATING dla powtarzających się TOW_KOD
    # (zakładamy, że są kolumny: TOW_KOD, NAZWA, LONG_NAME_CLEAN, RATING)
    df_grouped = df[['TOW_KOD', 'NAZWA', 'LONG_NAME_CLEAN', 'RATING']].copy()

    # Stałe zmienne do grupowania
    tow_kod_col = 'TOW_KOD'
    nazwa_col   = 'NAZWA'
    rating_col  = 'RATING'

    print(f"Grupowanie według kolumn: {tow_kod_col}, {nazwa_col}")

    # Budujemy słownik agregacji: sumujemy RATING, resztę bierzemy 'first'
    agg_dict = {rating_col: 'sum'}
    for col in df_grouped.columns:
        if col != rating_col:
            agg_dict[col] = 'first'

    # Właściwe grupowanie
    df_grouped = df_grouped.groupby([tow_kod_col, nazwa_col], as_index=False).agg(agg_dict)
    print(f"Po grupowaniu liczba wierszy: {len(df_grouped)}")
    
    # Klasyfikacja produktów za pomocą k-means dla każdej kategorii
    try:
        # Dodajemy kolumnę na wyniki klasyfikacji
        df_grouped['cluster'] = ''
        
        # Lista unikalnych kategorii
        categories = df_grouped[nazwa_col].unique()
        print(f"Znaleziono {len(categories)} unikalnych kategorii.")
        
        # Dla każdej kategorii wykonujemy klasyfikację
        for category in categories:
            if pd.isna(category):
                continue
                
            print(f"Przetwarzanie kategorii: {category}")
            
            # Filtrujemy dane dla danej kategorii
            category_df = df_grouped[df_grouped[nazwa_col] == category].copy()
            
            # Jeśli kategoria ma za mało produktów, wszystkie oznaczamy jako LONGTAIL
            if len(category_df) < 3:
                df_grouped.loc[df_grouped[nazwa_col] == category, 'cluster'] = 'Longtail'
                print(f"  Kategoria {category} ma mniej niż 3 produkty, wszystkie oznaczone jako Longtail")
                continue
            
            # Przygotowanie danych do klasyfikacji
            X = category_df[[rating_col]].values
            
            # Normalizacja danych (Min-Max Scaling)
            scaler = MinMaxScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Zastosowanie k-means z 3 klastrami
            kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
            kmeans.fit(X_scaled)
            
            # Dodanie etykiet klastrów
            category_df['temp_cluster'] = kmeans.labels_
            
            # Znalezienie średnich wartości RATING dla każdego klastra
            cluster_means = {}
            for cluster in range(3):
                cluster_means[cluster] = category_df[category_df['temp_cluster'] == cluster][rating_col].mean()
            
            # Sortowanie klastrów według średnich wartości
            sorted_clusters = sorted(cluster_means.items(), key=lambda x: x[1])
            
            # Mapowanie klastrów na kategorie produktów
            cluster_category_map = {
                sorted_clusters[2][0]: 'Hit',       # Klaster z najwyższą średnią wartością
                sorted_clusters[1][0]: 'Dobry',     # Klaster ze średnią wartością
                sorted_clusters[0][0]: 'Longtail'   # Klaster z najniższą wartością
            }
            
            # Przypisanie kategorii produktów
            for idx, row in category_df.iterrows():
                cluster_value = cluster_category_map[row['temp_cluster']]
                df_grouped.loc[idx, 'cluster'] = cluster_value
            
            # Informacja o liczbie produktów w każdej kategorii
            hits = len(category_df[category_df['temp_cluster'] == sorted_clusters[2][0]])
            good = len(category_df[category_df['temp_cluster'] == sorted_clusters[1][0]])
            longtail = len(category_df[category_df['temp_cluster'] == sorted_clusters[0][0]])
            print(f"  Kategoria {category}: Hit={hits}, Dobry={good}, Longtail={longtail}")
    
    except Exception as e:
        print(f"Błąd podczas klasyfikacji: {e}")
        return
    
    # Zapisanie wyników do pliku Excel
    try:
        # Usuwamy ewentualną kolumnę temp_cluster, jeśli istnieje
        if 'temp_cluster' in df_grouped.columns:
            df_grouped.drop('temp_cluster', axis=1, inplace=True)
            
        # Zapisujemy wyniki
        df_grouped.to_excel(output_file, index=False)
        print(f"Zapisano wyniki do pliku: {output_file}")
    except Exception as e:
        print(f"Błąd podczas zapisywania pliku: {e}")
        return
    
    print("Przetwarzanie zakończone pomyślnie!")

if __name__ == "__main__":
    main()