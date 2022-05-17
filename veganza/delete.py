s = input("enter string with items seprated by ', ' and ranking: ")
s = s.split(', ')
for i in range(len(s)):
    for j in range((i+1)):
        if s[i][-1] < s[j][-1]:
            s[i], s[j] = s[j], s[i]
print(s)