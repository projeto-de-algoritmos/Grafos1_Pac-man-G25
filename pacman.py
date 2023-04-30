import pygame
from mapa import mapa
from collections import deque
import sys

# Define as cores
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
VERMELHO = (255, 0, 0)
BRANCO = (255, 255, 255)

# Carrega a imagem do Pac-Man
pacman_img = pygame.image.load("packman_icon.png")
tamanho = (20, 20)
imagem_redimensionada = pygame.transform.scale(pacman_img, tamanho)

# Carrega a imagem do fantasmas
fantasma1_img = pygame.image.load("fantasma1.png")
tamanho = (24, 24)
imagem_redimensionada_fantasma = pygame.transform.scale(fantasma1_img, tamanho)

# Define os ticks
ticks=0
# Define o temporizador
temporizador = pygame.time.Clock()
tempo_segundo = 0  # Inicializa o contador do tempo em 0
contador_tempo = 0

# Define o tamanho da janela
tamanho = (540, 540)
 
direcao_pacman = "direita"

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
        tela.blit(imagem_redimensionada_fantasma, [y*self.elemento_size+self.elemento_size//30, x*self.elemento_size+self.elemento_size//30])

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

    def atualizar_posicao_pacman(self,pacman_posicao, direcao_pacman):
        i, j = pacman_posicao
        if direcao_pacman == "direita":
            j += 1
        elif direcao_pacman == "esquerda":
            j -= 1
        elif direcao_pacman == "cima":
            i -= 1
        elif direcao_pacman == "baixo":
            i += 1
        if (i, j) in grafo:
            posicao_atual=i,j
            for fantasma in [fantasma1, fantasma2]:
                if (i,j) not in self.visitados:
                    self.visitados.add(posicao_atual)
                    self.pontos += 1

                if fantasma.posicao == (i, j):
                    return
            pacman.set_posicao((i, j))

    def desenhar(self):
        x, y = self.posicao
        # Desenha o Pac-Man
        tela.blit(imagem_redimensionada, [y*self.elemento_size+self.elemento_size//30, x*self.elemento_size+self.elemento_size//30])
    
    def colide_com_fantasma(self, fantasma):
        if self.posicao == fantasma.posicao:
            # Se o pacman colidiu com um fantasma, mata o pacman
            self.morrer()
    
    def morrer(self):
        # Adicione o código para reiniciar o jogo ou para mostrar uma mensagem de "game over"
        font = pygame.font.Font(None, 72)
        text = font.render("Game Over", 1, BRANCO)
        tela.blit(text, (540 / 2 - text.get_width() / 2, 540 / 2 - text.get_height() / 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        #running = False
        sys.exit()

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
def desenha_mapa(mapa, tamanho_elemento, pacman):
    for i, linha in enumerate(mapa):
        for j, coluna in enumerate(linha):
            if coluna == "#":
                pygame.draw.rect(tela, AZUL, [j*tamanho_elemento, i*tamanho_elemento, tamanho_elemento, tamanho_elemento])
            elif (i, j) in grafo:
                if (i, j) not in pacman.visitados:
                    pygame.draw.circle(tela, BRANCO, [j*tamanho_elemento+tamanho_elemento//2, i*tamanho_elemento+tamanho_elemento//2], 2)
                else:
                    # Apaga a bolinha branca
                    pygame.draw.rect(tela, PRETO, [j*tamanho_elemento, i*tamanho_elemento, tamanho_elemento, tamanho_elemento])

# Cria o Pac-Man
pacman = Pacman(25, 13, 20)      

# Cria os fantasmas
fantasma1 = Fantasma(10, 12, 20)
fantasma2 = Fantasma(10, 14, 20)
fantasma3 = Fantasma(10, 13, 20)
                
# Loop principal do jogo
checar = False

i=0

while not checar:
    if pacman.pontos==274:
        # Adicione o código para reiniciar o jogo ou para mostrar uma mensagem de "game over"
        font = pygame.font.Font(None, 72)
        text = font.render("You Win", 1, BRANCO)
        tela.blit(text, (540 / 2 - text.get_width() / 2, 540 / 2 - text.get_height() / 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        #running = False
        sys.exit()

    #Verifica se há colisão do pacman com o fantasma
    pacman.colide_com_fantasma(fantasma1)
    pacman.colide_com_fantasma(fantasma2)
    pacman.colide_com_fantasma(fantasma3)
    # Atualiza o temporizados
    tempo_millisegundos = temporizador.tick(60)
    tempo_segundo += tempo_millisegundos / 70.0

    # Move o fantasma a cada segundo
    if tempo_segundo > 1:
        ticks=ticks+1
        #print(ticks)
        fantasma1.atualizar_posicao(pacman.posicao)
        tempo_segundo -= 1

        if ticks >20:
            fantasma2.atualizar_posicao(pacman.posicao)
            tempo_segundo -= 1
        if ticks >40:
            fantasma3.atualizar_posicao(pacman.posicao)
            tempo_segundo -= 1
            
        # Atualiza a posição do Pac-Man
    if ticks % 1 == 0:
        if i == 10:
            pacman.atualizar_posicao_pacman(pacman.posicao, direcao_pacman)
            i=0

    # Eventos do Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            checar = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direcao_pacman = "direita"
            elif event.key == pygame.K_LEFT:
                direcao_pacman = "esquerda"
            elif event.key == pygame.K_UP:
                direcao_pacman = "cima"
            elif event.key == pygame.K_DOWN:
                direcao_pacman = "baixo"

    #fantasma2.atualizar_posicao(pacman.posicao)
    # Limpa a tela
    tela.fill(PRETO)

    # Desenha o mapa
    desenha_mapa(mapa, 20,pacman)

    # Renderiza o texto da pontuação
    pontuacao_texto = fonte.render(f"Pontuação: {pacman.pontos}", True, VERMELHO)

    # Desenha o texto da pontuação na tela
    tela.blit(pontuacao_texto, (10, 2))

    # Desenha o Pac-Man
    pacman.desenhar()
    # Desenha os fantasmas
    fantasma1.desenhar()
    fantasma2.desenhar()
    fantasma3.desenhar()
    
    # Atualiza a tela
    pygame.display.update()
    
    i += 1

# Encerra o Pygame
pygame.quit()