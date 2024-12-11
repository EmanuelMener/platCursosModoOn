import requests

# Configurações da API do Asaas
ASAAS_API_URL = "https://sandbox.asaas.com/api/v3/"
ASAAS_API_KEY = "$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDAwOTY0OTg6OiRhYWNoXzVkMGEyMDhiLTNhYTYtNDI1Ny05OGYwLWZlMDVkYjk5Y2FlNA=="

def testar_autenticacao():
    """Testa a autenticação na API do Asaas."""
    url = f"{ASAAS_API_URL}myAccount"
    headers = {
        "Content-Type": "application/json",
        "access_token": ASAAS_API_KEY,
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Autenticação bem-sucedida:", response.json())
    else:
        print(f"Erro na autenticação: {response.status_code} - {response.text}")

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
        "cpfCnpj": cpfCnpj,
    }

    print(f"Enviando requisição para criar cliente com payload: {payload}")
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code in [200, 201]:
        cliente_data = response.json()
        print(f"Cliente criado com sucesso: {cliente_data}")
        return cliente_data.get("id")
    else:
        raise Exception(f"Erro ao criar cliente: {response.status_code} - {response.text}")

def criar_cobranca_pix(cliente_id, valor, descricao):
    """Cria uma cobrança PIX no Asaas para um cliente existente."""
    url = f"{ASAAS_API_URL}payments"
    headers = {
        "Content-Type": "application/json",
        "access_token": ASAAS_API_KEY,
    }
    payload = {
        "customer": cliente_id,
        "billingType": "PIX",
        "dueDate": "2024-12-15",
        "value": valor,
        "description": descricao,
    }

    print(f"Enviando requisição para criar cobrança com payload: {payload}")
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code in [200, 201]:
        payment_data = response.json()
        print(f"Cobrança criada com sucesso. Resposta completa: {payment_data}")
        return payment_data.get("invoiceUrl"), payment_data.get("pixQrCode")
    else:
        raise Exception(f"Erro ao criar cobrança: {response.status_code} - {response.text}")


# Testes
if __name__ == "__main__":
    try:
        testar_autenticacao()

        # CPF de teste (use um CPF válido para testes)
        cpf_teste = "12345678909"  # Substitua por um CPF válido para teste

        # Teste de criação de cliente com CPF
        cliente_id = criar_cliente("Cliente Teste", "cliente.teste@exemplo.com", cpf_teste)
        print(f"Cliente criado com ID: {cliente_id}")

        # Teste de criação de cobrança PIX
        invoice_url, pix_qr_code = criar_cobranca_pix(
            cliente_id=cliente_id,
            valor=120.50,
            descricao="Teste de cobrança PIX via Asaas"
        )
        print(f"Cobrança criada com sucesso!")
        print(f"Link da fatura: {invoice_url}")
        print(f"QR Code PIX: {pix_qr_code}")

    except Exception as e:
        print(f"Erro durante o processo: {e}")
