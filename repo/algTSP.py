class AlgTSP:

    def __init__(self, pMatrizDist):
        self.caminho = []
        self.matrizDist = pMatrizDist
        self.vertices = len(pMatrizDist)

    def inserirNoMeio(self,v1,v2, posV):
        #Recebe dois vertices e tenta inserir entre eles um outro vertice que incurta a distancia entre os vertices v1 e v2
        
        inseriuNovo = False
        
        melhorSolucao = self.matrizDist[v1][v2]
   
        vAdicionado = -1

        for v in range(self.vertices):
            
            if v not in self.caminho:
                dist1 = self.matrizDist[v1][v]

                dist2 = self.matrizDist[v2][v]


                if (dist1 + dist2)/2 < melhorSolucao:
                    vAdicionado = v
                    melhorSolucao = (dist1 + dist2)/2

        if vAdicionado != -1:
            inseriuNovo = True
            self.caminho.insert(posV,vAdicionado)

        return inseriuNovo

    def gerarCaminho(self):


        self.caminho.append(0)
        inicio = 0

        posConsolidado = 0
        #while( len(self.caminho) < self.vertices ):

        #achouDistante = False
        #while not achouDistante:
        vDist = max(self.matrizDist[inicio], key=self.matrizDist[inicio].get)
                #if vDist in self.caminho:
                #    del self.matrizDist[inicio][vDist]
                #else:
                #    achouDistante = True

        self.caminho.append(vDist)
        
        consegueInserir = True
        while consegueInserir:
            consegueInserir = False

            i = posConsolidado
            
            while i < (len(self.caminho) - 1) :
                v1 = self.caminho[i]
                v2 = self.caminho[i + 1]

                inseriu = self.inserirNoMeio(v1,v2,i + 1)

                if not consegueInserir and inseriu:
                    consegueInserir = inseriu
                    i = -1
                    

                i+= 1

            #inicio = self.caminho[-1]
            #posConsolidado = len(self.caminho) - 1
        self.caminho.append(0)
        return self.caminho













