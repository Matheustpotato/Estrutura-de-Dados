# -*- coding: utf-8 -*-
from random import choice
from jogador import Jogador
from tabuleiro import Tabuleiro

class JogadorIA(Jogador):
    def __init__(self, tabuleiro: Tabuleiro, tipo: int):
        super().__init__(tabuleiro, tipo)

    def getJogada(self) -> (int, int):
        board = self.matriz
        marcador = self.tipo
        # qual o oponente
        oponente = Tabuleiro.JOGADOR_X if marcador == Tabuleiro.JOGADOR_0 else Tabuleiro.JOGADOR_0

        # checa vitória 
        def win(player):
            # Linhas e colunas
            for i in range(3):
                if board[i][0] == board[i][1] == board[i][2] == player:
                    return True
                if board[0][i] == board[1][i] == board[2][i] == player:
                    return True
            # Diagonais
            if board[0][0] == board[1][1] == board[2][2] == player:
                return True
            if board[0][2] == board[1][1] == board[2][0] == player:
                return True
            return False

        # Lista de posições vazias
        vazio = []
        for l in range(3):
            for c in range(3):
                if board[l][c] == Tabuleiro.DESCONHECIDO:
                    vazio.append((l, c))

        # R1: ganhar ou bloquear
        # tentar ganhar
        for (l, c) in vazio:
            board[l][c] = marcador
            if win(marcador):
                board[l][c] = Tabuleiro.DESCONHECIDO
                return (l, c)
            board[l][c] = Tabuleiro.DESCONHECIDO
        # bloquear o oponente
        for (l, c) in vazio:
            board[l][c] = oponente
            if win(oponente):
                board[l][c] = Tabuleiro.DESCONHECIDO
                return (l, c)
            board[l][c] = Tabuleiro.DESCONHECIDO

        # R2: criar 2 sequencias
        for (l, c) in vazio:
            count = 0
            board[l][c] = marcador
            for (l2, c2) in vazio:
                if board[l2][c2] == Tabuleiro.DESCONHECIDO:
                    board[l2][c2] = marcador
                    if win(marcador):
                        count += 1
                    board[l2][c2] = Tabuleiro.DESCONHECIDO
            board[l][c] = Tabuleiro.DESCONHECIDO
            if count >= 2:
                return (l, c)

        # R3: marcar centro
        if board[1][1] == Tabuleiro.DESCONHECIDO:
            return (1, 1)

        # R4: canto oposto
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        for (l, c) in corners:
            if board[l][c] == oponente:
                opp_l, opp_c = 2 - l, 2 - c
                if board[opp_l][opp_c] == Tabuleiro.DESCONHECIDO:
                    return (opp_l, opp_c)

        # R5: qualquer canto vazio
        for (l, c) in corners:
            if board[l][c] == Tabuleiro.DESCONHECIDO:
                return (l, c)

        # R6: qualquer posição vazia restante
        if vazio:
            return choice(vazio)

        return None
