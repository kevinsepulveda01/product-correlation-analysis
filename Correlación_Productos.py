import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import lil_matrix

def main():
    # Cargar datos y tomar muestra del 50%
    file_path = r""
    df = pd.read_csv(file_path).sample(frac=0.5, random_state=42)
    
    # Filtrar datos relevantes
    df_clean = df[df['part_nbr_MOD'].notna()][['NUM_FACTURA', 'part_nbr_MOD']]
    
    # Configuración de parámetros
    min_transactions = 50
    final_relations = []

    # Filtrar partes frecuentes
    part_counts = df_clean['part_nbr_MOD'].value_counts()
    frequent_parts = part_counts[part_counts >= min_transactions].index
    
    if len(frequent_parts) >= 2:
        # Mapeo de índices
        part_to_idx = {part: i for i, part in enumerate(frequent_parts)}
        transactions = df_clean[df_clean['part_nbr_MOD'].isin(frequent_parts)]
        transactions = transactions.groupby('NUM_FACTURA')['part_nbr_MOD'].apply(list)

        # Matriz de co-ocurrencia
        co_matrix = lil_matrix((len(frequent_parts), len(frequent_parts)), dtype=np.int32)
        
        for parts in transactions:
            indices = [part_to_idx[p] for p in parts if p in part_to_idx]
            for i in range(len(indices)):
                for j in range(i+1, len(indices)):
                    co_matrix[indices[i], indices[j]] += 1
                    co_matrix[indices[j], indices[i]] += 1

        # Calcular similitud coseno
        cosine_sim = cosine_similarity(co_matrix)
        
        # Generar heatmap para top 10 partes
        top_n = min(10, len(frequent_parts))
        top_parts = frequent_parts[:top_n]
        
        plt.figure(figsize=(12, 10))
        sns.heatmap(
            cosine_sim[:top_n, :top_n],
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            xticklabels=top_parts,
            yticklabels=top_parts,
            linewidths=0.5
        )
        plt.title(f'Matriz de Correlación (Top {top_n} Partes)')
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        
        heatmap_path = r""
        plt.savefig(heatmap_path)
        plt.close()
        print(f"Heatmap guardado en: {heatmap_path}")

        # Almacenar relaciones
        for i in range(len(frequent_parts)):
            for j in range(i+1, len(frequent_parts)):
                score = cosine_sim[i, j]
                final_relations.append([
                    frequent_parts[i],
                    frequent_parts[j],
                    score,
                    'Fuerte' if score >= 0.7 else 'Moderada' if score >= 0.5 else 'Débil'
                ])

    # Crear y guardar resultados
    if final_relations:
        relation_df = pd.DataFrame(final_relations, 
                                  columns=['PARTE1', 'PARTE2', 'RELACION', 'INTERPRETACION'])
        
        output_path = r""
        relation_df.to_csv(output_path, index=False, float_format='%.6f')
        print(f"Archivo guardado en: {output_path}")
    else:
        print("No se encontraron relaciones significativas.")

if __name__ == "__main__":
    main()