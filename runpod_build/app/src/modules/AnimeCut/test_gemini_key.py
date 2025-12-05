import google.generativeai as genai
import os

# Chave fornecida pelo usuário
API_KEY = "AIzaSyB1xrzEStrgNAEdzyYzHtE0odJJlvDLAmM"

def test_key():
    print(f"Testando chave: {API_KEY[:10]}...")
    try:
        genai.configure(api_key=API_KEY)
        
        # Lista modelos disponíveis
        print("Listando modelos disponíveis...")
        models = [m.name for m in genai.list_models()]
        print(f"Modelos encontrados: {len(models)}")
        
        target_model = "models/gemini-2.0-flash"
        if target_model in models:
            print(f"Modelo alvo '{target_model}' esta disponivel!")
        else:
            print(f"Modelo alvo '{target_model}' NAO encontrado na lista.")
            print("Modelos disponiveis:", models)
            
        # Teste de geração simples
        print("Testando geracao de texto...")
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content("Ola, isso e um teste de API.")
        print(f"Resposta recebida: {response.text}")
        
        print("\nSUCESSO! A chave e o modelo estao funcionando.")
        return True
        
    except Exception as e:
        print(f"\nERRO: {e}")
        return False

if __name__ == "__main__":
    test_key()
