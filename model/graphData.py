from model.GM11 import return_data


def getGraphData(city):
    res = {}
    res["title"] = ["二手房预测", "新房预测"]
    oldhouseYear, oldhousePredictYear, oldhouseData, oldhousePredictData = return_data(city, 0)
    newhouseYear, newhousePredictYear, newhouseData, newhousePredictData = return_data(city, 1)
    basicGraph = {}
    basicGraph["graphTitle"] = oldhouseYear
    basicGraph["graphName"] = ["二手房", "新房"]
    basicGraph["graphData"] = [oldhouseData, newhouseData]
    predictGraph = {}
    predictGraph["graphTitle"] = oldhouseYear
    predictGraph["graphName"] = ["二手房", "新房"]
    predictGraph["graphData"] = [oldhousePredictData, newhousePredictData]
    res["data"] = [basicGraph, predictGraph]
    return res

