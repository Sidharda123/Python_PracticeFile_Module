My_dict = {'apple': 5, 'banana': 8, 'cherry': 12}
My_dict_list = list(My_dict.items())
n = len(My_dict_list)
index = 0
while index < n:
    key , value  = My_dict_list[index]
    print(f" {key} : {value}")
    index = index+1