Connection Speed Analysis
===

### About

A simple cli to run a speedtest-cli analysis and save it to a .CSV file.

The .CSV file is saved under:

```bash
$HOME/.connection_speed_analysis/results.csv
```

### How to run it

* clone this repository

```bash
git clone git@github.com:fcgomes92/connection_speed_analysis.git
cd connection_speed_analysis
```

* install the cli globally or in a virtualenv

```
pip install -e ./
```

* to run a single test just. The result will be appended to the .CSV

```bash
speed_analysis test_speed
```

* to set an hourly cron to check the speed

```bash
speed_analysis set_cron "$(which speed_analysis) test_speed"
```