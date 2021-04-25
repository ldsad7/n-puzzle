Heuristics:
- Число ходов, требуемых для решения, не меньше, чем число плиток, находящихся не на своих местах.
- Manhattan distance (сопоставляет каждому расположению плиток сумму расстояний от текущей позиции каждой плитки до её целевой позиции)
- Euclidean distance/...
- Linear Conflict (http://academiccommons.columbia.edu/download/fedora_content/download/ac:141290/CONTENT/cucs-219-85.pdf)
- Hamming distance
- 

Begin {Algorithm}\
For each row rj in the state s, one accounts for the conflicts local to that row ic(s,rj) as follows:\
• lc(s,rj) = O •\
• For each tile tj in rj' determine C(tj,rJ\
• 'While there is a non-zero C(tj'rj) value, do\
• Find tic such that there is no C(tj'rj) greater than C(t",r). (As tic is the tile with the most\
conflicts, we choose to move it out of rj)'\
e C(t",rj) = O.\
• For every tile tj which had been in conflict with tic' C(tprj) "" C(tj,rj)-1.\
elc(s,rj)=lc(s,rj)+ 1.\
Check similarly for linear conflicts in each column Cj' computing lc(s, Cj)' Then calculate the estimate\
of the Linear Conflict alone:\
Le(s) = 2[ {lc(s,rl)+ ... +ic(s,rL)}+{ic(s,cl)+···+ic(s,cL)} ]\
Determine, for each tile I j in state s, its Manhattan Distance md(s,tj), and sum these to get the overall\
Manhattan Distance MD(s) =md(s,t1) + ... +md(s,tN)' Calculate the overall Linear Conflict heuristic\
estimate: h'(s) = MD(s) + Le(s).\
End {Algorithm} 
