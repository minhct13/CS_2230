import os
from PIL import Image

import torch
import torch.utils.data as data




def cid2filename(cid, prefix):
    """
    Creates a training image path out of its CID name
    
    Arguments
    ---------
    cid      : name of the image
    prefix   : root directory where images are saved
    
    Returns
    -------
    filename : full image filename
    """
    return os.path.join(prefix, cid[-2:], cid[-4:-2], cid[-6:-4], cid)

def pil_loader(path):
    # open path as file to avoid ResourceWarning (https://github.com/python-pillow/Pillow/issues/835)
    with open(path, 'rb') as f:
        img = Image.open(f)
        return img.convert('RGB')

def accimage_loader(path):
    import accimage
    try:
        return accimage.Image(path)
    except IOError:
        # Potentially a decoding problem, fall back to PIL.Image
        return pil_loader(path)

def default_loader(path):
    from torchvision import get_image_backend
    if get_image_backend() == 'accimage':
        return accimage_loader(path)
    else:
        return pil_loader(path)

def imresize(img, imsize):
    img.thumbnail((imsize, imsize), Image.ANTIALIAS)
    return img

def flip(x, dim):
    xsize = x.size()
    dim = x.dim() + dim if dim < 0 else dim
    x = x.view(-1, *xsize[dim:])
    x = x.view(x.size(0), x.size(1), -1)[:, getattr(torch.arange(x.size(1)-1, -1, -1), ('cpu','cuda')[x.is_cuda])().long(), :]
    return x.view(xsize)

def collate_tuples(batch):
    if len(batch) == 1:
        return [batch[0][0]], [batch[0][1]]
    return [batch[i][0] for i in range(len(batch))], [batch[i][1] for i in range(len(batch))]

class ImagesFromList(data.Dataset):
    """A generic data loader that loads images from a list 
        (Based on ImageFolder from pytorch)

    Args:
        root (string): Root directory path.
        images (list): Relative image paths as strings.
        imsize (int, Default: None): Defines the maximum size of longer image side
        bbxs (list): List of (x1,y1,x2,y2) tuples to crop the query images
        transform (callable, optional): A function/transform that  takes in an PIL image
            and returns a transformed version. E.g, ``transforms.RandomCrop``
        loader (callable, optional): A function to load an image given its path.

     Attributes:
        images_fn (list): List of full image filename
    """

    def __init__(self, root, images, imsize=None, bbxs=None, transform=None, loader=default_loader):

        images_fn = [os.path.join(root,images[i]) for i in range(len(images))]

        if len(images_fn) == 0:
            raise(RuntimeError("Dataset contains 0 images!"))

        self.root = root
        self.images = images
        self.imsize = imsize
        self.images_fn = images_fn
        self.bbxs = bbxs
        self.transform = transform
        self.loader = loader

    def __getitem__(self, index):
        """
        Args:
            index (int): Index

        Returns:
            image (PIL): Loaded image
        """
        path = self.images_fn[index]
        img = self.loader(path)
        imfullsize = max(img.size)

        if self.bbxs is not None:
            img = img.crop(self.bbxs[index])

        if self.imsize is not None:
            if self.bbxs is not None:
                img = imresize(img, self.imsize * max(img.size) / imfullsize)
            else:
                img = imresize(img, self.imsize)

        if self.transform is not None:
            img = self.transform(img)

        return img

    def __len__(self):
        return len(self.images_fn)

    def __repr__(self):
        fmt_str = 'Dataset ' + self.__class__.__name__ + '\n'
        fmt_str += '    Number of images: {}\n'.format(self.__len__())
        fmt_str += '    Root Location: {}\n'.format(self.root)
        tmp = '    Transforms (if any): '
        fmt_str += '{0}{1}\n'.format(tmp, self.transform.__repr__().replace('\n', '\n' + ' ' * len(tmp)))
        return fmt_str