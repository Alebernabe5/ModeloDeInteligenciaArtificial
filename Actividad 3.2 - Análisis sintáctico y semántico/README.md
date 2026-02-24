# Actividad 3.2: Análisis Sintáctico y Semántico con spaCy 🚀

Este proyecto aplica técnicas avanzadas de **Procesamiento de Lenguaje Natural (NLP)** para analizar las opiniones de los usuarios sobre un producto real. El objetivo es extraer información valiosa (sentimiento, entidades y temas) de forma automatizada.

## 📦 Artículo Seleccionado
**Producto:** [Amazon Kindle (2024)](https://www.amazon.es/kindle-2024/dp/B0CP32JG8B)
> "El Kindle más ligero y compacto, con pantalla sin reflejos, pasos de página más fluidos y luz frontal ajustable."

---

🧠 Metodología y Arquitectura del Pipeline
A diferencia de un análisis básico, este proyecto utiliza un Pipeline Híbrido. Se ha modificado el flujo estándar de spaCy para integrar reglas lógicas fijas con modelos de aprendizaje estadístico:

Capa de Reglas (Heurística): Mediante el EntityRuler, aseguramos que términos específicos de Amazon no sean mal clasificados por la IA.

Capa Estadística: El modelo es_core_news_lg realiza el etiquetado morfosintáctico basándose en el contexto.

Capa de Extensión: Se añade un "bus de datos" adicional (spacy-textblob) que viaja por todo el documento calculando la carga emocional de cada palabra.

## 🔍 Análisis del Código Paso a Paso
1. Preparación del Entorno e Importaciones
Se cargan las herramientas de spaCy (displacy, EntityRuler), random para la selección de muestras y spacy-textblob para el sentimiento.

Se carga el modelo lg, fundamental para el paso de similitud semántica gracias a sus Word Vectors de 300 dimensiones.

2. Carga y Procesamiento de Datos
Se gestiona la lectura del archivo comentariosKindle.txt con codificación utf-8.

doc = nlp(text): Se genera el objeto Doc, transformando el texto plano en una estructura de datos lingüística explotable.

Limpieza (Preprocessing): Función que devuelve los lemas omitiendo stopwords y puntuación.

3. Configuración del Pipeline (Reto)
Se inyecta el EntityRuler antes del NER automático para que las palabras personalizadas (como Kindle o Calibre) tengan "personalidad" y prioridad.

Se inyecta el componente de sentimiento para que esté disponible en todo el pipeline.

4. Salidas NER y Sentimiento
Entidades: Iteración por nombres propios detectados, traduciendo etiquetas técnicas a lenguaje humano.

Score de Sentimiento: Se extrae un valor numérico (entre -1 y 1) mediante doc._.blob.polarity. Se aplica lógica para categorizar el resultado como Positivo, Negativo o Neutro.

5. Descubrimiento de Tópicos
Estrategia A (Frecuencia): Busca palabras con la etiqueta NOUN (sustantivos), identificando los temas más repetidos.

Estrategia B (Semántica): Se utiliza doc.similarity() para comparar la posición matemática (vector) de los comentarios con categorías candidatas (Tecnología, Deporte, etc.).

6. Análisis Sintáctico Visual
phrase_ejem: Selección de una oración al azar del corpus.

POS & DEP: Identificación de categorías gramaticales y relaciones de dependencia.

Identificación de Verbos: Localización visual del núcleo de la oración (ROOT) y auxiliares.

displacy.serve: Lanzamiento de un servidor local para visualizar el árbol de dependencias.

## 📊 Interpretación para el Informe Ejecutivo
Análisis Sintáctico: Permite extraer qué acciones realizan los usuarios con el producto (ej: "leer", "cargar").

Análisis de Tópicos: Capacidad de categorizar el texto por "intención" incluso si no se mencionan palabras técnicas.

Polaridad: Un score cercano a 1.0 indica satisfacción total, mientras que valores inferiores a 0 activan alertas de posibles quejas técnicas.

## 🛠️ Requisitos e Instalación

Para ejecutar este script, es necesario tener instalado Python y las siguientes librerías:

```bash
# Instalación de librerías
pip install spacy spacytextblob pandas

# Descarga del modelo de lenguaje en español (Large)
python -m spacy download es_core_news_lg

