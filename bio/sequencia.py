# Funções de manipulação de sequências de DNA.
#
# Nossa "mini BioPython"! Aqui cada função recebe uma sequência como uma
# STRING (ex: "ATCG") e devolve um resultado (outra string, um número, etc.).
#
# IMPORTANTE: implemente cada função abaixo. Apague o
# "raise NotImplementedError(...)" quando for resolver.

# Você vai precisar destas constantes
from bio.constantes import DNA_PARA_AMINOACIDO, DNA_STOP_CODONS, CONVERSOR_DE_BASE


def complementar(sequencia):
    resultado = ""
    for base in sequencia:
        resultado += CONVERSOR_DE_BASE[base]
    return resultado


def complementar_reversa(sequencia):
        resultado = ""
        for base in sequencia:
            resultado = CONVERSOR_DE_BASE[base] + resultado
        return resultado


def transcrever(sequencia):
    return sequencia.replace("T", "U")

    
def calcular_percentual(sequencia, bases):
    contador = 0
    for base in sequencia:
        if base in bases:
            contador += 1
    return contador / len(sequencia) 

    
def calcular_percentual_gc(sequencia):
    return calcular_percentual(sequencia, ["G", "C"])


def contar_bases(sequencia):
    contagem = {"A": 0, "T": 0, "C": 0, "G": 0}
    for base in sequencia:
        contagem[base] += 1
    return contagem


def encontrar_inicio(sequencia):
    sequencia_inicio = sequencia.find("ATG")
    if sequencia_inicio == -1:
        return ""
    return sequencia[sequencia_inicio:]


def traduzir(sequencia, parar=False):
    proteina = ""
    for i in range(0, len(sequencia) - 2, 3):
        codon = sequencia[i:i + 3]
        if codon in DNA_STOP_CODONS:
            if parar:
                break
            else:
                proteina += "*"
        else:
            proteina += DNA_PARA_AMINOACIDO.get(codon, "X")
    return proteina
    