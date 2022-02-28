# TUGAS KECIL 2 IF2211 STRATEGI ALGORITMA

## Pembuatan Pustaka Convex Hull dengan Menggunakan Algoritma Divide and Conquer
Pustaka myConvexHull adalah pustaka buatan yang dapat digunakan untuk mencari Convex Hull dari himpunan titik yang berada pada suatu bidang datar. Pustaka dibangun berdasarkan pustaka ConvexHull dari paket scipy.spatial sebagai referensi. Pustaka ditulis dalam bahasa Python dan berada pada direktori 
```
src\myConvexHull.py
```

## Requirement
Pastikan bahwa Python sudah terinstall pada perangkat yang digunakan. Program ini menggunakan beberapa pustaka seperti matplotlib dan pandas yang mungkin tidak bersifat pre-installed pada distribusi standar Python. Oleh karena itu, Anda dapat menggunakan distribusi Anaconda atau melakukan instalasi pustaka yang dibutuhkan menggunakan pip.

## Cara Penggunaan Pustaka
Pada program pengolahan data yang Anda buat, lakukan import untuk pustaka matplotlib, pandas, dan datasets dari paket sklearn, bersamaan dengan pustaka myConvexHull. Pada contoh berikut ini, diasumsikan bahwa file myConvexHull.py berada pada direktori yang sama dengan program utama.
```
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import dataset
from myConvexHull import myConvexHull
```

Load dataset yang diinginkan, lalu buat dataframenya. Sebagai contoh, akan digunakan dataset Iris.
```
data = datasets.load_iris()
df = pd.DataFrame(data.data, columns=data.feature_names) 
df['Target'] = pd.DataFrame(data.target) 
```

Untuk mencari Convex Hull dan melakukan visualisasi data, gunakan pustaka matplotlib.pyplot yang sebelumnya sudah dinamai sebagai plt. Misalkan akan dicari dan divisualisasikan diagram yang menggambarkan hubungan antara petal-length dengan petal-width dari bunga iris berdasarkan jenisnya.
```
plt.figure(figsize = (10, 6))
colors = ['b','r','g']
plt.title('Petal-length vs Petal-width')
plt.xlabel(data1.feature_names[2]) # <-
plt.ylabel(data1.feature_names[3]) # <-
for i in range(len(data1.target_names)):
    bucket = df[df['Target'] == i]
    bucket = bucket.iloc[:,[2,3]].values # <-
    hull = myConvexHull(bucket)
    plt.scatter(bucket[:, 0], bucket[:, 1], label=data1.target_names[i])
    for line in hull.lines:  
        plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], colors[i])
plt.legend()
plt.show()
```
Perhatikan bahwa angka 2 dan 3 (ditandai dengan tanda panah) adalah indeks dari atribut yang ingin dibandingkan. Pada dataset Iris, atribut Petal-length berada pada indeks 2 dan Petal-width berada pada indeks 3.

Terakhir, jalankan program Python Anda dan diagram pun akan ditampilkan.

---
Pustaka dibuat oleh Christine Hutabarat (13520005) - 13520005@std.stei.itb.ac.id
