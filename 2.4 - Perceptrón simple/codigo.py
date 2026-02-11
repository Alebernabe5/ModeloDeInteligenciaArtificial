import pandas as pd
import numpy as np

# ==========================================
# PASO 1: SELECCIÓN Y PREPARACIÓN DEL DATO
# ==========================================
ruta = 'data.csv'  # Asegúrate de que el archivo se llame así en tu carpeta

try:
    # Carga de datos con detección de separador
    df = pd.read_csv(ruta, sep=None, engine='python')
    print(f"✅ Archivo cargado. Filas originales: {len(df)}")

    # 1.1 Limpieza: Eliminar columna de ID y la columna vacía 'Unnamed: 32'
    # Esto es crucial para que dropna() no elimine todos los datos
    df = df.drop(columns=['id', 'Unnamed: 32'], errors='ignore')

    # 1.2 Codificación: Convertir 'diagnosis' (M/B) a numérico (1/0)
    if 'diagnosis' in df.columns:
        df['diagnosis'] = df['diagnosis'].map({'M': 1, 'B': 0})

    # 1.3 Eliminar filas con valores nulos restantes
    df_clean = df.dropna()
    print(f"✅ Datos tras limpieza: {len(df_clean)} filas.")

    # 1.4 Selección de variables independientes (Features) y dependiente (Target)
    # Seleccionamos 3 variables físicas representativas
    features = ['radius_mean', 'texture_mean', 'perimeter_mean']
    X = df_clean[features].values.astype(float)
    y = df_clean['diagnosis'].values

    # 1.5 Normalización (Z-Score): Escalar los datos para que el Perceptrón converja
    X_std = np.copy(X)
    for i in range(X.shape[1]):
        X_std[:, i] = (X[:, i] - X[:, i].mean()) / X[:, i].std()
    
    print("✅ Normalización completada.")

except Exception as e:
    print(f"❌ Error en la preparación de datos: {e}")
    X_std, y = None, None

# ==========================================
# PASO 2: DESARROLLO DEL NÚCLEO (CLASE)
# ==========================================
class Perceptron:
    def __init__(self, eta=0.01, n_iter=50):
        self.eta = eta          # Tasa de aprendizaje
        self.n_iter = n_iter    # Épocas (iteraciones)

    def fit(self, X, y):
        """Ajusta los pesos entrenando con los datos X e y"""
        # Inicializamos pesos: [bias, w1, w2, w3]
        self.w_ = np.zeros(1 + X.shape[1])
        self.errors_ = []

        for _ in range(self.n_iter):
            errors = 0
            for xi, target in zip(X, y):
                # Regla de actualización del Perceptrón
                update = self.eta * (target - self.predict(xi))
                self.w_[1:] += update * xi
                self.w_[0] += update  # Actualización del sesgo (bias)
                errors += int(update != 0.0)
            self.errors_.append(errors)
        return self

    def net_input(self, X):
        """Calcula el valor neto (z) antes de la activación"""
        return np.dot(X, self.w_[1:]) + self.w_[0]

    def predict(self, X):
        """Función de activación: Escalón unitario (Heaviside)"""
        return np.where(self.net_input(X) >= 0.0, 1, 0)

# # ==========================================
# PASO 3: ENTRENAMIENTO Y VALIDACIÓN
# ==========================================
if X_std is not None:
    # 3.1 División manual (Split) 80% Entrenamiento / 20% Test
    limit = int(len(X_std) * 0.8)
    X_train, X_test = X_std[:limit], X_std[limit:]
    y_train, y_test = y[:limit], y[limit:]

    # 3.2 Instanciar y Entrenar
    # eta: tasa de aprendizaje, n_iter: número de épocas
    modelo = Perceptron(eta=0.01, n_iter=50)
    modelo.fit(X_train, y_train)
    print("✅ Entrenamiento finalizado.")

    # 3.3 Evaluación del rendimiento en ENTRENAMIENTO
    preds_train = modelo.predict(X_train)
    accuracy_train = np.mean(preds_train == y_train) * 100

    # 3.4 Evaluación del rendimiento en TEST
    preds_test = modelo.predict(X_test)
    accuracy_test = np.mean(preds_test == y_test) * 100
    
    # 3.5 Salida por consola detallada
    print("-" * 40)
    print("ESTADÍSTICAS DEL MODELO:")
    print(f"📊 Precisión en Entrenamiento: {accuracy_train:.2f}%")
    print(f"🎯 Precisión en Test (Validación): {accuracy_test:.2f}%")
    print("-" * 40)
    print(f"Pesos finales (w): {modelo.w_[1:]}")
    print(f"Sesgo final (bias): {modelo.w_[0]}")
    print("-" * 40)

    # Opcional: Ver si el error llegó a cero
    if modelo.errors_[-1] == 0:
        print("💡 El modelo convergió perfectamente (error 0).")
    else:
        print(f"💡 El modelo terminó con {modelo.errors_[-1]} errores en la última época.")