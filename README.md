# Blockhain

Creation of blockchain

# Development installation

* [__Flask__](https://flask.palletsprojects.com/en/1.1.x/)
* [__Flask-RESTful__](https://flask-restful.readthedocs.io/en/latest/)

## INSTALLATION

``` shell script
$ git clone ssh://git@git.boost.open.global:443/open/recherche_et_developpement/spectrum/blockchain.git
```

or 

``` shell script
$ git clone https://gitlab.boost.open.global/open/recherche_et_developpement/spectrum/mock_socket_bluetooth.git
```

``` shell script
$ cd blockchain
```

install the necessary package

``` shell script
$ python install -r requirements.txt
```

## RUN

To run the example (from flask cli):

``` shell script
$ python main.py test_block_chain  
```


To run the flask server:

``` shell script
$ python main.py run -h localhost 
```

The base url is [http://localhost:5000](http://localhost:5000)

#### List of routes

| Routes   |      METHODS      |  DESCRIPTION | EXAMPLE OF DATA |
|:----------|:---------:|:----------|:----------:|
| [/blockchain/init](http://localhost:5000/blockchain/init) |  POST | Create the first block (or add block if first block already exists) | [Example first bloc JSON](examples/example_first_bloc.json) |
| [/blockchain/init?from_json](http://localhost:5000/blockchain/init?from_json) | POST | Create an entire block chain from a json | [Example bloc chain JSON](examples/example_bloc_chain.json) |
| [/blockchain/add](http://localhost:5000/blockchain/add) | POST | Add block to the block chain (return error if block chain has not aa first block) | [Example bloc JSON](examples/example_bloc.json) |
| [/blockchain/compare](http://localhost:5000/blockchain/compare) | POST | Compare data of 2 block chain and return a concatenate version of the 2 block chains. | [Example compare block chain JSON](examples/example_compare_bloc_chain.json) |

## Update code

### Add route to the blueprint

You can add a new module in path __app/blockchain_api/views__ or add new resource in existing views, then you update the \_\___init____.py of __views__ package

#### Example
For example, we need to add a hello route

First we create a module __hello.py__ in __views__

__hello.py__

``` python
from flask_restful import Resource
from http import HTTPStatus


class Hello(Resource):
    def get(self):

        return "Hello world !", HTTPStatus.OK
```

The tree of our directory now look like the following:

``` shell script

app
├── blockchain_api
│   ├── __init__.py
│   └── views
│       ├── __init__.py
│       ├── blockchain.py
|       └── hello.py
...

```

Now, in the \_\___init____.py of __views__ package, we will add the following line

``` python
...
from app.blockchain_api.views.hello import Hello
...

api.add_resource(Hello, "/hello")
```

The complete file looks like

``` python
from flask import Blueprint
from flask_restful import Api

from app.blockchain_api.views.blockchain import BlockChainApi
from app.blockchain_api.views.hello import Hello

block_chain_blueprint = Blueprint("blockchain", __name__)
api = Api(block_chain_blueprint)


# init block_chain with a first block
api.add_resource(BlockChainApi, "/init")

# Only in README
api.add_resource(Hello, "/hello")
```

You can now run the server

``` shell script
python main.py run -h localhost
```

If you open [http://localhost:5000/blockchain/hello](http://localhost:5000/blockchain/hello),

You will have: 

"Hello world !"

### Add a new blueprint

If you need to add a new blueprint to your api, you need to create a new package at the root of __app__, and update the server

#### Example

For example, you need to create a blueprint __hello__

First we create a package __hello_api__ under app and a __views__ under __hello_api__

The tree of our directory now look like the following:

``` shell script
app
├── __init__.py
├── blockchain_api
│   ├── __init__.py
|   ├── ...
│   └── views
│       ├── __init__.py
│       ├── ...
├── hello_api
│   ├── __init__.py
│   └── views
│       └── __init__.py

```

Let's now create a module __hello_world.py__ under __views__ of __hello_api__

__hello_world.py__

``` python
from flask_restful import Resource
from http import HTTPStatus


class Hello(Resource):
    def get(self):

        return "Hello world !", HTTPStatus.OK

```

Now we will add the following code inside the \_\___init____.py of __views__ of __hello_api__

hello_api/views/\_\_init__.py

``` python
from flask import Blueprint
from flask_restful import Api

from app.hello_api.views.hello_world import Hello

hello_blueprint = Blueprint("hello", __name__)
api = Api(hello_blueprint)

api.add_resource(Hello, "/world")
```

Finally, we will update the \_\_init__.py of __app__

We must add the new blueprint in the __blueprints__ dict in the \_\_call__() method

the __key__ is the blueprint instance and the __value__ is the url prefix for all the routes of the blueprint

app/\_\_init__.py
``` python
class Server:

    __app = None

    def __init__(self):
        ...

    def __call__(self, *args, **kwargs):
        ...

        from app.blockchain_api.views import block_chain_blueprint
        from app.hello_api.views import hello_blueprint

        # register blueprints
        blueprints = {
            block_chain_blueprint: "/blockchain",
            hello_blueprint: "/hello"
        }
        self.__register_blueprints(blueprints=blueprints)

        ...
    
    ...
```

You can now run the server

``` shell script
python main.py run -h localhost
```

If you open [http://localhost:5000/hello/world](http://localhost:5000/hello/world),

You will have: 

"Hello world !"

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
