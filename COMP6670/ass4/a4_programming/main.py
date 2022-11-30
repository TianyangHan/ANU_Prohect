import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D #This is for 3d scatter plots.
import math
import random
import os
import scipy
from matplotlib.pyplot import imread
from PIL import Image
np.random.seed(13579201)

width = 64
height = 128
dimension = (height, width, 3)
images = []
filename = []
for file in os.listdir("./train"):
    if file.endswith(".jpg"):
        im = imread("./train/" + file)
        im = im.flatten() # flatten im into a vector
        images.append(im)
        filename.append(file)
A_pp = np.stack(images).T # build a matrix where each column is a flattened image
# print(A_pp.shape)
# plt.imshow(A_pp[:, 0].reshape(dimension))
# plt.show()


def preprocess(A_pp):
    #YOUR CODE HERE
    A_pp = np.float64(A_pp)
    mu = np.sum(A_pp,axis=1)/len(A_pp[0])
    q = np.zeros_like(A_pp)
    A = np.zeros_like(A_pp)
    for i in range(len(A_pp)):
        q[i] = A_pp[i] - mu[i]
        norm = np.linalg.norm(q[i], ord=np.inf)
        A[i] = q[i] / norm if norm !=0 else q[i]
    norm = np.linalg.norm(q,ord=np.inf,axis=1)
    return A, norm, mu

A, Q_norms, A_means = preprocess(A_pp)
print(A)
print(Q_norms)
print(A_means.shape)


def eigen_ped(A):
    matrix = np.dot(A.T,A) / len(A[0])
    v,d = np.linalg.eig(matrix)
    S = np.cov(A)
    D = np.zeros(len(S))
    for i in range(len(v)):
        D[i] = v[i]
    F = np.dot(A,d)
    for i in range(len(v)):
       F[:,i] = F[:,i] / np.linalg.norm(F[:,i], axis = 0)
    return F,D




# For the purposes of doing this assignment, this code isn't really here. Pretend it's engraved in rock.
F, D = eigen_ped(A)
F_real = np.real(F)
print('Orthogonality Check (should be close to 0): ', F_real[:, 0].T @ F_real[:, 1])
print('Unit Vector Check: ', math.isclose(np.linalg.norm(F_real[:, 0]), 1))
print(F.shape)  # It should be (24576, 199)
print(D.shape)  # It should be (24576)

# The visulisation of an Eigen Pedestrain should **look like** a pedestrain.
print('Visualise an Eigen Pedestrain:')
ep = np.rint((F[:, 0] * Q_norms + A_means).reshape(dimension)).astype(int)
plt.imshow(ep)
plt.show()


def reduce_dimensionality(image_vector, k, F, D, A_means, Q_norms):
    vec = image_vector.copy()
    vec = np.float64(vec)
    vec = (vec-A_means) *(1/Q_norms)
    compressed = F.T @ vec  # 199x1
    for i in range(k,len(compressed)):
        compressed[i]=0
    p = np.sum(D[0:k]) / np.sum(D)
    return compressed,p

# Display Code. Leave it alooooooooooone.
Idx = 0
compressed_image, p = reduce_dimensionality(A_pp[:, Idx], 80, F, D, A_means, Q_norms)
print(compressed_image.shape)  # should be (199,)
print('Variance Captured:', int(p * 100), '%')



def reconstruct_image(compressed_image, F, Q_norms, A_means):
    # YOUR CODE HERE
    # img = np.sum(compressed_image * F, axis=1)
    img = np.zeros(len(F))
    for i in range(len(compressed_image)):
        img+=compressed_image[i]*F[:,i]
    R_c = (img*Q_norms+A_means).reshape((128,64,3))
    return R_c

#Display Code. Leave it alooooooooooone.
R_c = np.rint(reconstruct_image(compressed_image, F, Q_norms, A_means)).astype(int)
print('Compressed Image: ')
plt.imshow(R_c)
plt.show()
Img = A[:, Idx]
R_o = A_pp[:, Idx].reshape(dimension)
print('Original Image')
plt.imshow(R_o)
plt.show()

# Two images should look similar. The compressed image may be a little more blurry.


def the_nearest_image(query_image, gallery_images, k, F, D, A_means, Q_norms):
    # YOUR CODE HERE
    compressg = []
    for i in range(len(gallery_images[0])):
        tmp1, tmp2 = reduce_dimensionality(gallery_images[:,i],k,F,D,A_means,Q_norms)
        compressg.append(tmp1)
    compress_imageg = np.array(compressg)
    compressed_imageq, pq = reduce_dimensionality(query_image,k,F,D,A_means,Q_norms)
    min_dis = np.inf
    for i in range(len(compress_imageg)):
        dis = np.linalg.norm(compressed_imageq-compress_imageg[i,:])
        if dis<min_dis :
            result = i
        min_dis = min(min_dis,dis)
    return result


query_image = imread("./val_query/0227_c2s1_046476_01.jpg")
query_image = query_image.flatten()

# read gallery images
gallery_images = []
original_gallery_images = []
filename = []
for file in os.listdir("./gallery"):
    if file.endswith(".jpg"):
        im = imread("./gallery/" + file)
        original_gallery_images.append(im)
        im = im.flatten()  # flatten im into a vector
        gallery_images.append(im)
        filename.append(file)

original_gallery_images = np.array(original_gallery_images)
gallery_images = np.stack(gallery_images).T

idx = the_nearest_image(query_image, gallery_images, 80, F, D, A_means, Q_norms)
plt.imshow(query_image.reshape(dimension))
plt.show()
plt.imshow(gallery_images[:, idx].reshape(dimension))
plt.show()



def image_similarity_ranking(image_gallery, image_query):
    gallery_images = image_gallery.reshape((len(image_gallery),-1))
    gallery_images = gallery_images.T
    k=80
    compressg = []
    for i in range(len(gallery_images[0])):
        tmp1, tmp2 = reduce_dimensionality(gallery_images[:,i],k,F,D,A_means,Q_norms)
        compressg.append(tmp1)
    # compress_imageg = np.array(compressg)
    image_query = image_query.flatten()
    compressed_imageq, pq = reduce_dimensionality(image_query,k,F,D,A_means,Q_norms)
    dis_list = []
    for i in range(len(compressg)):
        dis_list.append(np.linalg.norm(compressed_imageq-compressg[i]))
    res = np.argsort(dis_list)
    return res


id_list = image_similarity_ranking(original_gallery_images, imread("./val_query/0227_c2s1_046476_01.jpg"))

plt.imshow(imread("./val_query/0227_c2s1_046476_01.jpg"))
plt.show()
plt.imshow(original_gallery_images[id_list[0]])
plt.show()

def match_score(name, rr):
    def reid(idx):
        return filename[rr[idx]][:4]
    base = 0.0
    code = name[:4]
    if reid(0) == code or reid(1) == code or reid(2) == code:
        base += 0.4
        if (reid(0) == code):
            base += 0.3
        elif (reid(1) == code):
            base += 0.2
        elif (reid(2) == code):
            base += 0.1
        if (reid(0) == code and reid(1) == code) or (reid(0) == code and reid(2) == code) or (reid(1) == code and reid(2) == code):
            base += 0.2
            if (reid(0) == code and reid(1) == code and reid(2) == code):
                base += 0.1
    else:
        if (reid(3) == code):
            base += 0.4
        elif (reid(4) == code):
            base += 0.2
    return base

def total_score():
    score = 0
    for file in os.listdir("./val_query"):
        rr = image_similarity_ranking(original_gallery_images, imread("./val_query/" + file))
        #_, rr = the_nearest_image(imread("./test/" + file).flatten(), A_pp, 30, F, D, A_means, Q_norms)
        score += match_score(file, rr)
    return score

total_score()
