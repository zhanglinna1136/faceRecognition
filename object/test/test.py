users = {
    'username': 'efermi',
    'first': 'enrico',
    'last': 'fermi',
}
i = 0
# for dict_key in users.keys():
#     if i == 1:
#         print(dict_key)
#     i+=1
# print(list(users.keys())[0])

for i in users.items():
    print(i[0])
print(users.items())
