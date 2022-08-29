



def escribir():
    dict1 = {'Edo': True, 'dis': "arduino"}
    file1 = open("guardado.txt", "w")
    file1.write("%s = %s\n" % ("dict1", dict1))
    file1.close()


def leer():
    f = open('guardado.txt', 'r')
    if f.mode == 'r':
        contents = f.read()

        print(contents)