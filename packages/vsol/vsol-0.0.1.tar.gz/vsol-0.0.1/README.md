# VSOL - Versatile Simple Objective Language

A simple, human-readable, and easy-to-use configuration file format.
<br>

Version: 0.0.1 <br>
Created by [**Md. Almas Ali**](https://github.com/Almas-Ali)
<br>

[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fvsol-lang%2Fvsol&count_bg=%2379C83D&title_bg=%23484848&icon=macys.svg&icon_color=%23F1F3FA&title=Hits&edge_flat=false)](https://hits.seeyoufarm.com)
![GitHub stars](https://img.shields.io/github/stars/vsol-lang/vsol.svg?style=social&label=Star&maxAge=2592000)
![GitHub forks](https://img.shields.io/github/forks/vsol-lang/vsol.svg?style=social&label=Fork&maxAge=2592000)
![GitHub last commit](https://img.shields.io/github/last-commit/vsol-lang/vsol.svg)
[![PyPI version](https://badge.fury.io/py/vsol.svg)](https://badge.fury.io/py/vsol)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/vsol.svg)](https://pypi.python.org/pypi/vsol/)
[![PyPI license](https://img.shields.io/pypi/l/vsol.svg)](https://pypi.python.org/pypi/vsol/)
[![PyPI status](https://img.shields.io/pypi/status/vsol.svg)](https://pypi.python.org/pypi/vsol/)
[![Total Downloads](https://static.pepy.tech/badge/vsol)](https://pepy.tech/project/vsol)

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Example](#example)
- [License](#license)


## Introduction

VSOL, which stands for **Versatile Simple Objective Language**, is a configuration file format that is designed to be easy to read, write, and understand. It is often used for configuring software applications, as it allows developers and users to specify settings and options in a clear and concise manner. VSOL files are written in a human-readable format, using plain text and simple syntax rules, making it easy to edit and manage them using a text editor or other software tools. This format is particularly useful for applications that require complex configurations, as it allows developers to organize settings hierarchically and specify default values, making it easier to maintain and modify settings over time. Overall, VSOL is a flexible and powerful configuration file format that can help improve the functionality and usability of software applications.

## Installation

```bash
pip install vsol
```

## Usage

```python
# Import VSOL
from vsol import VSOL

vsol = VSOL()

vsol.load("example.vsol")
```

## Example

```python
# VSOL - Versatile Simple Objective Language

# Base object
# This is a comment
string = "# This is not a comment"

.project
    site_name = "VSOL"
    version = "0.0.1"
    description = "VSOL - Versatile Simple Objective Language"
    authors = ["VSOL Team", "VSOL Contributors", "VSOL Users"]

.const
    const1 = "This is a const"

.debug
    debug = true

.contact
    authors_email = ["example@mail.com"]

.project_urls
    Documentation = "https://example.com"
    Github = "https://github.com/vsol-lang/vsol"

.license
    license = "MIT"

# Multi-level object
.inner1

    .inner2

        .inner3
            inner3 = "This is a inner3"

        .inner4
            inner4 = "This is a inner4"

    .inner5
        inner5 = "This is a inner5"

```

## License

[![forthebadge](https://forthebadge.com/images/badges/cc-0.svg)](https://forthebadge.com)

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
