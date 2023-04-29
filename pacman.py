import pygame
from mapa import mapa

# Define as cores
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
VERMELHO = (255, 0, 0)
BRANCO = (255, 255, 255)

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

#Define a classe do Fantasma
class Fantasma:
    def __init__(self, x, y, elemento_size):
        self.elemento_size = elemento_size
        self.color = VERMELHO
        self.set_posicao((x, y))

    def set_posicao(self, posicao):
        if posicao in grafo:
            self.posicao = posicao

    def draw(self):
        x, y = self.posicao
        pygame.draw.circle(tela, self.color, [y*self.elemento_size+self.elemento_size//2, x*self.elemento_size+self.elemento_size//2], self.elemento_size//2)

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

    def draw(self):
        x, y = self.posicao
        pygame.draw.circle(tela, self.color, [y*self.elemento_size+self.elemento_size//2, x*self.elemento_size+self.elemento_size//2], self.elemento_size//2)

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

    for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                checar = True

    # Limpa a tela
    tela.fill(PRETO)

    # Desenha o Pac-Man
    pacman.draw()
    # Desenha os fantasmas
    fantasma1.draw()
    fantasma2.draw()
    fantasma3.draw()

    # Desenha o mapa
    desenha_mapa(mapa, 20)
    
    # Atualiza a tela
    pygame.display.update()

# Encerra o Pygame
pygame.quit()