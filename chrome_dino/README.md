feito com python 3.10
pip install -r requirements.txt

Lógica do algoritmo :

1: começo do jogo \ inicia-se o algoritmo
3: a cada iteração do algoritmo, mediante o cenário em que se encontra o personagem, o modelo deve retornar se o dino deve ou não pular
4: cada decisão é guardada em uma base de dados, com suas circunstâncias (distancia dos obstáculos e se foi bem suscedido)
5: se o personagem falhar, o modelo é re-treinado dom a base de dados adquirida
6: voltar ao passo 1
