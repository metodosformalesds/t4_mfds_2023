def calcular_digito_verificador(cuenta):
  """
  Calcula el digito verificador de una cuenta

  Args:
    cuenta: La cuenta CLABE a calcular 

  Returns:
    El digito verificador de la cuenta CLABE
  """
  digitos = cuenta[:-1]

  valor = 0
  for i in range(1, len(digitos) + 1):
    valor = valor + (i * int(digitos[-i]))

  residuo = valor % 11

  if residuo == 0:
    return 0

  if residuo < 10:
    return residuo
  
  return 11 - residuo

# Ejemplo con 16 digitos, sale 7 
cuenta = "1234567812345678"
digito_verificador = calcular_digito_verificador(cuenta)
print(digito_verificador)
