# Blockhain

Creation of blockchain



## Test

To run test, you must install __pytest__ and __pytest-cov__

run:

``` shell script
$ pip install pytest pytest-cov
```

or

``` shell script
$ pip install -r requirements.txt
```


Now, to test the project, run:

``` shell script
pytest "tests/"
```

### Coverage

#### HTML

To run test with coverage in html:

``` shell script
pytest "tests/" --cov="app" --cov-report html
```

Now  you can open the file __htmlcov/index.html__ in your browser


#### XML

To run test with coverage in xml:

``` shell script
pytest "tests/" --junitxml=pytest-report.xml --cov="app" --cov-report xml
``` 

It will generate 2 files __pytest-report.xml__ and __coverage.xml__ (this files are requested for sonar)
