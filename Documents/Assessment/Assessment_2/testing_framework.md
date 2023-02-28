[Back to content page](README.md)

------

## Review and choice of testing framework
We reviewd 4 popular testing framework for python, discusses their pros and cons and justifying the final choice of testing framework that best fit out test plan. The 4 frameworks are as follow:

1. [Robot Framework](#robot-framework)
2. [pytest](#pytest)
3. [PyUnit (unittest)](#pyunit-unittest)
4. [Nose2](#nose2)

### [Robot Framework](https://robotframework.org/)

Free, open-source test automation framework predominately used for acceptance testing and acceptance test-driven development. It requires Python version 3.6 or newer, and can be used on almost all platforms.

Pros: 
- Keyword-driven which are beginner friendly and allow users to easily create highly readable test cases
- Test data syntax can be easily used and combined
- Complete ecosystem consists of common tools and testing libraries, where function can be reuse in another project
- Rich built-in library offers many APIs and is highly extensible

Cons:
- Fixed form writing can lead to complexity when developing complex automation systems
- Hard to customize HTML report
- Robot Framework cannot run parallel tests without use of external tool (e.g. Selenium Grid)

### [pytest](https://docs.pytest.org/en/7.2.x/)

Open-source Python-based unit testing framework. It requires Python 3.7 or newer. Easy to learn, and offers more features such as assertion rewriting comparing to PyUnit.

Pros:
- Informative test feedback comparing to PyUnit
- Test cases are fast and easy to write, compact (less boilerplate code), expressive and readable
- Functional modularization, help cover all parameter combinations without rewriting test cases
- Scalability, offers rich and useful plugins (e.g. pytest-xdist allows parallel tests without additional test runners)
- Values in test case are stored after test is complete, details on which value assertion failed and value was asserted are available

Cons:
- Uses special syntax which reduce test cases compatibility with other frameworks
- Can be overkill when developing simple test cases

### [PyUnit (unittest)](https://wiki.python.org/moin/PyUnit)

Python standard unit testing automation framework. `unittest.TestCase` class provides special assertion methods, similar to Pytest. Using unittest-sml-reporting allows generation of XML reports.

Pros:
- Comes with Python standard library 
- Easy syntax and conventions suitable for beginners
- Individual test cases can be run easily, test outputs are concise flexible
- Fast test reports generation

Cons:

- Uses of snake\_case for (Python) and camelCase (JUnit) naming method still exists which can be confusing
- Test code can be difficult to read it becomes too abstract

### [Nose2](https://docs.nose2.io/en/latest/)

Support Python versions that are currently supported by the Python team. An extension of unittest, through plugins it add support for test execution and discovery, decorators, fixtures, parameterization, and more.

Pros:
- Can extend uinttest test case with nose2 functions
- Rich built-in plugins
- Allows parallel testing
- Automatic tests collection (Providing users follow  guidelines when organizing library and test code)

Cons:
- Documentation can be challenging to read
- No as actively maintained compares to other frameworks

### Choice and justification

At the current state of our development, we believe pytest is the best fit compare to other frameworks mentioned above. 

Our group is familiar with the Python syntax, and pytest uses a similar syntax that can reduce test cases development time.

Pytest has a large active user base, more inforamtion can be found online when encountering bugs (e.g. stackoverflow) which can also lead to less development time.

Pytest has the richest test case output file comparing to other frameworks, such as using JUnit to output .xml file that can be used by the pipeline. It also offers more pulgins comparing to unittest.

------

[Back to content page](README.md)
