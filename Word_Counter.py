# cook your dish here

def word_count(sentence, N):
    sentence = sentence.lower()

    lst = list(sentence)
    new_list = []
    for item in lst:
        if(item == " " or ( 97 <= ord(item) <= 122)):
            new_list.append(item)
            
    new_list = "".join(new_list)
    print(new_list)
    words = new_list.split()

    freq = {}

    for word in words:
        freq[word] = freq.get(word, 0) + 1

    result = [(word, count) 
              for word, count in freq.items() 
              if count == N]

    return result

text = "Apple is apple and the apple is not mango and mango is mango"
print(word_count(text,3))