# encoding: utf-8
# myTeam.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from captureAgents import CaptureAgent
import random, time, util
from game import Directions, Actions
import game

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'TestAgent', second = 'DefensivoAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  For the nightly contest, however, your team will be created without
  the --redOpts and --blueOpts command-line arguments to capture.py.
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class TestAgent(CaptureAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on).

    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.
    """

    '''
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py.
    '''
    self.start = gameState.getAgentPosition(self.index)
    CaptureAgent.registerInitialState(self, gameState)

    '''
    Your initialization code goes here, if you need any.
    '''

  def chooseAction(self, gameState):
      # Pega as acoes possiveis
      legalActions = gameState.getLegalActions(self.index)

      # Para cada acao possivel da um VALOR baseado no metodo evaluate
      values = [self.avaliaEstado(gameState, a) for a in legalActions]

      # Descobre o menor valor entre as acoes possiveis
      minValue = min(values)

      # Pega todas as acoes com o valor igual ao menor valor encontrado
      bestActions = [a for a, v in zip(legalActions, values) if v == minValue]

      # Sorteia entre as acoes com menor valor, a acao a ser realizada
      action = random.choice(bestActions)

      # Retorna a acao sorteada
      return action

  def avaliaEstado(self, gameState, acao):

      # Dada a acao muda o estado do jogo
      novoEstadoDoJogo = gameState.generateSuccessor(self.index, acao)

      # Descobre a posicao do agente apos a acao
      myPos = self.getMinhaPosicao(novoEstadoDoJogo)

      # Estado do agente apos a acao
      myState = novoEstadoDoJogo.getAgentState(self.index)

      # Pontos recebe a distancia para a comida mais proxima
      pontos = self.getDistanciaComidaMaisProxima(gameState, myPos)

      # Descobre a distancia ao inimigo mais proximo
      distInimigo = self.getDistanciaInimigoMaisProximo(gameState, myPos)

      # metodo para pegar as comidas especiais
      capsulaMaisProxima = 99999
      capsulas = self.getCapsules(gameState)
      if len(capsulas) > 0:
          listaDistanciasCapsulas = [self.getMazeDistance(myPos, x) for x in capsulas]
          capsulaMaisProxima = min(listaDistanciasCapsulas)

      if capsulaMaisProxima == 0:
          pontos = pontos - 10000
      elif capsulaMaisProxima < 3:
          pontos = pontos - 100
      elif capsulaMaisProxima < 5:
          pontos = pontos - 10


      estadosInimigos = [gameState.getAgentState(i) for i in self.getOpponents(novoEstadoDoJogo)]
      defensores = [d for d in estadosInimigos if not d.isPacman and d.getPosition() != None]
      invasores = [i for i in estadosInimigos if i.isPacman and i.getPosition() != None]
      defensoresAssustados = [a for a in defensores if a.scaredTimer>0 and a.getPosition() != None]
      #defensoresNormais = [n for n in defensores if n.scaredTimer==0 and a.getPosition() != None]
      #print defensoresAssustados


      if invasores:
        # print "Invasores"
        # util.pause()
        if distInimigo == 0:
            pontos = pontos + 100000  # Aumenta 100000 caso o inimigo esteja na mesma posicao
        elif distInimigo < 3:
            pontos = pontos + 100  # Aumenta 100 caso o inimigo esteja bem proximo
        elif distInimigo < 5:
            pontos = pontos + 10  # Aumenta 10 caso o inimigo esteja proximo
      if defensoresAssustados:
        # print "Defensores assustados"
        # util.pause()
        if distInimigo == 0:
          pontos = pontos - 100000  # Diminui 100000 caso o inimigo esteja na mesma posicao
        elif distInimigo < 3:
          pontos = pontos - 100  # Diminui 100 caso o inimigo esteja bem proximo
        elif distInimigo < 5:
          pontos = pontos - 10  # Diminui 10 caso o inimigo esteja proximo


      # Evitar ao maximo ficar parado
      if acao == Directions.STOP:
          pontos = pontos + 100


      comidasRestantes = len(self.getComidas(gameState))

      # Se comeu duas comidas
      if comidasRestantes <= 18:
          distanciaInicio = self.getMazeDistance(myPos, self.start)

      #util.pause()
      #print pontos
      #util.pause()
      return pontos

  def getMinhaPosicao(self, gameState):
      # Retorna a posicao do agente
      return gameState.getAgentPosition(self.index)

  def getInimigos(self, gameState):
      # Retorna estado dos inimigos
      visao = self.getCurrentObservation()
      inimigos = [visao.getAgentPosition(i) for i in self.getOpponents(visao)]
      return inimigos

  # def getInvasores(self, gameState):
  #     inimigos = self.getInimigos(gameState)
  #     invasores = [i for i in inimigos ]

  def getDistanciasInimigos(self, gameState, pos):
      # Retorna as distancias a cada inimigo
      inimigos = self.getInimigos(gameState)
      listaDistanciasInimigos = [self.getMazeDistance(pos, x) for x in inimigos]
      return listaDistanciasInimigos

  def getDistanciaInimigoMaisProximo(self, gameState, pos):
      # Retorna a distancia ao inimigo mais proximo
      return min(self.getDistanciasInimigos(gameState, pos))

  def getPosicaoInimigoMaisProximo(self, gameState, pos):
      # Retorna a posicao ao inimigo mais proximo
      inimigos = self.getInimigos(gameState)
      posInimigoMaisProximo = min(inimigos, key=lambda x: self.getMazeDistance(pos, x))
      return posInimigoMaisProximo

  def getComidas(self, gameState):
      # Retorna os estados das comidas
      comida = self.getFood(gameState)
      estadosComidas = comida.asList()
      return estadosComidas

  def getDistanciasComidas(self, gameState, pos):
      # Retorna as distancias a cada inimigo
      comidas = self.getComidas(gameState)
      listaDistanciasComidas = [self.getMazeDistance(pos, x) for x in comidas]
      return listaDistanciasComidas

  def getDistanciaComidaMaisProxima(self, gameState, pos):
      # Retorna a distancia ao inimigo mais proximo
      return min(self.getDistanciasComidas(gameState, pos))

  def getPosicaoComidaMaisProxima(self, gameState, pos):
      # Retorna a posicao ao inimigo mais proximo
      comidas = self.getComidas(gameState)
      posComidaMaisProxima = min(comidas, key=lambda x: self.getMazeDistance(pos, x))
      return posComidaMaisProxima


class DefensivoAgent(CaptureAgent):
    """
    A Dummy agent to serve as an example of the necessary agent structure.
    You should look at baselineTeam.py for more details about how to
    create an agent as this is the bare minimum.
    """

    def registerInitialState(self, gameState):
        """
        This method handles the initial setup of the
        agent to populate useful fields (such as what team
        we're on).

        A distanceCalculator instance caches the maze distances
        between each pair of positions, so your agents can use:
        self.distancer.getDistance(p1, p2)

        IMPORTANT: This method may run for at most 15 seconds.
        """

        ''' 
        Make sure you do not delete the following line. If you would like to
        use Manhattan distances instead of maze distances in order to save
        on initialization time, please take a look at
        CaptureAgent.registerInitialState in captureAgents.py. 
        '''
        CaptureAgent.registerInitialState(self, gameState)

        ''' 
        Your initialization code goes here, if you need any.
        '''

    def chooseAction(self, gameState):
        # Pega as acoes possiveis
        legalActions = gameState.getLegalActions(self.index)

        # Para cada acao possivel da um VALOR baseado no metodo evaluate
        values = [self.avaliaEstado(gameState, a) for a in legalActions]

        # Descobre o menor valor entre as acoes possiveis
        minValue = min(values)

        # Pega todas as acoes com o valor igual ao menor valor encontrado
        bestActions = [a for a, v in zip(legalActions, values) if v == minValue]

        # Sorteia entre as acoes com menor valor, a acao a ser realizada
        action = random.choice(bestActions)

        # Retorna a acao sorteada
        return action

    def avaliaEstado(self, gameState, acao):
        # Dada a acao muda o estado do jogo
        novoEstadoDoJogo = gameState.generateSuccessor(self.index, acao)

        # Estado do agente apos a acao
        myState = novoEstadoDoJogo.getAgentState(self.index)

        # Descobre a posicao do agente apos a acao
        myPos = novoEstadoDoJogo.getAgentPosition(self.index)

        # Pega todos os inimigos
        inimigos = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
        distanciaInimigos = [self.getMazeDistance(myPos, i.getPosition()) for i in inimigos]
        distanciaInimigoMaisProximo = min(distanciaInimigos)
        pontos = distanciaInimigoMaisProximo
        # Pega os 'invasores' -> inimigos que estao com estado isPacman True e que tem valor em getPosition()
        invasores = [a for a in inimigos if a.isPacman and a.getPosition() != None]

        # Se o agente esta assustado
        if myState.scaredTimer > 0:
            print "Estou assustado"
            util.pause()
            if distanciaInimigoMaisProximo == 0:
                pontos = pontos + 100000  # Aumenta 100000 caso o inimigo esteja na mesma posicao
            elif distanciaInimigoMaisProximo < 3:
                pontos = pontos + 100  # Aumenta 100 caso o inimigo esteja bem proximo
            elif distanciaInimigoMaisProximo < 5:
                pontos = pontos + 10  # Aumenta 10 caso o inimigo esteja proximo



        # Aqui garante que ele nunca vai passar do meio
        if myState.isPacman:
            # Atacando
            pontos = pontos + 99999

        # if len(invasores) > 0:
        #     distanciaInvasores = [self.getMazeDistance(myPos, a.getPosition()) for a in invasores]
        #     distanciaInvasorMaisProximo = min(distanciaInvasores)
        #     pontos = pontos + distanciaInvasorMaisProximo*10

        # Evitar ao maximo ficar parado
        if acao == Directions.STOP:
            pontos = pontos + 100

        # Evitar fazer a ação contrária
        rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
        if acao == rev: pontos = pontos + 10

        return pontos













# Deixa o MaisPerto aqui para testes
class MaisPertoAgent(CaptureAgent):
    """
    A Dummy agent to serve as an example of the necessary agent structure.
    You should look at baselineTeam.py for more details about how to
    create an agent as this is the bare minimum.
    """

    def registerInitialState(self, gameState):
        """
        This method handles the initial setup of the
        agent to populate useful fields (such as what team
        we're on).

        A distanceCalculator instance caches the maze distances
        between each pair of positions, so your agents can use:
        self.distancer.getDistance(p1, p2)

        IMPORTANT: This method may run for at most 15 seconds.
        """

        ''' 
        Make sure you do not delete the following line. If you would like to
        use Manhattan distances instead of maze distances in order to save
        on initialization time, please take a look at
        CaptureAgent.registerInitialState in captureAgents.py. 
        '''
        CaptureAgent.registerInitialState(self, gameState)

        ''' 
        Your initialization code goes here, if you need any.
        '''

    def chooseAction(self, gameState):
        # Pega as acoes possiveis
        legalActions = gameState.getLegalActions(self.index)

        # Para cada acao possivel da um VALOR baseado no metodo evaluate
        values = [self.avaliaEstado(gameState, a) for a in legalActions]

        # Descobre o menor valor entre as acoes possiveis
        minValue = min(values)

        # Pega todas as acoes com o valor igual ao menor valor encontrado
        bestActions = [a for a, v in zip(legalActions, values) if v == minValue]

        # Sorteia entre as acoes com menor valor, a acao a ser realizada
        action = random.choice(bestActions)

        # Retorna a acao sorteada
        return action

    def avaliaEstado(self, gameState, acao):
        # Dada a acao muda o estado do jogo
        novoEstadoDoJogo = gameState.generateSuccessor(self.index, acao)

        # Descobre a posicao do agente apos a acao
        myPos = novoEstadoDoJogo.getAgentPosition(self.index)

        # Pega a lista de comidas do labirinto
        comida = self.getFood(gameState)

        # Transforma a lista de comidas em uma lista de posicoes
        estadosComidas = comida.asList()

        # Descobre a distancia do agente para cada comida
        listaDistanciasComidas = [self.getMazeDistance(myPos, x) for x in estadosComidas]

        # Calcula a menor distancia para uma comida
        distanciaComida = min(listaDistanciasComidas)

        return distanciaComida

