import os

inputFileName = "rocCurrents.txt"
moduleFileName = "powermap.txt"
moduleOutputName = "moduleCurrents.txt"

if(os.path.exists(inputFileName) and os.path.exists(moduleFileName)):
    fin = open(inputFileName, "r+")
    lines = fin.readlines()

    fModule = open(moduleFileName, "r+")
    moduleList = fModule.readlines()

    fout = open(moduleOutputName, "w")

    for l in lines:
        line = l.split()

        alias = line[0].replace("PixelBarrel","BPix")
        alias = alias.replace("_S","_SEC")
        alias = alias.replace("LAY","LYR")

        for iModule in moduleList:
            module = iModule.split()

            if alias in module[0]:
                moduleCurrent = float(line[2])*16.0
                fout.write(module[0] + " " + str(moduleCurrent) + "\n")


    fout.close()
    fModule.close()
    fin.close()
