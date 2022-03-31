def commonWords(str1, str2):
    result = "";
    n1 = len(str1)
    n2 = len(str2)
     
    if(n1!=n2):
        return 0
    # Compare str1 and str2
    i = 0
    j = 0
    while i <= n1 - 1 and j <= n2 - 1:
        if (str1[i] != str2[j]):
            break
             
        result += str1[i]
        i += 1
        j += 1
    if(i==n1):
        return 1
    else:
        return 0
    # print(commonWords("prahar","pandya"))
    # print(commonWords("prahar","prahar"))
def LCP(l1,l2):
    string_comparison = 0
    maxlength = max(len(l1),len(l2))
    minlength = min(len(l1),len(l2))
    for i in range(minlength):
        if(commonWords(l1[i],l2[i])==0):
            break
        else:
            string_comparison=string_comparison+1
    return string_comparison/minlength

def LCS(l1,l2):
    string_comparison = 0
    maxlength = max(len(l1),len(l2))
    minlength = min(len(l1),len(l2))
    for i in reversed(range(minlength)):
        if(commonWords(l1[i],l2[i])==0):
            break
        else:
            string_comparison=string_comparison+1
    return string_comparison/minlength

def LCSubseq(l1,l2):
    result = 0
    maxlength = max(len(l1),len(l2))
    minlength = min(len(l1),len(l2))
    for i in range(len(l1)):
        string_comparison = 0
        for j in range(len(l2)):
            if(commonWords(l1[i],l2[j])==1):
                string_comparison=string_comparison+1
        result += string_comparison
#     print(string_comparison)
    return result/maxlength

def LCSubstr(l1,l2):
    result = 0
    maxlength = max(len(l1),len(l2))
    minlength = min(len(l1),len(l2))
    for i in range(len(l1)):
        string_comparison = 0
        for j in range(len(l2)):
            if(j>=i and commonWords(l1[i],l2[j])==1):
                string_comparison=string_comparison+1
        result += string_comparison
#     print(string_comparison)
    return result/maxlength
    
# print(LCP(["prahar","pandya"],["prahar","pandya"]))
# print(LCP(["prahar","pandya"],["prahar","prahar"]))