#!/usr/bin/env python
"""
Ejecuta 
"""
import subprocess
import sys
import time

def main():
    print("""
         Anime & Manga     
    """)
    
    try:
        result = subprocess.run(
            [sys.executable, "setup_database.py"],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error en setup: {e.stderr}")
        sys.exit(1)
    
    # Paso 2: Verificar dependencias
    print("\n[2/3]  Verificando dependencias...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"],
            check=True
        )
        print(" Dependencias listas")
    except subprocess.CalledProcessError as e:
        print(f"Error instalando dependencias: {e}")
        sys.exit(1)
    
    time.sleep(1)
    
    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "dashboard.py"],
            check=False
        )
    except KeyboardInterrupt:
        print("\n\n Dashboard cerrado")
        sys.exit(0)

if __name__ == "__main__":
    main()
