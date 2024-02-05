from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from models.central.user import Address
from database.central.users import UserORM
from database.central.payment_settings import PaymentSettingsORM
from database.central.address import AddressORM
from models.central.ordem_servico import OrdemServico, OrdemServicoResponse, ProductInvoice, ProductInvoiceResponse
from database.central.product_invoice import OrdemServicoORM, ProductInvoiceORM, OrdemServicoProductInvoiceORM
from database.central.company import CompanyORM
from database.central.users import UserORM
from utils.jwt_token import has_authenticated
import logging
from starlette import status
from typing import Dict, Any, List
from collections import defaultdict, Counter

import stripe
import httpx  # Import httpx instead of aiohttp
import random
logger = logging.getLogger(__name__)
router = APIRouter(prefix='/api/stripe', tags=['Stripe'])

# Configure the Stripe secret key


def contar_e_detalhar_produtos(array_de_produtos):
    resultado = []

    contador = {}
    for produto in array_de_produtos:
        chave_produto = tuple(produto.items())
        if chave_produto in contador:
            contador[chave_produto] += 1
        else:
            contador[chave_produto] = 1

    for (detalhes_produto, quantidade) in contador.items():
        detalhes_produto = dict(detalhes_produto)
        detalhes_produto['quantidade'] = quantidade
        resultado.append(detalhes_produto)

    return resultado


async def get_ordem_servico(ordem_servico_id: int):
    ordem_servico = await OrdemServicoORM.find_one(id=ordem_servico_id)

    async def fetch_additional_info(ordem_servico):
        cliente_pj = await CompanyORM.find_one(id=ordem_servico.company_id)
        cliente_fisico = await UserORM.find_one(id=ordem_servico.user_id)
        tabela_de_ligacao = await OrdemServicoProductInvoiceORM.find_many(ordem_servico_id=ordem_servico.id)

        produtos = []
        subtotal = 0

        for ligacao in tabela_de_ligacao:
            produto = await ProductInvoiceORM.find_one(id=ligacao.product_invoice_id)
            if produto:
                subtotal += produto.valor
                produtos.append({
                    "produto_id": ligacao.product_invoice_id,
                    "nome_produto": produto.nome,
                    "categoria": produto.categoria,
                    "nome": produto.nome,
                    "unidade_de_medida": produto.unidade_de_medida,
                    "valor": produto.valor,
                })

        validade = ordem_servico.created_at + timedelta(days=3)
        return {
            "id": ordem_servico.id,
            "company_id": ordem_servico.company_id,
            "user_id": ordem_servico.user_id,
            "status": ordem_servico.status,
            "tipo_cliente": ordem_servico.tipo_cliente,
            "contrato": ordem_servico.contrato,
            "pagamento": ordem_servico.pagamento,
            "stripe_pagamento_id": ordem_servico.stripe_pagamento_id if ordem_servico.stripe_pagamento_id is not None else '',
            "imposto_percentual": ordem_servico.imposto_percentual,
            "desconto_percentual": ordem_servico.desconto_percentual,
            "cliente": cliente_pj.nome_fantasia if cliente_pj else cliente_fisico.name,
            "produtos": produtos,
            "created_at": ordem_servico.created_at,
            "total": subtotal,
            "validade": validade
        }

    # Use asyncio.gather to parallelize database queries
    results = await fetch_additional_info(ordem_servico)

    return results


async def select_gateway(gateway_id, amount, gateway_configuration):
    # stripe.api_key = gateway_configuration['api_key']
    processing_methods = {
        "stripe": process_payment_with_stripe,
        "paypal": process_payment_with_paypal
        # Add other processing methods as needed
    }

    if gateway_id not in processing_methods:
        raise ValueError(
            f"Unsupported processing method for gateway_id: {gateway_id}")

    processing_function = processing_methods[gateway_id]
    result = await processing_function(amount, gateway_configuration)
    # print(result)


async def process_payment_with_stripe(amount, gateway_configuration):
    try:
        # Stripe payment processing logic
        dados_cliente = {
            'name': 'Joao Vitor M do Nascimento',
            'email': 'joaovitormonsores@hotmail.com',
            # Other customer data if necessary
        }
        cliente_id = await criar_cliente_stripe(dados_cliente, gateway_configuration['api_key'])

        # After creating the customer, generate the invoice
        items_da_fatura = [
            {
                'price': amount,  # Replace with the actual price ID from your Stripe dashboard
            }
            # Add more items as needed
        ]
        await gerar_invoice_stripe(cliente_id, items_da_fatura)

        return f"Processing payment with Stripe for {amount}"
    except stripe.error.StripeError as e:
        logger.error(f"Error processing payment with Stripe: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error processing payment")


async def get_produtos_stripe_prices():
    try:
        # Fetch prices from Stripe
        prices_in_stripe = stripe.Price.list()
        # print(prices_in_stripe)
        return prices_in_stripe['data']
    except stripe.error.StripeError as e:
        # Handle Stripe errors here
        print(f"Error fetching prices from Stripe: {e}")


async def get_produtos_stripe_prices2():
    try:
        # Fetch prices from Stripe
        prices_in_stripe = stripe.Product.list()
        # print(prices_in_stripe)
        return prices_in_stripe['data']
    except stripe.error.StripeError as e:
        # Handle Stripe errors here
        print(f"Error fetching prices from Stripe: {e}")


async def gerar_invoice_stripe(id_do_cliente, collection_method='send_invoice', currency='BRL'):
    try:
        # Example order_data structure
        order_data = {
            "total": 3000,
        }

        # Create a payment intent
        intent = stripe.PaymentIntent.create(
            amount=order_data['total'] * 100,  # Amount should be in cents
            currency=currency,
            customer=id_do_cliente,
            payment_method_types=['card'],
        )

        # Assuming `cart` is an object representing the cart in your Python application
        items = {
            "mode": "payment",
            "success_url": "http://localhost:8000/success.php",
            "cancel_url": "http://localhost:8000/cancel.php",
            "line_items": []
        }

        # Fetch products from Stripe
        products_in_stripe = stripe.Price.list()

        # The line `# print(products_in_stripe['data'])` is commented out code that is not being
        # executed. It is a comment used for debugging purposes to print the data returned from the
        # Stripe API call. By printing the `products_in_stripe['data']`, you can see the response data
        # from the Stripe API and inspect the structure and contents of the data.
        # print(products_in_stripe['data'])

        # Uncomment this section if needed
        # prices = []
        # for product in unique_products:
        #     price = stripe.Price.create(
        #         unit_amount=product['unit_amount'],
        #         currency=currency,
        #         product_data={"name": product['name']},
        #     )
        #     prices.append(price)
        # Uncomment this section if using the 'prices' list
        # line_items = []
        # for product in products:
        #     matching_prices = [
        #         price for price in prices if price.product == product['name']]
        #     if matching_prices:
        #         price_id = matching_prices[0].id
        #         line_items.append(
        #             {"price": price_id, "quantity": product["quantity"]})
        #     else:
        #         print(f"Warning: No matching price found for product '{product['name']}'")
        line_items = [
            {
                # Replace with the actual price from Stripe if available
                "price": product["id"],
                "quantity": 1,
            }
            for product in products_in_stripe['data']
        ]
        # Get or create a payment link for the invoice
        payment_link = stripe.PaymentLink.create(
            line_items=line_items,
            # invoice_creation={"enabled": True},
        )

        print(payment_link)
    except stripe.error.StripeError as e:
        # Handle Stripe errors, raise an exception, or log the error
        print(f"Error creating invoice: {e}")
        raise


async def process_payment_with_paypal(amount, gateway_configuration):
    # PayPal payment processing logic
    return f"Processing payment with PayPal for {amount}"


async def criar_cliente_stripe(dados_cliente, chave_secreta_stripe):
    url_endpoint = 'https://api.stripe.com/v1/customers'
    stripe.api_key = chave_secreta_stripe
    headers = {
        'Authorization': f'Bearer {chave_secreta_stripe}',
    }

    async with httpx.AsyncClient() as client:
        # Check if the customer with the given email already exists
        existing_customer_id = await obter_id_do_cliente(dados_cliente['email'])

        if existing_customer_id:
            return existing_customer_id

        # If the customer doesn't exist, create a new one
        response = await client.post(url_endpoint, data=dados_cliente, headers=headers)
        if response.status_code == 200:
            # Customer created successfully
            cliente_id = response.json()['id']
            return f'Customer created successfully. Customer ID: {cliente_id}'
        else:
            # Something went wrong
            return f'Error creating customer. Response code: {response.status_code}, Message: {response.text()}'


async def obter_id_do_cliente(email_do_cliente):
    try:
        # Verificar se o cliente já existe com base no e-mail
        cliente_existente = stripe.Customer.list(
            email=email_do_cliente, limit=1)

        if cliente_existente.data:
            # Se o cliente já existe, retornar o ID do primeiro cliente encontrado
            return cliente_existente.data[0].id
        else:
            # Se o cliente não existe, criar um novo cliente e retornar o ID
            novo_cliente = stripe.Customer.create(email=email_do_cliente)
            return novo_cliente.id

    except stripe.error.StripeError as e:
        # Lidar com erros do Stripe, se necessário
        print(f"Erro ao obter ID do cliente: {e}")
        return None


@router.post('/processar-pagamento', status_code=200)
async def process_payment(amount: int, user: dict = Depends(has_authenticated)):
    try:
        payment_settings = await PaymentSettingsORM.find_many()
        payment_setting = payment_settings[0]
        gateway_id = payment_setting.gateway_id
        gateway_configuration = payment_setting.gateway_configuration

        await select_gateway(gateway_id, amount, gateway_configuration)

        return {"gateway_configuration": gateway_configuration}
    except Exception as e:
        logger.error(f"Error processing payment: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error processing payment")


@router.get('/buscar-planos', status_code=200)
async def buscar_planos(amount, user: dict = Depends(has_authenticated)):
    try:
        # Obter as configurações de pagamento
        payment_settings = await PaymentSettingsORM.find_many()
        payment_setting = payment_settings[0]
        gateway_id = payment_setting.gateway_id
        gateway_configuration = payment_setting.gateway_configuration

        # Selecionar gateway
        await select_gateway(gateway_id, amount, gateway_configuration)

        # Lista de planos
        planos = [
            {
                'nome': 'Free',
                'preco': 0,
                'espaco': 2,
                'moeda': 'BRL',
                'intervalo': 'month',
                'intervalo_contagem': 1,
                'descricao': 'Plano gratuito',
            },
            {
                'nome': 'Startup',
                'preco': 39900,
                'espaco': 10,
                'moeda': 'BRL',
                'intervalo': 'month',
                'intervalo_contagem': 1,
                'descricao': 'Plano Startup',
            },
            {
                'nome': 'University',
                'preco': 59900,
                'espaco': 50,
                'moeda': 'BRL',
                'intervalo': 'month',
                'intervalo_contagem': 1,
                'descricao': 'Plano University',
            },
            {
                'nome': 'Business',
                'preco': 125000,
                'espaco': 100,
                'moeda': 'BRL',
                'intervalo': 'month',
                'intervalo_contagem': 1,
                'descricao': 'Plano Business',
            },
        ]

        # Criar planos no Stripe
        for plano in planos:
            stripe.Plan.create(
                amount=plano['preco'],
                currency=plano['moeda'],
                interval=plano['intervalo'],
                interval_count=plano['intervalo_contagem'],
                product={
                    'name': plano['nome'],
                    'type': 'service',
                    'statement_descriptor': plano['descricao'],
                },
            )

        # Retornar informações sobre os planos (ou algo mais que você queira retornar)
        return {"message": "Planos criados com sucesso."}

    except Exception as e:
        logger.error(f"Erro ao processar pagamento: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao processar pagamento"
        )


@router.post('/status-pagamento', status_code=200)
async def receber_status_pagamento(webhook_data: Dict[str, Any]):
    invoiceitem_object = webhook_data['data']['object']
    invoice_id = invoiceitem_object['id']

    print(f"ID da fatura: {invoice_id}")

    # Obter configurações de pagamento
    payment_settings = await PaymentSettingsORM.find_many()
    payment_setting = payment_settings[0]
    gateway_configuration = payment_setting.gateway_configuration
    stripe.api_key = gateway_configuration['api_key']

    try:
        # Obter dados da fatura do Stripe
        fatura = stripe.Invoice.retrieve(invoice_id)
        print(f"Status: {fatura.status}")
        print(f"Total: {fatura.amount_due} {fatura.currency}")

        # Obter ordens de serviço associadas à fatura do Stripe
        ordem_servico = await OrdemServicoORM.find_one(stripe_pagamento_id=invoice_id)
        await OrdemServicoORM.update(id=ordem_servico.id, status="Pago", pagamento="Pago") if fatura.status == 'paid' else None
        print(ordem_servico)
        # Aqui você pode adicionar lógica para verificar se a ordem de serviço foi paga
        # usando o status da fatura do Stripe e atualizar o estado da ordem de serviço no banco de dados.

        return {"message": "Status do pagamento recebido com sucesso."}

    except stripe.error.StripeError as e:
        logger.error(f"Erro ao processar status do pagamento do Stripe: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar status do pagamento do Stripe: {e}"
        )


@router.get('/buscar_fatura_por_id', status_code=200)
async def buscar_fatura_por_id(invoice_id):
    try:
        # Assuming `PaymentSettingsORM` is an asynchronous database model
        payment_settings = await PaymentSettingsORM.find_many()

        # Ensure that at least one payment setting is available before proceeding
        if not payment_settings:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Configurações de pagamento não encontradas"
            )

        payment_setting = payment_settings[0]
        gateway_id = payment_setting.gateway_id
        gateway_configuration = payment_setting.gateway_configuration

        # Set the Stripe API key
        stripe.api_key = gateway_configuration['api_key']

        # Retrieve invoice information from Stripe
        fatura = stripe.Invoice.retrieve(invoice_id)

        # Perform actions with invoice data
        print(f"Status: {fatura.status}")
        print(f"Total: {fatura.amount_due} {fatura.currency}")

        # Add logic here to process webhook data and update the payment status in your system
        # For example, check the payment status and update the order status in the database

        # Return the invoice data as a response
        return {"fatura": fatura}

    except stripe.error.StripeError as se:
        logger.error(f"Erro no Stripe: {se}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro no Stripe: {se}"
        )

    except Exception as e:
        logger.error(f"Erro ao processar status do pagamento: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar status do pagamento: {e}"
        )


@router.post('/criar_fatura', status_code=201)
async def criar_fatura(email_do_cliente: str, ordem_servico_id: int, currency: str = "brl"):
    try:
        # Assuming `PaymentSettingsORM` is an asynchronous database model
        print("Obtendo configurações de pagamento...")
        payment_settings = await PaymentSettingsORM.find_many()

        # Ensure that at least one payment setting is available before proceeding
        if not payment_settings:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Configurações de pagamento não encontradas"
            )

        payment_setting = payment_settings[0]
        gateway_id = payment_setting.gateway_id
        gateway_configuration = payment_setting.gateway_configuration

        # Set the Stripe API key
        stripe.api_key = gateway_configuration['api_key']
        customer_id = await obter_id_do_cliente(email_do_cliente)

        print(f"Configurações de pagamento obtidas. ID do cliente: {
              customer_id}")

        # Create an invoice
        ordem_servico = await get_ordem_servico(ordem_servico_id)
        # Logic to count and detail products
        quantidades = defaultdict(int)
        produtos_unicos = []
        lista_produtos = contar_e_detalhar_produtos(ordem_servico['produtos'])

        if ordem_servico['stripe_pagamento_id'] is not None and ordem_servico['stripe_pagamento_id'] != "":
            # A ordem de serviço já tem um ID de pagamento.
            print("Ordem de serviço já possui ID de pagamento.")
            return {"Erro": "Fatura já existente seu id é : " + ordem_servico['stripe_pagamento_id']}

        else:
            print("Criando nova fatura...")
            new_invoice = stripe.Invoice.create(
                customer=customer_id,
                payment_settings={"payment_method_types": ['boleto', 'card']},
                auto_advance=True
            )

            for item in lista_produtos:
                try:
                    print(f"Criando item de fatura para {
                          item['nome_produto']}...")
                    price = stripe.Price.create(
                        unit_amount=int(item['valor'] * 100),
                        currency=currency,
                        product_data={"name": item['nome_produto']},
                    )
                    invoice_item = stripe.InvoiceItem.create(
                        currency=currency,
                        price=price.id,
                        invoice=new_invoice.id,
                        customer=customer_id,
                        quantity=item['quantidade']
                    )
                    print(f"Item de fatura criado para {
                          item['nome_produto']}.")
                    # Handle successful invoice item creation here
                except Exception as e:
                    print(f"Erro ao criar item de fatura para {
                          item['nome_produto']}: {e}")
                    # Handle errors here (e.g., logging, retrying, continuing)

            # Finalize the invoice (automatically charged if auto_advance is True)
            stripe.Invoice.modify(new_invoice.id)
            stripe.Invoice.finalize_invoice(new_invoice.id)

            if ordem_servico['stripe_pagamento_id'] is not None and ordem_servico['stripe_pagamento_id'] != "":
                # A ordem de serviço já tem um ID de pagamento.
                print("Ordem de serviço já possui ID de pagamento.")
                return {"Você já iniciou um pagamento para essa ordem de serviço. Seu ID é": ordem_servico['stripe_pagamento_id']}

            else:
                print("Atualizando ID de pagamento na ordem de serviço...")
                await OrdemServicoORM.update(id=ordem_servico_id, stripe_pagamento_id=new_invoice.id)
                print(f"ID de pagamento atualizado na ordem de serviço. Nova fatura criada: {
                      new_invoice.id}")
                # A ordem de serviço não tem um ID de pagamento.
                return {"nova_fatura": new_invoice.id}

    except stripe.error.StripeError as se:
        print(f"Erro ao criar fatura no Stripe: {se.user_message}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar fatura no Stripe: {se.user_message}"
        )
