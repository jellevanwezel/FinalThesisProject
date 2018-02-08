import numpy as np
import scipy
import scipy.stats


class Classify():

    def knn(self,k,x,data,labels):
        xRep = np.tile(x,(data.shape[0],1))
        distances = np.sqrt(np.sum((np.square(xRep - data)),axis=1)) #euclidean dist
        labDist = np.column_stack((labels, distances))
        labDist = self.sortMatrix(labDist,1)
        label = int(scipy.stats.mode(labDist[0:k,0])[0])
        return label

    def sortMatrix(self, m,column):
        temp = m.view(np.ndarray)
        return temp[np.lexsort((temp[:, column], ))]
