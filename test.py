a="".join(["\x00" for i in range(1)])
print(bytes(a,"utf-8"))
print(int(bytes("\xa9i\xd3","utf-8")))