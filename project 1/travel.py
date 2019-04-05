import math
from heapq import heappush,heappop
from node import Node

class Travel():
    """
    this class define the strategies that we are going to explore the search tree
    """

    def __init__(self, root):
        self.root = root
        self.infi = 999  # maximum possible movement if there is really a solution
        self.base = []  # contains the children of the roots
        self.frontier = []  # current nodes in memory that we want to explore
        self.fa = "Failure"

        for s in root.expand():
            self.base.append([s.f, s])
        
        self.base = self.nodeSort(self.base)

        # expand all the base node before calculating the cost
        for b in self.base:
            b[1].expand()


    def Astar_Q(self) -> Node:
        """
        A* search using the Priority Queue to maintance the frontier
        """

        # frontier list
        front = []
        # a dictionary to store seen states, if there is a duplication, only 
        # the one with better g will be kept
        visited = {}
        # Only for debuging purpose, to see how many nodes are pruned
        removed = 0
        explored = 0

        for b in self.base:
            heappush(front, b[1])
            visited[tuple(sorted(b[1].state["players"]))] = b[1]
        
        while True:
            #print(len(front))
            currentNode = heappop(front)
            
            if currentNode.goal_test():
                print("# total removed duplicate nodes =",removed)
                print("# current PQ size =", len(front))
                print("# explored node =", explored)
                return currentNode
            
            if currentNode.f > self.infi:
                return None
            
            successors = currentNode.expand()
            explored += 1

            for s in successors:
                state = tuple(sorted(s.state["players"]))
                if state in visited:
                    # only record better node
                    if visited[state].g > s.g:
                        heappush(front, s)
                        visited[state] = s
                    else:
                        # discard the worse one to reduce space and 
                        # time complexity
                        removed += 1
                else:
                    heappush(front, s)
                    visited[state] = s

    # Below, are some search algorithms that I also discoved but not used in this project
    #####################################################################################

    def RBFS(self, node:Node, flimit:float) -> Node:
        """
        main part of RBFS search

        - `node` current node that will be explored

        - `flimit` heuristic limitation for search

        """
        successors = node.successors

        # there is no path for base node
        if len(successors) == 0:
            return self.fa, self.infi

        for s in successors:
            self.frontier.append((s.f, s))

        while True:
            self.frontier = self.nodeSort(self.frontier)

            # no way towards the goal state through this offspring
            if len(self.frontier) == 0:
                return self.fa, self.infi

            currentNode = self.frontier[0][1]
            # remove the current node from the frontier
            self.frontier = self.frontier[1:]

            # already find the goal
            if currentNode.goal_test():
                return currentNode, currentNode.f
            
            if (currentNode.f <= flimit):
                successors = currentNode.expand()

                # NOTICE: len(successors) might = 0
                for s in successors:
                    self.frontier.append((s.f, s))
            else:
                return self.fa, currentNode.f


    def findRBFS(self):
        """
        this function is used to maintance the self.base, 
        to decide which base are going to be explored next.
        """
        flimit = self.infi - 1

        while True:

            self.base = self.nodeSort(self.base)
            print([(i[0], i[1].fromLastAction) for i in self.base])

            #[NodeCost, NodeObject]
            best = self.base[0]

            # if best base be assigned a infi cost value
            if best[0] >= flimit:
                return "No path, cheack your search logic"

            # the cost of the second best one
            alternativeCost= self.base[1][0]

            # TODO: we can try to use a hash table to store part of the frontier in order to save times
            # new frontier for switching between different branch
            self.frontier = []
            
            result, cost = self.RBFS(best[1], min(flimit, alternativeCost))

            if result != self.fa:
                return result
            
            # update the flimit for the base node
            self.base[0][0] = cost

    def nodeSort(self, nodes:[Node]) -> [Node]:
        return sorted(nodes, key=lambda x:x[0])