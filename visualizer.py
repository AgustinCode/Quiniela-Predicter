import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Leer el archivo CSV
df = pd.read_csv('results.csv')

# Convertir la columna 'Fecha' a datetime
df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y')

# Convertir 'Posicion' a entero y 'Numero' a entero (para asegurar el tipo de dato correcto)
try:
    df['Posicion'] = df['Posicion'].astype(int)
except ValueError as e:
    print(f"Error en la conversión de 'Posicion': {e}")

try:
    df['Numero'] = df['Numero'].astype(int)
except ValueError as e:
    print(f"Error en la conversión de 'Numero': {e}")

# Verificar si hay datos faltantes
if df['Fecha'].isnull().any() or df['Posicion'].isnull().any() or df['Numero'].isnull().any():
    print("Hay datos faltantes en las columnas 'Fecha', 'Posicion' o 'Numero'.")

# Crear una figura y ejes para múltiples gráficos
fig, axs = plt.subplots(6, 4, figsize=(20, 30))

# 1. Gráfico de frecuencia de números
sns.histplot(data=df, x='Numero', kde=True, bins=50, ax=axs[0, 0])
axs[0, 0].set_title('Frecuencia de Números')
axs[0, 0].set_xlabel('Número')
axs[0, 0].set_ylabel('Frecuencia')

# 2. Números más frecuentes por posición
for pos in range(1, 21):
    ax = axs[(pos - 1) // 4 + 1, (pos - 1) % 4]
    pos_df = df[df['Posicion'] == pos]
    sns.countplot(data=pos_df, x='Numero', order=pos_df['Numero'].value_counts().index[:5], ax=ax)
    ax.set_title(f'Posición {pos}')
    ax.set_xlabel('Número')
    ax.set_ylabel('Frecuencia')
    ax.tick_params(axis='x', rotation=45)

# 3. Gráfico de calor de números por posición y fecha
pivot_df = df.pivot_table(index='Fecha', columns='Posicion', values='Numero', aggfunc='first')
sns.heatmap(pivot_df, cmap='YlOrRd', annot=True, fmt='d', ax=axs[5, 0])
axs[5, 0].set_title('Números por Posición y Fecha')
axs[5, 0].set_xlabel('Posición')
axs[5, 0].set_ylabel('Fecha')

# Crear una nueva figura para el gráfico de tendencia
fig_tendencia, ax_tendencia = plt.subplots(figsize=(15, 8))

# 4. Gráfico de líneas para ver la tendencia de los números en cada posición
for pos in range(1, 21):
    pos_df = df[df['Posicion'] == pos].copy()
    if not pos_df.empty:  # Asegurarse de que pos_df no esté vacío
        ax_tendencia.plot(pos_df['Fecha'], pos_df['Numero'], label=f'Posición {pos}')
ax_tendencia.set_title('Tendencia de Números por Posición')
ax_tendencia.set_xlabel('Fecha')
ax_tendencia.set_ylabel('Número')
ax_tendencia.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

# Ajustar el diseño y mostrar la figura
plt.tight_layout()
plt.show()

# Mostrar la figura de tendencia
plt.tight_layout()
plt.show()
