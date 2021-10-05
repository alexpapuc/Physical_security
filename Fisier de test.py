str = ['E1.1-E1.2','BI1','E2-BU2']
target_letter = '-'
lst=[]
for item in str:
    if target_letter in item :
        new_item = item
        index_position = new_item.index(target_letter)
        index_position = int(index_position)
        str_target = item[:index_position]
        lst.append(str_target)
    else:
        lst.append(item)
print(lst)