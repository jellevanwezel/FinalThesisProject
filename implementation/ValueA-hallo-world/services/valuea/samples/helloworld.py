import valuea_framework.broker.Service
import numpy as np
import scipy
import scipy.stats


class Service(valuea_framework.broker.Service.BaseService):
    def __init__(self, *args, **kwargs):
        super(Service, self).__init__(*args, **kwargs)


    def execute(self):
        params = self.get_message()
        k = params['k']
        x = params['x']
        dataSetName = params['dataset']
        dataLocation = "data/" + dataSetName + ".csv"
        data =  np.loadtxt(open(dataLocation, "rb"), delimiter=",")
        labels = data[:,0]
        data = np.delete(data, np.s_[0:1], axis=1)
        label = self.knn(k,x,data,labels)
        return {'message': label}


    def knn(self,k,x,data,labels):
        xRep = np.tile(x,(data.shape[0],1))
        distances = np.sqrt(np.sum((np.square(xRep - data)),axis=1)) #euclidean dist
        labDist = np.column_stack((labels, distances))
        labDist = self.sortMatrix(labDist,1)
        label = int(scipy.stats.mode(labDist[0:k,0])[0])
        return label

    def sortMatrix(self, m,column):
        temp = m.view(np.ndarray)
        np.lexsort((temp[:, column],))
        return temp[np.lexsort((temp[:, column], ))]

