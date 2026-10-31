X = [1.5, 2.3, 3.7, 4.1, 5.6, 6.8, 7.9, 8.4, 9.2, 10.2]
c = 127 / max(abs(x) for x in X)          # the scale: 127 over the largest magnitude
q = [round(x * c) for x in X]              # what is stored: one int8 per value
back = [v / c for v in q]                  # dequantized
print("c =", round(c, 4))
print("int8:", q)
print("back:", [round(b, 3) for b in back])
print("max error:", round(max(abs(a - b) for a, b in zip(X, back)), 4))
