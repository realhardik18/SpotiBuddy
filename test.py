e = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
final = []
for i in range(0, len(e)+1, 4):
    final.append(e[i-4: i])
print(final[1:])
