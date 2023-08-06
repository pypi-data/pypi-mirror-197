## PyIMCTrans

This tool reads the IMC schema from a XML file, locally creates files containing the messages and connects (imports) the main global machinery.

See `/example` to check an example implementation of the Follow Reference maneuver.

### Change log:
#### Version 0.1.1
    - Handle lost TCP connection/End of file:
        - Gracefully terminates, if EOF (or equivalent) is encountered.
    - Added a .subscribe_all() function.
    - Added MIT License
    - On extract, downloads IMC.xml definition from main git repository, when none is found.
    - Added an 'Unknown message', used when a message with valid sync number and valid crc but unknown id is received.
    - Update pyproject.toml
        - Corrected version
        - Added license
        - Added keywords

### End-User
- Fancying a virtual env?
```shell
$ sudo apt install python3.8-venv
$ python3 -m venv tutorial_env
$ source tutorial_env/bin/activate
```
- To use:
```shell
$ pip3 install pyimclsts
$ # or, if you are cloning the repo, from the folder pyproject.toml is located, run:
$ pip3 install .
```
- Choose a folder and have a version of the IMC schema
```shell
$ wget https://raw.githubusercontent.com/LSTS/imc/master/IMC.xml
```
- Extract messages locally
```shell
$ python3 -m pyimclsts.extract
```
- And you are ready to go!
### Dev
    - Build with 
    ```shell
    $ python3 -m build
    ```
    - Upload with (currently to TestPyPi):
    ```shell
    $ python3 -m twine upload --repository testpypi dist/*
    ```
    - You might need
    ```shell
    $ python3 -m pip install --upgrade twine
    ```
### Current TODO list:
    - Improve README
        - Add a description of the general functioning of the tool.
    - Implement a message whitelist
        - Although it works without problems, it is a little cumbersome to have +300 available messages.
    - Implement logging?
        - In the subscriber, message bus or the IO Interface?

    - Notes:
    - Users MUST be warned (documentation?) that the constructor does not type check, because the other operations (serialization) may fail if not correctly used. However, failure by type checking or failure by serialization is ultimately a failure during runtime, which begs the question: How to avoid a runtime error?
    - Currently using IntFlag to make bitfields. It works, but does not throw exceptions when using an invalid combination of flags.
        - Should it throw errors in this case?
    