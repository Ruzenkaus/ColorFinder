from __future__ import print_function
import binascii
import struct
from PIL import Image
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
from tkinter import Tk, Button, Label, filedialog, messagebox

def find_color():

    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])

    if file_path:
        im = Image.open(file_path)
        im = im.resize((150,150))

        ar = np.asarray(im)
        shape = ar.shape

        ar = ar.reshape(np.prod(shape[:2]),shape[2]).astype(float)

        print('finding clusters')

        codes,dist = scipy.cluster.vq.kmeans(ar, 5)
        print('clustesr centres: ', codes)



        vecs, dist = scipy.cluster.vq.vq(ar, codes)
        counts, bins = np.histogram(vecs, len(codes))

        index_max = np.argmax(counts)
        peak = codes[index_max]
        colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
        print('most frequent is %s (#%s)' % (peak, colour))
        M_L.config(text='most frequent is %s (#%s)' % (peak, colour))
    else:
        messagebox.showerror(message="You didn't select path")

if __name__ == '__main__':

    window = Tk()
    window.title('Main_color')

    M_L = Label(text='Choose your image and here will be your color!')
    M_L.grid(column=1, row=0)
    b_c = Button(text='Detect color', command=find_color)
    b_c.grid(column=1, row=1)

    window.mainloop()

