## How to run the code?

Let me show you how to use the code.

It can divided to two parts.

### Part1: make your image database
When you clone the repository, it will look like this:

    ├── flask/          # website
    ├── src/            # Source files
    ├── USAGE.md        # How to use the code
    └── README.md       # Intro to the repo

you need to add your images into a directory called __database/__, so it will look like this:

    ├── flask/          # website
    ├── src/            # Source files
    ├── USAGE.md        # How to use the code
    ├── README.md       # Intro to the repo
    └── database/       # Directory of all your images

__all your image should put into database/__

In this directory, each image class should have its own directory

see the picture for details:



In my database, there are 25 classes, each class has its own directory,

and the images belong to this class should put into this directory.

### Part2: run the code
I implement several algorithm, you can run it with python3.

#### For RGB histogram
```python
python3 src/color.py
```

#### For daisy image descriptor
```python
python3 src/daisy.py
```

#### For gabor filter
```python
python3 src/gabor.py
```

#### For edge histogram
```python
python3 src/edge.py
```

#### For histogram of gradient (HOG)
```python
python3 src/HOG.py
```

#### For VGG19
You need to install pytorch0.2 to run the code
```python
python3 src/vggnet.py
```

#### For ResNet152
You need to install pytorch0.2 to run the code
```python
python3 src/resnet.py
```

#### Indexing for the feature vector 
You need to install  <a href="https://github.com/yahoojapan/NGT/wiki/Python-Quick-Start">NGT</a> and get feature images before to run the code 

```python
python3 src/NGT.py
```
#### For create and save index NGT and info images into datase 
You need to install sqlite to run the code
```python
python3 src/SQLite.py
```
Above are basic usage of my codes.

There are some advanced issue such as features fusion and dimension reduction,

the intro of these parts will be written further in the future :D

### Appendix: feature fusion
I implement the basic feature fusion method -- concatenation.

Codes for feature fusion is written in [fusion.py](https://github.com/phandungmta/CBIR-Conten-base-image-retrivel-Website-search-imageblob/master/src/fusion.py)

In fusion.py, there is a class called *FeatureFusion*.

You can create a *FeatureFusion* instance with an argument called **features**.

For example, in [fusion.py line140](https://github.com/phandungmta/CBIR-Conten-base-image-retrivel-Website-search-imageblob/master/src/fusion.py#L140)
```python
fusion = FeatureFusion(features=['color', 'daisy'])
APs = evaluate_class(db, f_instance=fusion, d_type=d_type, depth=depth)
```
- The first line means to concatenate color featrue and daisy feature.
- The second line means to evaluate with the concatenated feature.

If you want to know the performance of all possible feature combination, look at [fusion.py line122](https://github.com/phandungmta/CBIR-Conten-base-image-retrivel-Website-search-imageblob/master/src/fusion.py#L122) for example
```python
evaluate_feats(db, N=2, d_type='d1')
```
- Parameter *N* means how many feature you want to concatenate.
- Parameter *d_type* means the distance metric you want to use.
- Function *evaluate_feats* will generate a result file that record performances for all feature concatenation.

## Author
Po-Chih Huang / [@pochih](http://pochih.github.io/)
## <a href="https://github.com/pochih/CBIR">Source code</a>

## Implement
Phan duc dung/[@phandungmta]
