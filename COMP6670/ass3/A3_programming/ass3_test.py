import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal
from mpl_toolkits.mplot3d import Axes3D #This is for 3d scatter plots.
import math
import random
import functools




def initialise_parameters(X, K):
    # YOUR CODE HERE
    dim = np.shape(X)[1]
    mu = []
    sigma = []
    pi = []
    max_X = np.max(X, axis=0)
    min_X = np.min(X, axis=0)
    mu = np.array(np.linspace(min_X, max_X, num=K + 2)[1:-1,:])
    #mu = centers[1:-1, :]
    sigma = np.array([0.5 * np.eye(dim) for i in range(K)])
    #sigma = np.asarray([np.cov(X, rowvar=False)] * K)
    pi = np.array(1.0 / K * np.ones(K))

    return sigma, mu, pi


def E_step(pi, mu, sigma, X):
    # YOUR CODE HERE

    r = np.zeros( [len(X),len(pi)] )
    for i in range(len(pi)):
        r[:,i] = multivariate_normal.pdf(X, mu[i], sigma[i]) * pi[i]
    r =  r/(np.sum(r,axis=1).reshape((-1,1)))

    return r




def M_step(r, X):
    # YOUR CODE HERE
    mu = np.zeros((len(r[0]), len(X[0])))
    sigma = np.zeros((len(r[0]), len(X[0]), len(X[0])))
    for k in range(r.shape[1]):
        mu[k] = np.dot(r[:,k],X) / np.sum(r,axis=0).reshape((-1,1))[k]
        sigma[k] =np.dot( np.transpose(X-mu[k]), r[:,k].reshape((-1,1)) * (X-mu[k])  / np.sum(r,axis=0).reshape((-1,1))[k])
    pi = np.array(np.sum(r,axis=0).reshape((-1,1))/r.shape[0])
    return mu, sigma, pi



def classify(pi, mu, sigma, x):
    # YOUR CODE HERE
    r = E_step(pi,mu,sigma,x)
    k = np.argmax(r,axis=1)
    return k[0]




def EM(X, K, iterations):
    # YOUR CODE HERE
    #global pi, mu, sigma
    sigma, mu, pi = initialise_parameters(X,K)

    for i in range(iterations):
        r = E_step(pi,mu,sigma,X)
        mu,sigma,pi = M_step(r,X)

    return mu, sigma, pi




def allocator(pi, mu, sigma, X, k):
    N = X.shape[0]
    cluster = []
    for ix in range(N):
        prospective_k = classify(pi, mu, sigma, X[ix, :])
        if prospective_k == k:
            cluster.append(X[ix, :])
    return np.asarray(cluster)





#
# X = np.load("./data.npy")
#
# iterations = 30
# K = 3
# mu_1, sigma_1, pi_1 = EM(X[:, :3], K, iterations)
# print('\nSigma: \n', sigma_1)
# print('\nMu: \n', mu_1)
# print('\nPi: \n', pi_1)
#
# def allocator(pi, mu, sigma, X, k):
#     N = X.shape[0]
#     cluster = []
#     for ix in range(N):
#         prospective_k = classify(pi, mu, sigma, X[ix, :])
#         if prospective_k == k:
#             cluster.append(X[ix, :])
#     return np.asarray(cluster)
#
# colours = ['r', 'g', 'b']
# fig = plt.figure(figsize=(16, 10))
# ax = fig.add_subplot(111, projection='3d')
# for k in range(K):
#     cluster = allocator(pi_1, mu_1, sigma_1, X[:, :3], k)
#     ax.scatter(cluster[:,0], cluster[:,1], cluster[:, 2], c=colours[k])
# plt.show()




def grayConversion(image):
    grayValue = 0.33 * image[:, :, 2] + 0.34 * image[:, :, 1] + 0.33 * image[:, :, 0]
    #grayValue = 0.11* image[:, :, 2] +  0.59*image[:, :, 1] + 0.3*image[:, :, 0]

    return grayValue


def image_segmentation(image, k, iterations):
    #global mu,sigma,pi
    #grey_image = grayConversion(image)
    grey_image = np.reshape(image, [image.shape[0]*image.shape[1],3])
    dim1, dim2, _ = image.shape
    result = np.zeros((dim1,dim2))
    mu, sigma, pi = EM(grey_image, k, iterations)
    for i in range(len(image)):
        for j in range(len(image[0])):
            re = classify(pi,mu,sigma,image[i,j])

            result[i,j] = re.astype(int)
    return result.astype(int)



image = plt.imread('mandm.png')
import time
start = time.time()
gmm_labels = image_segmentation(image, 5, 10)

end = time.time()
print(f'It takes {end-start} seconds to segement the image.')
colors = [[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 255], [0, 0, 0]]
segemented_image = np.zeros_like(image, dtype=np.int32)
m, n, _ = segemented_image.shape
for i in range(m):
    for j in range(n):
        segemented_image[i, j] = np.array(colors[gmm_labels[i, j]])
plt.imshow(segemented_image)
plt.show()




