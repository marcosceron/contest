# myTeam.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from captureAgents import CaptureAgent
import random, time, util
from game import Directions
from game import Actions
import game

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'MaisPertoAgent', second = 'MaisPertoAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

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
    #Pega as acoes possiveis
    legalActions=gameState.getLegalActions(self.index)

    #Para cada acao possivel da um VALOR baseado no metodo evaluate
    values = [self.avaliaEstado(gameState, a) for a in legalActions]

    #Descobre o menor valor entre as acoes possiveis
    minValue = min(values)

    #Pega todas as acoes com o valor igual ao menor valor encontrado
    bestActions = [a for a, v in zip(legalActions, values) if v == minValue]

    #Sorteia entre as acoes com menor valor, a acao a ser realizada
    action=random.choice(bestActions)

    #Retorna a acao sorteada
    return action

  def avaliaEstado(self, gameState, acao):
    #Dada a acao muda o estado do jogo
    novoEstadoDoJogo = gameState.generateSuccessor(self.index, acao)

    #Descobre a posicao do agente apos a acao
    myPos=novoEstadoDoJogo.getAgentPosition(self.index)

    #Pega a lista de comidas do labirinto
    comida = self.getFood(gameState)

    #Transforma a lista de comidas em uma lista de posicoes
    estadosComidas=comida.asList()

    #Descobre a distancia do agente para cada comida
    listaDistanciasComidas=[self.getMazeDistance(myPos,x) for x in estadosComidas]

    #Calcula a menor distancia para uma comida
    distanciaComida=min(listaDistanciasComidas)
    
    return distanciaComida
