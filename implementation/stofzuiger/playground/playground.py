d = {
    1.345:"test1"
}

d[1.234] = dict()
innerDict = d[1.234]

innerDict[1] = "test"

print d