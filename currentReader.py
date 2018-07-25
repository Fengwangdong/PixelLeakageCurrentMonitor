import os

cylinder = ["BpI","BpO","BmI","BmO"]
sector   = ["S1","S2","S3","S4","S5","S6","S7","S8"]
layer    = ["LAY1","LAY2","LAY3","LAY4"]
#disk     = ["D1","D2","D3"]
#rog      = ["ROG1","ROG2","ROG3","ROG4"]
#ring     = ["RNG1","RNG2"]

fileName = "currentsFromDB.txt"
outputFile = "currents.txt"

if(os.path.exists(fileName)):
    fin = open(fileName, "r+")
    lines = fin.readlines()

    fout = open(outputFile,"w")

    for index1 in cylinder:
        for index2 in sector:
            for index3 in layer:

                alias = "PixelBarrel_" + index1 + "_" + index2 + "_" + index3
                hvCurrent = -999.
                anaCurrent = -999.
                digCurrent = -999.

                for l in lines:
                    line = l.split()

                    aliasHV = "null"
                    aliasLV1 = "null"
                    aliasLV2 = "null"

                    if "LAY14/channel002" in line[0]:
                        aliasHV = line[0].replace("LAY14/channel002","LAY1")

                    if "LAY14/channel003" in line[0]:
                      aliasHV = line[0].replace("LAY14/channel003","LAY4")

                    if "LAY23/channel002" in line[0]:
                      aliasHV = line[0].replace("LAY23/channel002","LAY3")

                    if "LAY23/channel003" in line[0]:
                        aliasHV = line[0].replace("LAY23/channel003","LAY2")


                    if "LAY14/channel000" in line[0]:
                        aliasLV1 = line[0].replace("LAY14/channel000","LAY1Dig")
                        aliasLV2 = line[0].replace("LAY14/channel000","LAY4Dig")

                    if "LAY14/channel001" in line[0]:
                        aliasLV1 = line[0].replace("LAY14/channel001","LAY1Ana")
                        aliasLV2 = line[0].replace("LAY14/channel001","LAY4Ana")

                    if "LAY23/channel000" in line[0]:
                        aliasLV1 = line[0].replace("LAY23/channel000","LAY2Dig")
                        aliasLV2 = line[0].replace("LAY23/channel000","LAY3Dig")

                    if "LAY23/channel001" in line[0]:
                        aliasLV1 = line[0].replace("LAY23/channel001","LAY2Ana")
                        aliasLV2 = line[0].replace("LAY23/channel001","LAY3Ana")


                    if aliasHV == alias:
                        hvCurrent = float(line[1])

                    if (alias in aliasLV1) or (alias in aliasLV2):
                        if ("Dig" in aliasLV1) or ("Dig" in aliasLV2):
                            digCurrent = float(line[1])
                        if ("Ana" in aliasLV1) or ("Ana" in aliasLV2):
                            anaCurrent = float(line[1])


                if hvCurrent == -999. or digCurrent == -999. or anaCurrent == -999.:
                    print alias, " has empty content!  HV: ", hvCurrent, "  Dig: ", digCurrent, "  Ana: ", anaCurrent
                    fout.write(alias + "   " + str(hvCurrent) + "   " + str(digCurrent) + "   " + str(anaCurrent) + "\n")

                else:
                    fout.write(alias + "   " + str(hvCurrent) + "   " + str(digCurrent) + "   " + str(anaCurrent) + "\n")


    fin.close()
    fout.close()
