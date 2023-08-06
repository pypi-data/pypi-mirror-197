
# service-days
A tool to help calculate the number of service days between two dates given a service schedule.


[![PyPI - Version](https://img.shields.io/pypi/v/service-days.svg)](https://pypi.org/project/service-days)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/service-days.svg)](https://pypi.org/project/service-days)

-----
**Table of Contents**

- [Concepts](#concepts)
- [Installation](#installation)
- [License](#license)
- [Miscellany](#miscellany)

## Concepts  
There are many libraries that will find the number work days between two dates, but what
if you don't work Monday to Friday? What if your schedule is Monday, Thursday, Saturday?  

This library calls that 3 day work schedule "service days"; as in, there are 3  "service days" in a given week.    

It will calculate the number of service days between two dates given a service schedule.

`service-days` is a library that will calculate the number of service days between two dates

### Tools 
**Add Days**  Given a date and a service schedule, add `x` number of days to get to the next service day.  

**Days in Period**  Given a start date and an end date, calculate the number of service days in that period.

**Convert JSON formatted text list, to list of days**  Given a JSON formatted list of days, convert it to a list of days.

e.g. 
```
'["Mon", "Tue"]'
```


## Installation

```console
pip install service-days
```

## License

`service-days` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.


## Miscellany

This is my first attempt at using hatch to manage a Python project. I'm not sure if I'm doing it right, but I'm trying. If you have any suggestions, please let me know. Thanks!