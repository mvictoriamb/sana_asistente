import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/calendar.readonly'
]

def autenticar_cuenta(nombre_cuenta, archivo_token):
    creds = None
    
    if os.path.exists(archivo_token):
        try:
            creds = Credentials.from_authorized_user_file(archivo_token, SCOPES)
        except Exception:
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None
        
        if not creds:
            print(f"\n>>> ⚠️ SE REQUIERE LOGIN PARA: {nombre_cuenta} <<<")
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(archivo_token, 'w') as token:
            token.write(creds.to_json())

    return creds


if __name__ == "__main__":
    # Nombres EXACTOS de los archivos que main.py espera
    cuentas = {
        "Personal": "token_personal.json",
        "UMA": "token_uma.json",
        "Secundaria": "token_tercero.json"
    }

    for nombre, archivo in cuentas.items():
        print(f"\n--- Preparando token para: {nombre} ---")
        creds_generadas = autenticar_cuenta(nombre, archivo)
        if creds_generadas and creds_generadas.valid:
            print(f"✅ Token generado correctamente para {nombre}.")
        else:
            print(f"❌ Fallo al generar el token para {nombre}.")
