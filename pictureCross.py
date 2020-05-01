#-*-coding:UTF-8-*-

import sys
sys.path.append("/home/baptistussi/Desktop/PictureCross")
import pcObj

game=pcObj.Game() # Game(False) to disable user feed
#game.N={"rows": [[3,4],[3,2,1,1],[1,2,1],[3,1,1],[5,4],[5],[5],[6],[10],[11],[11],[3,3],[3,2],[3,3],[1,1]],
#"columns":[[0],[6],[2,8],[2,8],[2,8],[10],[8],[6],[3],[3,3],[2,1,4],[1,1,1,5],[3,1,5],[1,1,1],[3]]
#}
game.imprime()

solver=pcObj.Solver(game.dim, game.N)
solver.solve_M()
stat=solver.all_solved

if stat:
    print("Resolvido!")
else:
    print("Falhou!")

game.get_M(solver.M)
game.imprime()
