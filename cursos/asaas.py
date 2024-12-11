import requests

# Configurações da API do Asaas
ASAAS_API_URL = "https://www.asaas.com/api/v3/"
ASAAS_API_KEY = "$aact_MzkwODA2MWY2OGM3MWRlMDU2NWM3MzJlNzZmNGZhZGY6OmFkZjk3MTVjLWJiOTctNDkyZC04YmM0LTc4NDlhMmNmNDQwMDo6JGFhY2hfNzUxMjkyOTgtMzg0My00MDA0LTkzYjAtYjQ0YjU1NDlmYWJh"

def criar_cliente(nome, email, cpfCnpj):
    """Cria um cliente no Asaas com CPF ou CNPJ."""
    url = f"{ASAAS_API_URL}customers"
    headers = {
        "Content-Type": "application/json",
        "access_token": ASAAS_API_KEY,
    }
    payload = {
        "name": nome,
        "email": email,
        "cpfCnpj": cpfCnpj,  # Envia o CPF/CNPJ
    }

    print(f"Enviando requisição para criar cliente com payload: {payload}")
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code in [200, 201]:
        cliente_data = response.json()
        print(f"Cliente criado com sucesso: {cliente_data}")
        return cliente_data.get("id")
    else:
        raise Exception(f"Erro ao criar cliente: {response.status_code} - {response.text}")


def criar_cobranca_pix(nome_cliente, valor, email_cliente, descricao, cpfCnpj):
    """Cria uma cobrança PIX no Asaas."""
    # Primeiro, cria o cliente
    cliente_id = criar_cliente(nome_cliente, email_cliente, cpfCnpj)

    # Depois, cria a cobrança
    url = f"{ASAAS_API_URL}payments"
    headers = {
        "Content-Type": "application/json",
        "access_token": ASAAS_API_KEY,
    }
    payload = {
        "customer": cliente_id,
        "billingType": "PIX",
        "dueDate": "2024-12-15",  # Ajuste conforme necessário
        "value": float(valor),  # Garante que é serializável
        "description": descricao,
    }

    response = requests.post(url, headers=headers, json=payload)
    print("Resposta completa da API ao criar cobrança:", response.json())  # Log da resposta

    if response.status_code in [200, 201]:
        payment_data = response.json()
        print(f"Cobrança criada com sucesso: {payment_data}")
        return payment_data.get("invoiceUrl"), payment_data.get("pixQrCode")
    else:
        raise Exception(f"Erro ao criar cobrança: {response.status_code} - {response.text}")


