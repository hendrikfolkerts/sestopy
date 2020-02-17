def fun(pathToRoot):
        cura = pathToRoot["_a"]
        #the return value of pathToRoot["_a"] is a string
        if cura == "1":
            #print(2)
            return 2
        else:
            #print(4)
            return 4

#test the function -> uncomment the print(... command in lines 5 and 8 as well
#fun({"_a": "1"})
