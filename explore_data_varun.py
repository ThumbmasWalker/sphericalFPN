# import the necessary packages
from uscnn.utils import Icosphere
from tqdm import tqdm
import meshplot as mp
import numpy as np
import glob
import os

mp.offline()

# np.random.seed(7)

np.random.seed(42)
COLORS = {
    k: np.random.uniform(0, 1, size=(3,)) for k in range(15)
}


def normalize(vectors, radius=1):
    '''
    Reproject to spherical surface
    '''

    scalar = (vectors ** 2).sum(axis=1)**.5
    unit = vectors / scalar.reshape((-1, 1))
    offset = radius - scalar

    return vectors + unit * offset.reshape((-1, 1))


if __name__ == "__main__":
    # grab the path to the dataset files
    paths = list(glob.glob("/home/varun/datasets/2d3ds_sphere/area_1/*.npz"))

    # sort the paths according to the split
    paths = sorted(paths, key=lambda x: int(x.split(os.path.sep)[-1].split(".")[0].split("_")[-1]))

    # constants
    level = 7
    nv_pad = 30 * (4**level)

    # initialise an icosphere
    ico = Icosphere(level=level)

    # load a sample image
    arr = np.load(paths[0])
    img, lbl = arr["data"], arr["labels"]

    # img = img[:ico.vertices.shape[0]]
    # zeros_pad = np.zeros((nv_pad, 4))
    # img = np.concatenate((img, zeros_pad))

    # for face in tqdm(ico.faces, total=ico.faces.shape[0]):
    #     # get the coordinates for the vertices of the current face
    #     coords = ico.vertices[face]

    #     # compute the coordinates of the midpoint vertices
    #     mid = np.vstack([[coords[x, :]] for x in [[0, 1], [1, 2], [0, 2]]]).mean(axis=1)

    #     # normalize the midpoint coordinates
    #     mid = normalize(mid)[:, None, :]

    #     # get the indices of the midpoint vertices
    #     idx1 = np.argmax((1 * np.equal(ico_up.vertices, mid[0])).sum(axis=1))
    #     idx2 = np.argmax((1 * np.equal(ico_up.vertices, mid[1])).sum(axis=1))
    #     idx3 = np.argmax((1 * np.equal(ico_up.vertices, mid[2])).sum(axis=1))

    #     # bilinear interpolation
    #     av1 = (img[face[0]] + img[face[1]]) / 2
    #     av2 = (img[face[1]] + img[face[2]]) / 2
    #     av3 = (img[face[0]] + img[face[2]]) / 2

    #     img[idx1] = av1
    #     img[idx2] = av2
    #     img[idx3] = av3

    # plot the image and save it to disk
    output_img_path = f"figs/tmp/lvl{level}_lbl.html"
    mp.plot(ico.vertices, ico.faces, c=np.array([COLORS[x] for x in lbl]), filename=output_img_path)
