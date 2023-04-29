import pygame
from mapa import mapa
from collections import deque

# Define as cores
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
VERMELHO = (255, 0, 0)
BRANCO = (255, 255, 255)

# Define os ticks
ticks=0
# Define o temporizador
temporizador = pygame.time.Clock()
tempo_segundo = 0  # Inicializa o contador do tempo em 0

# Define o tamanho da janela
tamanho = (540, 540)
 
# Inicializa o Pygame
pygame.init()
 
# Define o título da janela
pygame.display.set_caption("Pac-Man")

# Cria a janela
tela = pygame.display.set_mode(tamanho)
 
# Define a fonte
fonte = pygame.font.SysFont(None, 25)

# 
def bfs(grafo, origem, destino):
    visitados = set()
    fila = deque([(origem, [])])

    while fila:
        vertice, caminho = fila.popleft()
        if vertice == destino:
            return visitados, caminho
        if vertice in visitados:
            continue
        visitados.add(vertice)
        for vizinho in grafo[vertice]:
            if vizinho not in visitados:
                fila.append((vizinho, caminho + [vizinho]))
    
    return visitados, None

#Define a classe do Fantasma
class Fantasma:
    def __init__(self, x, y, elemento_size):
        self.elemento_size = elemento_size
        self.color = VERMELHO
        self.set_posicao((x, y))

    def set_posicao(self, posicao):
        if posicao in grafo:
            self.posicao = posicao

    def desenhar(self):
        x, y = self.posicao
        pygame.draw.circle(tela, self.color, [y*self.elemento_size+self.elemento_size//2, x*self.elemento_size+self.elemento_size//2], self.elemento_size//2)

    def atualizar_posicao(self, pacman_posicao):
        visitados, caminho_minimo = bfs(grafo, self.posicao, pacman_posicao)
        if caminho_minimo:
            nova_posicao = caminho_minimo[0]
            for fantasma in [fantasma1, fantasma2]:
                if fantasma != self and fantasma.posicao == nova_posicao:
                    return
            self.set_posicao(nova_posicao)

# Define a classe Pacman
class Pacman:
    def __init__(self, x, y, elemento_size):
        self.elemento_size = elemento_size
        self.color = AMARELO
        self.set_posicao((x, y))
        self.pontos = 0
        self.visitados = set()

    def set_posicao(self, posicao):
        if posicao in grafo:
            self.posicao = posicao

    def desenhar(self):
        x, y = self.posicao
        pygame.draw.circle(tela, self.color, [y*self.elemento_size+self.elemento_size//2, x*self.elemento_size+self.elemento_size//2], self.elemento_size//2)

    def mover(self, direcao):
        x, y = self.posicao
        if direcao == "cima":
            proximo_no = (x-1, y)
        elif direcao == "baixo":
            proximo_no = (x+1, y)
        elif direcao == "esquerda":
            proximo_no = (x, y-1)
        elif direcao == "direita":
            proximo_no = (x, y+1)
        if proximo_no in grafo:
            if proximo_no not in self.visitados:
                self.visitados.add(proximo_no)

                self.pontos += 1
            self.posicao = proximo_no

def get_vizinhos(i, j):
    vizinhos = []
    if i > 0 and mapa[i-1][j] != "#":
        vizinhos.append((i-1, j))
    if i < len(mapa)-1 and mapa[i+1][j] != "#":
        vizinhos.append((i+1, j))
    if j > 0 and mapa[i][j-1] != "#":
        vizinhos.append((i, j-1))
    if j < len(mapa[0])-1 and mapa[i][j+1] != "#":
        vizinhos.append((i, j+1))
    return vizinhos

# Cria o grafo
grafo = {}
for i, linha in enumerate(mapa):
    for j, coluna in enumerate(linha):
        if coluna != "#" and coluna != " ":
            vizinhos = get_vizinhos(i, j)
            grafo[(i, j)] = vizinhos

# Define a função para desenhar o mapa
def desenha_mapa(mapa, tamanho_elemento):
    for i, linha in enumerate(mapa):
        for j, coluna in enumerate(linha):
            if coluna == "#":
                pygame.draw.rect(tela, AZUL, [j*tamanho_elemento, i*tamanho_elemento, tamanho_elemento, tamanho_elemento])


# Cria o Pac-Man
pacman = Pacman(25, 13, 20)      

# Cria os fantasmas
fantasma1 = Fantasma(10, 12, 20)
fantasma2 = Fantasma(10, 14, 20)
fantasma3 = Fantasma(10, 13, 20)
                
# Loop principal do jogo
checar = False

while not checar:
    # Atualiza o temporizados
    tempo_millisegundos = temporizador.tick(60)
    tempo_segundo += tempo_millisegundos / 70.0

    # Move o fantasma a cada segundo
    if tempo_segundo > 1:
        ticks=ticks+1
        #print(ticks)
        fantasma1.atualizar_posicao(pacman.posicao)
        tempo_segundo -= 1
#        pacman.colide_com_fantasma(fantasma1)
#        pacman.colide_com_fantasma(fantasma2)
#        pacman.colide_com_fantasma(fantasma3)

        if ticks >20:
            fantasma2.atualizar_posicao(pacman.posicao)
            tempo_segundo -= 1
        if ticks >40:
            fantasma3.atualizar_posicao(pacman.posicao)
            tempo_segundo -= 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            checar = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pacman.mover("cima")  
            elif event.key == pygame.K_DOWN:
                pacman.mover("baixo")
            elif event.key == pygame.K_LEFT:
                pacman.mover("esquerda")
            elif event.key == pygame.K_RIGHT:
                pacman.mover("direita") 

    #fantasma2.atualizar_posicao(pacman.posicao)
    # Limpa a tela
    tela.fill(PRETO)

    # Desenha o Pac-Man
    pacman.desenhar()
    # Desenha os fantasmas
    fantasma1.desenhar()
    fantasma2.desenhar()
    fantasma3.desenhar()

    # Desenha o mapa
    desenha_mapa(mapa, 20)
    
    # Atualiza a tela
    pygame.display.update()

# Encerra o Pygame
pygame.quit()