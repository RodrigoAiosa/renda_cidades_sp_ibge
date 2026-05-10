# utils.py
def formatar_numero_brasil(valor):
    """
    Formata número no padrão brasileiro com separador de milhar
    Ex: 11451245 -> "11.451.245"
    """
    if valor is None:
        return "N/A"
    try:
        # Converte para inteiro e formata com separadores
        numero = int(float(valor))
        return f"{numero:,}".replace(",", ".")
    except (ValueError, TypeError):
        return str(valor)

def formatar_moeda_brasil(valor):
    """
    Formata moeda no padrão brasileiro
    Ex: 12345.67 -> "R$ 12.345,67"
    """
    if valor is None:
        return "N/A"
    try:
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return str(valor)
