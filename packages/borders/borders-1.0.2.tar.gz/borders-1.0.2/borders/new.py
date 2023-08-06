from borders import frame

output = ["There are only 10 kinds of people in this world: Those who know binary and Those who don't."]
frame(output, max_width=100)


list_1 = [("hello", 1),("world", 2)]
#list_1 = ["hello","world"]

# isinstance("Hello", (float, int, str, list, dict, tuple))

for item in list_1:
    
    if isinstance(item, tuple):
        print(f"{item[0]} Colour = {item[1]}")
    else:
        print(item)



