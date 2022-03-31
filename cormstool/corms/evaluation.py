def topk_matric(k,final_score,r):
  if r in final_score:
      if(list(final_score.keys()).index(r) < k):
          return 1
  return 0

def mrr(final_score,r):
    rank=0
    mr=0
    if r in final_score:
        rank=list(final_score.keys()).index(r)+1
        mr=1/rank
    else: 
        mr=0
    return mr
