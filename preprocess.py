from collections import defaultdict

roman_num_lets = set(["I","X", "V", ".", "L"])

def check_roman(word):
    return all(c in roman_num_lets for c in word)
    
def separate_punct(word):
    res = []
    if not word[-1].isalpha() and word[0].isalpha():
        res.append(word[:-1])
        res.append(word[-1])
    else:
        res.append(word)
    return res
        
def clean_lines(lines,lower_case=True, stringify=False):
    res = defaultdict(list)
    title_n = 1
    title = "1"
    for line in lines:
        line = line.strip()
        cur = []
        words = line.split()
        if words:
            if len(words) == 1:
                word = words[0]
                if word.isupper():
                    if check_roman(word):
                        title_n += 1
                        title = str(title_n)
                    else:
                        title = separate_punct(word)[0]
            else:
                for word in words:
                    if lower_case:
                        word = word.lower()
                    cur.extend(separate_punct(word))
                res[title].extend((cur))
    if stringify:
		string_res = {}
		for k in res:
			l = res[k]
			string_res[k] = " ".join(l)
		res = string_res
    return res
        
    