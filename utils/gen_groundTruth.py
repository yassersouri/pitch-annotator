import scipy.io

FOLDER = '/Users/yasser/sci-repo/pitchdataset/groundTruth/%s' % 'train'

test_mat = '/Users/yasser/sci-repo/BSR_dataset/16068.mat'
test_image = '/Users/yasser/sci-repo/BSR_dataset/16068.jpg'

def main():
    loaded_mat = scipy.io.loadmat(test_mat)
    print loaded_mat.keys()

if __name__ == '__main__':
    main()