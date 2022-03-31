import cormstool.corms.comparison as comparison
import cormstool.corms.normalization as normalization
def measure(df,author,project,new_files):
    reviewer_lcs = dict()
    reviewer_lcp = dict()
    reviewer_lcsubseq = dict()
    reviewer_lcsubstr = dict()
    for i in range(df.shape[0]):
        mxp=0
        mxc=0
        mxq=0
        mxs=0
        for ef in eval(df["File Info"][i]):
            lst = ef.split("/")
            for ef_new in new_files:
                lst_new = ef_new.split("/")
                lcp = comparison.LCP(lst,lst_new)
                if(lcp>mxp):
                    mxp = lcp
                lcs = comparison.LCS(lst,lst_new)
                if(lcs>mxc):
                    mxc = lcs
                lcseq = comparison.LCSubseq(lst,lst_new)
                if(lcseq>mxq):
                    mxq = lcseq
                lcstr = comparison.LCSubstr(lst,lst_new)
                if(lcstr>mxs):
                    mxs = lcstr

        lst = str(df["Author"][i]).split("/")
        lst_new = str(author).split("/")
        lcp = comparison.LCP(lst,lst_new)
        mxp = lcp+mxp
        lcs = comparison.LCS(lst,lst_new)
        mxc = lcs+mxc
        lcseq = comparison.LCSubseq(lst,lst_new)
        mxq = lcseq+mxq
        lcstr = comparison.LCSubstr(lst,lst_new)
        mxs = lcstr+mxs

        lst = df["Project/Subproject"][i].split("/")
        lst_new = project.split("/")
        if(not(len(lst)==1 or len(lst_new)==1)):
          lst = lst[-1].split("/")
          lst_new = lst_new[-1].split("/")
          lcp = comparison.LCP(lst,lst_new)
          mxp = lcp+mxp
          lcs = comparison.LCS(lst,lst_new)
          mxc = lcs+mxc
          lcseq = comparison.LCSubseq(lst,lst_new)
          mxq = lcseq+mxq
          lcstr = comparison.LCSubstr(lst,lst_new)
          mxs = lcstr+mxs

        mxp = round(mxp, 2)
        mxc = round(mxc, 2)
        mxq = round(mxq, 2)
        mxs = round(mxs, 2)

        r = df["Reviewer"][i]
        if r not in reviewer_lcp:
            reviewer_lcp[r]=mxp
        else:
            reviewer_lcp[r]=reviewer_lcp[r]+mxp
        if r not in reviewer_lcs:
            reviewer_lcs[r]=mxc
        else:
            reviewer_lcs[r]=reviewer_lcs[r]+mxc
        if r not in reviewer_lcsubseq:
            reviewer_lcsubseq[r]=mxq
        else:
            reviewer_lcsubseq[r]=reviewer_lcsubseq[r]+mxq
        if r not in reviewer_lcsubstr:
            reviewer_lcsubstr[r]=mxs
        else:
            reviewer_lcsubstr[r]=reviewer_lcsubstr[r]+mxs
    
        i = i+1
    # normalization.normalize_in_place(reviewer_lcp)
    # normalization.normalize_in_place(reviewer_lcs)
    # normalization.normalize_in_place(reviewer_lcsubseq)
    # normalization.normalize_in_place(reviewer_lcsubstr)
    
    final_score = dict()
    # for key in rev_act:
    #     if key in final_score:
    #         final_score[key] = final_score[key] + rev_act[key]
    #     else:
    #         final_score[key] = rev_act[key]
    for key in reviewer_lcp:
        if key in final_score:
            final_score[key] = final_score[key] + reviewer_lcp[key]
        else:
            final_score[key] = reviewer_lcp[key]
    for key in reviewer_lcs:
        if key in final_score:
            final_score[key] = final_score[key] + reviewer_lcs[key]
        else:
            final_score[key] = reviewer_lcs[key]           
    for key in reviewer_lcsubseq:
        if key in final_score:
            final_score[key] = final_score[key] + reviewer_lcsubseq[key]
        else:
            final_score[key] = reviewer_lcsubseq[key]
    for key in reviewer_lcsubstr:
        if key in final_score:
            final_score[key] = final_score[key] + reviewer_lcsubstr[key]
        else:
            final_score[key] = reviewer_lcsubstr[key]

    # normalization.normalize_in_place(final_score)
    final_score = dict(sorted(final_score.items(), key=lambda item: item[1],reverse=True))
    return final_score