import arcpy, os

# ===== Variables =====

folderPath = r"\\doe-file\gesb\Project_Geology\Projects-SWP\Santa Ana Division\Perris Dam"          # update as needed

# ===== Functions =====

def createNewFile():
    newFile = open("MXD_Source_List.csv", "w")
    newFile.write("Map Document, MXD Path, DataFrame Name, DataFrame Description, Layer name, Layer Datasource\n")
    newFile.close()

def crawlMXDS(folderPath):
    newFile = open("MXD_Source_List.csv", "a")
    for root, dirs, files in os.walk(folderPath):
        for f in files:
            if f.lower().endswith(".mxd"):
                print(f) # used for debugging
                try:
                    mxdName = os.path.splitext(f)[0]
                    mxdPath = os.path.join(root, f)
                    mxd = arcpy.mapping.MapDocument(mxdPath)
                    dataframes = arcpy.mapping.ListDataFrames(mxd)
                    for df in dataframes:
                        dfDesc = df.description if df.description != "" else "None"
                        layers = arcpy.mapping.ListLayers(mxd, "", df)  
                        for lyr in layers:
                            # checks for specific unicode characters in layer names
                            if u'\xb0' not in lyr.name: # unicode for degree symbol
                                lyrName = lyr.name
                                lyrDatasource = lyr.dataSource if lyr.supports("dataSource") else "N/A"
                                seq = "%s, %s, %s, %s, %s, %s\n" % (mxdName, mxdPath, df.name, dfDesc, lyrName, lyrDatasource)
                                newFile.write(seq)
                            else:
                                lyrName = "N/A"
                                lyrDatasource = lyr.dataSource if lyr.supports("dataSource") else "N/A"
                                seq = "%s, %s, %s, %s, %s, %s\n" % (mxdName, mxdPath, df.name, dfDesc, lyrName, lyrDatasource)
                                newFile.write(seq)
                    del mxd        
                except Exception as err:
                    print(err)
    newFile.close()
    
# ===== Call Functions =====

createNewFile()
crawlMXDS(folderPath)


