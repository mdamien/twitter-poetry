lines = open('raw.txt')
lines = [l.strip() for l in lines]
lines = [l for l in lines if len(l) > 10] 
lines = [l for l in lines if l.upper() != l]
with open('data','w') as out:
    for line in lines:
        out.write(line+'\n')
