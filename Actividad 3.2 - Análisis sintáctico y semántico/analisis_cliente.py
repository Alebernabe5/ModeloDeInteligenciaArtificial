import spacy
from spacy import displacy
from spacy.pipeline import EntityRuler
from spacytextblob.spacytextblob import SpacyTextBlob
import random
import os

# 1. PREPARACIÓN DEL ENTORNO
# Cargar el large que incluye vectores de palabras 
nlp = spacy.load("es_core_news_lg")

# INTEGRACIÓN DE SENTIMIENTO (Componente Custom) 
if "spacytextblob" not in nlp.pipe_names:
    nlp.add_pipe('spacytextblob')

# CONFIGURACIÓN DEL ENTITY RULER 
# Añadir reglas manuales antes del NER estándar
if "entity_ruler" not in nlp.pipe_names:
    ruler = nlp.add_pipe("entity_ruler", before="ner")
    patterns = [
        {"label": "PRODUCTO", "pattern": "Kindle"},
        {"label": "MARCA", "pattern": "Amazon"},
        {"label": "SOFTWARE", "pattern": "Calibre"},
        {"label": "PRODUCTO", "pattern": "ebook"},
        {"label": "CARACTERÍSTICA", "pattern": "Verde matcha"}
    ]
    ruler.add_patterns(patterns)

# 2. CARGA DE DATOS Y PROCESAMIENTO INICIAL
dataText = "comentariosKindle.txt"

if os.path.exists(dataText):
    with open(dataText, "r", encoding="utf-8") as file:
        text = file.read().strip()
    
    if not text:
        print(f"Error: El archivo {dataText} está vacío.")
        exit()
    
    # Generación del objeto Doc 
    doc = nlp(text) 
else:
    print(f"Error: El archivo {dataText} no existe en la carpeta.")
    exit()

# --- FUNCIÓN DE LIMPIEZA (Paso 2 - Preprocessing) ---
def cleaning_pro(texto):
    doc_temp = nlp(texto)
    # Devuelve lemas omitiendo stopwords, puntuación y espacios
    return [t.lemma_.lower() for t in doc_temp if not t.is_stop and not t.is_punct and not t.is_space]


# EJECUCIÓN Y MOSTRADO DE RESULTADOS


# ENTIDADES (NER)
print("\n" + "="*45)
print("PASO 3: EXTRACCIÓN DE ENTIDADES NOMBRADAS")
print("="*45)
print(f"{'Texto':<20} | {'Etiqueta':<15} | {'Descripción'}")
print("-" * 70)
for ent in doc.ents:
    print(f"{ent.text:<20} | {ent.label_:<15} | {spacy.explain(ent.label_)}")


# ANÁLISIS DE SENTIMIENTO 
print("\n" + "="*45)
print("ANÁLISIS DE SENTIMIENTO GLOBAL")
print("="*45)
score = doc._.blob.polarity
print(f"Score de Sentimiento (Polaridad): {score:.2f}")
print("Interpretación: " + ("Positivo" if score > 0.1 else "Negativo" if score < -0.1 else "Neutro"))


#  DESCUBRIMIENTO DEL TÓPICO
print("\n" + "="*45)
print("DESCUBRIMIENTO DEL TÓPICO")
print("="*45)

# Estrategia A: Sustantivos mas frecuentes
nouns = [t.lemma_.lower() for t in doc if t.pos_ == "NOUN" and not t.is_stop]
frequency = {s: nouns.count(s) for s in set(nouns)}
top_5 = sorted(frequency.items(), key=lambda x: x[1], reverse=True)[:5]
print(f"[Estrategia A] Sustantivos más frecuentes: {top_5}")

# Estrategia B: Similitud Semántica
category = ["tecnología", "política", "deportes", "cocina"]
print("[Estrategia B] Similitud con categorías:")
for cat in category:
    sim = doc.similarity(nlp(cat))
    print(f" - {cat}: {sim:.4f}")


# --- MOSTRAR PASO 2: ANÁLISIS GRAMATICAL (Final) ---
print("\n" + "="*45)
print("PASO 2: ANÁLISIS SINTÁCTICO (ORACIÓN AL AZAR)")
print("="*45)
prayers = list(doc.sents)
if prayers:
    phrase_ejem = random.choice(prayers)
    print(f"Frase seleccionada: {phrase_ejem.text}\n")
    print(f"{'Token':<15} | {'POS':<10} | {'DEP':<10}") #Muestra que tipo de palabra es cada token y su función sintáctica
    print("-" * 40)
    for token in phrase_ejem:
        print(f"{token.text:<15} | {token.pos_:<10} | {token.dep_:<10}")
        if token.pos_ in ["VERB", "AUX"]: #Identifica el nucleo de la oracion
            status = "PRINCIPAL (ROOT)" if token.dep_ == "ROOT" else "AUXILIAR"
            print(f"   >>> Verbo {status} identificado")

    # LANZAR VISOR 
    print("\nAbriendo visor del árbol en http://127.0.0.1:5000")
    print("Pulsa Ctrl+C para finalizar arbol")
    displacy.serve(phrase_ejem, style="dep")