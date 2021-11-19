import random
import math

matrixDist = []
qtdVertices = 0

class Cromossomo:

    caminho = []
    distPercorrida = -1

    def calculaDist(self):
        global matrixDist
        global qtdVertices

        #Calcula a distancia percorrida pelo caminho do cromossomo
        if self.distPercorrida == -1:
           
            totalDist = 0.0
            for i in range(qtdVertices - 1):
                #percorre o caminho do inicio ao fim
                pontoUm = self.caminho[i]
                pontoDOis = self.caminho[i + 1]

                dist = matrixDist[pontoUm][pontoDOis]

                totalDist += dist
            
            totalDist += matrixDist[qtdVertices - 1][0] #fecha o ciclo indo do ultimo ponto ao primeiro

            self.distPercorrida = totalDist
            print(self.distPercorrida)
        return self.distPercorrida
        
    def __lt__(self, outro):
        return self.calculaDist() < outro.calculaDist()

    def mutarCromossomo(self):
        global qtdVertices
        geneUm = random.randrange(qtdVertices - 1)
        geneDois = random.randrange(qtdVertices - 1)  
        self.caminho[geneUm],self.caminho[geneDois] = self.caminho[geneDois], self.caminho[geneUm]

class  AG:

    def __init__(self,pQtdVertices, tamanhoPopulacao, matrizDist,rotaBase):
        global matrixDist
        global qtdVertices

        qtdVertices = pQtdVertices
        matrixDist = matrizDist

        self.cromossomos = []
        self.tamPopulacao = tamanhoPopulacao
        self.numTentativas = 0

        i = 0
        mutacoes = qtdVertices // 1000
        print(mutacoes)
        while i < tamanhoPopulacao:
            cromossomo = Cromossomo()
            cromossomo.caminho =  rotaBase

            for j in range(mutacoes):
                cromossomo.mutarCromossomo()

            self.cromossomos.append(cromossomo)
            i += 1

    def selecionarIndividuo(self):
        verticeRandUm = random.randrange(self.tamPopulacao // 2)
        verticeRandDois = random.randrange(self.tamPopulacao // 2, self.tamPopulacao)

        if self.cromossomos[verticeRandUm].calculaDist() < self.cromossomos[verticeRandDois].calculaDist():
            return self.cromossomos[verticeRandUm]
        else:
            return self.cromossomos[verticeRandDois]

    
    def criarGeracao(self, cromossomo1, cromossomo2):
        global qtdVertices
        qtdNovosCromossomos = 20
        novosCromossomos = []
        corte = int(qtdVertices * 0.95)

        i = 0

        while i < qtdNovosCromossomos:
            qtdVerticesAdicionados = 0

            verticesFilho = cromossomo1.caminho[0:corte]
            for x in cromossomo2.caminho:
                if (qtdVerticesAdicionados == (self.tamPopulacao - corte) ):
                    break

                if x not in verticesFilho:
                    verticesFilho.append(x)
                    qtdVerticesAdicionados += 1

            novoCromossomo = Cromossomo()
            novoCromossomo.caminho = verticesFilho
            novoCromossomo.mutarCromossomo()

            novosCromossomos.append(novoCromossomo)

            i += 1

        return novosCromossomos

    def atualizarPopulacao(self, novosCromossomos):
        for c in novosCromossomos:
            self.cromossomos =  sorted(self.cromossomos)
            pior = self.cromossomos[-1]
            melhor = self.cromossomos[0]

            if c.calculaDist() < pior.calculaDist():

                self.cromossomos.pop()
                self.cromossomos.append(c)

                if c.calculaDist() < melhor.calculaDist():
                    self.numTentativas = 0
                else:
                    self.numTentativas += 1
            else:
                self.numTentativas += 1

        return self.numTentativas < 700


    def gerarCaminho(self):
        melhorSolucao = True

        while melhorSolucao:
            cromossoUm = self.selecionarIndividuo()
            cromossoDois = self.selecionarIndividuo()

            novosCromossomos = self.criarGeracao(cromossoUm,cromossoDois)
            melhorSolucao = self.atualizarPopulacao(novosCromossomos)

        self.cromossomos =  sorted(self.cromossomos)

        return self.cromossomos[0].caminho
