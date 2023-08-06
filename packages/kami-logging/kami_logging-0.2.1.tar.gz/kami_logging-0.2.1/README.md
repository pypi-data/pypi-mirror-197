<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="static/logo/icon.jpg" alt="Project logo"></a>
</p>

<h3 align="center">Kami Logging</h3>

<div align="center">


[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub release](https://img.shields.io/github/release/devkami/kami-logging?include_prereleases=&sort=semver&color=blue)](https://github.com/devkami/kami-logging/releases/)
[![issues - kami-logging](https://img.shields.io/github/issues/devkami/kami-logging)](https://github.com/devkami/kami-logging/issues)
[![pulls - kami-logging](https://img.shields.io/github/pulls/devkami/kami-logging)](https://github.com/devkami/kami-logging/pulls)
[![License](https://img.shields.io/badge/License-GNU-blue)](#license)


</div>

---

<p align="center"> Simple decorator to logging and benchmark functions
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Usage](#usage)
- [Built Using](#built_using)
- [TODO](../TODO.md)
- [Contributing](../CONTRIBUTING.md)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>

This package arose from the need to simplify the logging tasks of applications created by the Kami CO software development team.

Currently the package has 4 decorators: benchmark_with, logging_with, default_logging and default_benchmark for logging and basic performance testing with or without a defined logger object;

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the package and a daily use example.

### Prerequisites

- Python 3.x
- logging library

### Installing

```terminal
$pip install kami-logging
```

## 🎈 Usage <a name="usage"></a>
The four decorators available are:

- _**@logging_with:**_ generates a log message of type info at the beginning and end of the function execution, using a logger object defined by the developer

- _**@default_logging:**_ generates a log message of type info at the beginning and end of function execution, using a default logger object named 'default'

- _**@benchmark_with:**_ Generates a log message of type info with the runtime of the function accurate to 3 decimal places, using a developer-defined logger object

- _**@default_benchmark:**_ generates a log message of type info with the runtime of the function accurate to 3 decimal places, using a default logger object named 'default'

```python
import logging
from kami_logging import logging_with, benchmark_with

my_app_logger = logging.getLogger("my_app")

@benchmark_with(my_app_logger)
@logging_with(my_app_logger)
def my_func(*args, **kwargs):
  pass
```

Result:
<p align="center">
  <a href="" rel="noopener">
 <img src="static/example1.png" alt="Project logo"></a>
</p>

## ⛏️ Built Using <a name = "built_using"></a>

- [Python](https://www.python.org/) - Database
- [Logging](https://docs.python.org/3/library/logging.html) - Server Framework


## ✍️ Authors <a name = "authors"></a>

- [@maicondmenezes](https://github.com/maicondmenezes) - Idea & Initial work

See also the list of [contributors](https://github.com/devkami/kami-logging/contributors) who participated in this project.

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- References:
  - Arjancodes: [Github](https://github.com/ArjanCodes/), [Youtube](https://www.youtube.com/@ArjanCodes), [Twitter](https://twitter.com/arjancodes)
  - Eduardo Mendes: [Github](https://github.com/dunossauro), [Youtube](https://www.youtube.com/@Dunossauro), [Twitter](https://twitter.com/dunossauro)
