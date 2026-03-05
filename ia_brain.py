
import google.generativeai as genai
import json
import os
import datetime
import os
from dotenv import load_dotenv

# --- CONFIGURACIÓN ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def analizar_correos_con_gemini(buzon_unificado):
    """Resumen inicial general"""
    if not buzon_unificado:
        return "No hay correos nuevos."

    # Pasamos solo lo básico para no gastar tokens
    resumen_data = [{"de": m["remitente"], "asunto": m["asunto"]} for m in buzon_unificado]
    data_str = json.dumps(resumen_data, ensure_ascii=False)

    prompt = f"""
    Eres un asistente. Analiza estos correos: {data_str}
    
    1. Filtra lo que consideres importante o urgente.
    2. Genera un resumen hablado breve. NO leas la lista uno por uno, agrúpalos (ej: "Tienes 3 correos de la UMA").
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception:
        return "Error al resumir correos."

def generar_resumen_dia(texto_agenda, resumen_correos):
    """Informe del día (Agenda + Correos)"""
    dia_semana = datetime.datetime.now().weekday()
    es_finde = dia_semana >= 5
    contexto = "FIN DE SEMANA" if es_finde else "ENTRE SEMANA"

    prompt = f"""
    Asistente personal. Contexto: {contexto}.
    
    1. AGENDA: {texto_agenda if texto_agenda else "Vacía."}
    2. CORREOS: {resumen_correos}
    
    Genera un informe hablado breve y motivador.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception:
        return "Error generando informe."

def seleccionar_correo_por_voz(lista_correos, comando_usuario):
    """
    Detecta si el usuario quiere uno específico (por tema u ORDEN) o todos.
    """
    # Creamos una lista simplificada pero MANTENIENDO EL ORDEN (índices 0, 1, 2...)
    lista_ordenada = []
    for i, mail in enumerate(lista_correos):
        lista_ordenada.append(f"Índice {i+1}: De {mail['remitente']} - Asunto {mail['asunto']} (ID: {mail['id']})")
    
    data_str = "\n".join(lista_ordenada)
    
    prompt = f"""
    Tengo esta lista ordenada de correos:
    {data_str}
    
    El usuario dice: "{comando_usuario}"
    
    INSTRUCCIONES:
    1. Si el usuario pide leer "todos", "resumen de todos", "léelos todos", devuelve la palabra: ALL
    2. Si el usuario se refiere a uno por su posición ("el primero", "el último", "el segundo", "el correo de la UMA"), identifica cuál es.
    3. Devuelve SOLAMENTE el ID de ese correo.
    4. Si no coincide con nada, devuelve: NONE
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except:
        return "NONE"

def limpiar_cuerpo_para_voz(texto_cuerpo):
    """Limpia el texto del email"""
    prompt = f"Resúmelo: {texto_cuerpo[:3000]}"
    try:
        response = model.generate_content(prompt)
        return response.text
    except:

        return texto_cuerpo[:500]
