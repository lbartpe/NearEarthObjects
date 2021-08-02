# Explore Close Approaches of Near-Earth Objects

This program utilizes the command-line interface (CLI) to search for and
explore close approaches of near-Earth objects (NEOs), using data from
NASA/JPL's Center for Near Earth Object Studies.

## Overview

Located within is a command-line tool to inspect and query a dataset of NEOs
and their close approaches to Earth.

Concretely, the CLI tool reads data from both a CSV file and a JSON file,
converts that data into structured Python objects, performs filtering
operations on the data, limits the size of the result set, and writes the
results to a file in a structured format, such as CSV or JSON.

Abilities include inspection of the near-Earth objects in the data set and
query the data set of close approaches to Earth using any combination of the
following filters:

- Occurs on a given date.
- Occurs on or after a given start date.
- Occurs on or before a given end date.
- Approaches Earth at a distance of at least (or at most) X astronomical
    units.
- Approaches Earth at a relative velocity of at least (or at most) Y
    kilometers per second.
- Has a diameter that is at least as large as (or at least as small as)
    Z kilometers.
- Is marked by NASA as potentially hazardous (or not).

## Project Interface

This CLI tool is driven by the `main.py` script. That means that you'll run
`python3 main.py ... ... ...` at the command line to invoke the program.

At a command line, you can run `python3 main.py --help` for an explanation
of how to invoke the script.

```python
usage: main.py [-h] [--neofile NEOFILE] [--cadfile CADFILE] {inspect,query,interactive} ...

Explore past and future close approaches of near-Earth objects.

positional arguments:
  {inspect,query,interactive}

optional arguments:
  -h, --help            show this help message and exit
  --neofile NEOFILE     Path to CSV file of near-Earth objects.
  --cadfile CADFILE     Path to JSON file of close approach data.
```

There are three subcommands: `inspect`, `query`, and `interactive`.
Let's take a look at the interfaces of each of these subcommands.

### `inspect`

The `inspect` subcommand inspects a single NEO, printing its details in a
human-readable format. The NEO is specified with exactly one of the `--pdes`
option (the primary designation) and the `--name` option (the IAU name). The
`--verbose` flag additionally prints out, in a human-readable form, all known
close approaches to Earth made by this NEO. Each of these options has an
abbreviated version. To remind yourself of the full interface, you can
run `python3 main.py inspect --help`:

```
$ python3 main.py inspect --help
usage: main.py inspect [-h] [-v] (-p PDES | -n NAME)

Inspect an NEO by primary designation or by name.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Additionally, print all known close approaches of this NEO.
  -p PDES, --pdes PDES  The primary designation of the NEO to inspect (e.g. '433').
  -n NAME, --name NAME  The IAU name of the NEO to inspect (e.g. 'Halley').
```

Here are a few examples of the `inspect` subcommand in action:

```
# Inspect the NEO with a primary designation of 433 (that's Eros!)
$ python3 main.py inspect --pdes 433
NEO 433 (Eros) has a diameter of 16.840 km and is not potentially hazardous.

# Inspect the NEO with an IAU name of "Halley" (that's Halley's Comet!)
$ python3 main.py inspect --name Halley
NEO 1P (Halley) has a diameter of 11.000 km and is not potentially hazardous.

# Attempt to inspect an NEO that doesn't exist.
$ python3 main.py inspect --name fake-comet
No matching NEOs exist in the database.

# Verbosely list information about Ganymed and each of its known close approaches.
# For the record, Ganymed is HUGE - it's the largest known NEO.
$ python3 main.py inspect --verbose --name Ganymed
NEO 1036 (Ganymed) has a diameter of 37.675 km and is not potentially hazardous.
- On 1911-10-15 19:16, '1036 (Ganymed)' approaches Earth at a distance of 0.38 au and a velocity of 17.09 km/s.
- On 1924-10-17 00:51, '1036 (Ganymed)' approaches Earth at a distance of 0.50 au and a velocity of 19.36 km/s.
- On 1998-10-14 05:12, '1036 (Ganymed)' approaches Earth at a distance of 0.46 au and a velocity of 13.64 km/s.
- On 2011-10-13 00:04, '1036 (Ganymed)' approaches Earth at a distance of 0.36 au and a velocity of 14.30 km/s.
- On 2024-10-13 01:56, '1036 (Ganymed)' approaches Earth at a distance of 0.37 au and a velocity of 16.33 km/s.
- On 2037-10-15 18:31, '1036 (Ganymed)' approaches Earth at a distance of 0.47 au and a velocity of 18.68 km/s.
```

For an NEO to be found with the `inspect` subcommand, the given primary
designation or IAU name must match the data exactly, so if an NEO is
mysteriously missing, double-check the spelling and capitalization.

### `query`

The `query` subcommand is more significantly more advanced - a `query`
generates a collection of close approaches that match a set of specified
filters, and either displays a limited set of those results to standard output
or writes the structured results to a file.

```
$ python3 main.py query --help
usage: main.py query [-h] [-d DATE] [-s START_DATE] [-e END_DATE] [--min-distance DISTANCE_MIN] [--max-distance DISTANCE_MAX]
                     [--min-velocity VELOCITY_MIN] [--max-velocity VELOCITY_MAX] [--min-diameter DIAMETER_MIN]
                     [--max-diameter DIAMETER_MAX] [--hazardous] [--not-hazardous] [-l LIMIT] [-o OUTFILE]

Query for close approaches that match a collection of filters.

optional arguments:
  -h, --help            show this help message and exit
  -l LIMIT, --limit LIMIT
                        The maximum number of matches to return. Defaults to 10 if no --outfile is given.
  -o OUTFILE, --outfile OUTFILE
                        File in which to save structured results. If omitted, results are printed to standard output.

Filters:
  Filter close approaches by their attributes or the attributes of their NEOs.

  -d DATE, --date DATE  Only return close approaches on the given date, in YYYY-MM-DD format (e.g. 2020-12-31).
  -s START_DATE, --start-date START_DATE
                        Only return close approaches on or after the given date, in YYYY-MM-DD format (e.g. 2020-12-31).
  -e END_DATE, --end-date END_DATE
                        Only return close approaches on or before the given date, in YYYY-MM-DD format (e.g. 2020-12-31).
  --min-distance DISTANCE_MIN
                        In astronomical units. Only return close approaches that pass as far or farther away from Earth as the given
                        distance.
  --max-distance DISTANCE_MAX
                        In astronomical units. Only return close approaches that pass as near or nearer to Earth as the given
                        distance.
  --min-velocity VELOCITY_MIN
                        In kilometers per second. Only return close approaches whose relative velocity to Earth at approach is as fast
                        or faster than the given velocity.
  --max-velocity VELOCITY_MAX
                        In kilometers per second. Only return close approaches whose relative velocity to Earth at approach is as slow
                        or slower than the given velocity.
  --min-diameter DIAMETER_MIN
                        In kilometers. Only return close approaches of NEOs with diameters as large or larger than the given size.
  --max-diameter DIAMETER_MAX
                        In kilometers. Only return close approaches of NEOs with diameters as small or smaller than the given size.
  --hazardous           If specified, only return close approaches of NEOs that are potentially hazardous.
  --not-hazardous       If specified, only return close approaches of NEOs that are not potentially hazardous.
```

Here are a few examples of the `query` subcommand in action:

```
# Show (the first) two close approaches in the data set.
$ python3 main.py query --limit 2
On 1900-01-01 00:11, '170903' approaches Earth at a distance of 0.09 au and a velocity of 16.75 km/s.
On 1900-01-01 02:33, '2005 OE3' approaches Earth at a distance of 0.41 au and a velocity of 17.92 km/s.

# Show (the first) three close approaches on July 29th, 1969.
$ python3 main.py query --date 1969-07-29 --limit 3
On 1969-07-29 01:47, '408982' approaches Earth at a distance of 0.36 au and a velocity of 24.24 km/s.
On 1969-07-29 13:33, '2010 MA' approaches Earth at a distance of 0.21 au and a velocity of 8.80 km/s.
On 1969-07-29 19:56, '464798' approaches Earth at a distance of 0.10 au and a velocity of 8.02 km/s.

# Show (the first) three close approaches in 2050.
$ python3 main.py query --start-date 2050-01-01 --limit 3
On 2050-01-01 04:18, '2019 AY9' approaches Earth at a distance of 0.31 au and a velocity of 8.31 km/s.
On 2050-01-01 06:00, '162361' approaches Earth at a distance of 0.19 au and a velocity of 9.08 km/s.
On 2050-01-01 09:55, '2009 LW2' approaches Earth at a distance of 0.04 au and a velocity of 19.02 km/s.

# Show (the first) four close approaches in March 2020 that passed at least 0.4au of Earth.
$ python3 main.py query --start-date 2020-03-01 --end-date 2020-03-31 --min-distance 0.4 --limit 4
On 2020-03-01 00:28, '152561' approaches Earth at a distance of 0.42 au and a velocity of 11.23 km/s.
On 2020-03-01 09:28, '462550' approaches Earth at a distance of 0.47 au and a velocity of 17.19 km/s.
On 2020-03-02 21:41, '2020 QF2' approaches Earth at a distance of 0.45 au and a velocity of 8.79 km/s.
On 2020-03-03 00:49, '2019 TU' approaches Earth at a distance of 0.49 au and a velocity of 5.92 km/s.

# Show (the first) three close approaches that passed at most 0.0025au from Earth with a relative speed of at most 5 km/s.
# That's slightly less than the average distance between the Earth and the moon.
$ python3 main.py query --max-distance 0.0025 --max-velocity 5 --limit 3
On 1949-01-01 02:53, '2003 YS70' approaches Earth at a distance of 0.00 au and a velocity of 3.64 km/s.
On 1954-03-13 00:00, '2013 RZ53' approaches Earth at a distance of 0.00 au and a velocity of 3.04 km/s.
On 1979-09-02 00:16, '2014 WX202' approaches Earth at a distance of 0.00 au and a velocity of 1.79 km/s.

# Show (the first) three close approaches in the 2000s of NEOs with a known diameter of least 6 kilometers that passed Earth at a relative velocity of at least 15 km/s.
$ python3 main.py query --start-date 2000-01-01 --min-velocity 15 --min-diameter 6 --limit 3
On 2000-05-21 10:08, '7092 (Cadmus)' approaches Earth at a distance of 0.34 au and a velocity of 28.46 km/s.
On 2004-05-25 03:54, '7092 (Cadmus)' approaches Earth at a distance of 0.41 au and a velocity of 30.52 km/s.
On 2006-06-10 20:04, '1866 (Sisyphus)' approaches Earth at a distance of 0.49 au and a velocity of 26.81 km/s.

# Show (the first) two close approaches in January 2030 of NEOs that are at most 50m in diameter and are marked not potentially hazardous.
$ python3 main.py query --start-date 2030-01-01 --end-date 2030-01-31 --max-diameter 0.05 --not-hazardous --limit 2
On 2030-01-07 20:59, '2010 GH7' approaches Earth at a distance of 0.46 au and a velocity of 18.84 km/s.
On 2030-01-13 07:29, '2010 AE30' approaches Earth at a distance of 0.06 au and a velocity of 14.00 km/s.

# Show (the first) three close approaches in 2021 of potentially hazardous NEOs at least 100m in diameter that pass within 0.1au of Earth at a relative velocity of at least 15 kilometers per second.
$ python3 main.py query --start-date 2021-01-01 --max-distance 0.1 --min-velocity 15 --min-diameter 0.1 --hazardous --limit 3
On 2021-01-21 22:56, '363024' approaches Earth at a distance of 0.07 au and a velocity of 15.31 km/s.
On 2021-02-01 22:26, '2016 CL136' approaches Earth at a distance of 0.04 au and a velocity of 18.06 km/s.
On 2021-08-21 15:10, '2016 AJ193' approaches Earth at a distance of 0.02 au and a velocity of 26.17 km/s.

# Save, to a CSV file,  all close approaches.
$ python3 main.py query --outfile results.csv

# Save, to a JSON file, all close approaches in the 2020s of NEOs at least 1km in diameter that pass between 0.01 au and 0.1 au away from Earth.
$ python3 main.py query --start-date 2020-01-01 --end-date 2029-12-31 --min-diameter 1 --min-distance 0.01 --max-distance 0.1 --outfile results.json
```

### `interactive`

There's a third useful subcommand named `interactive`. This subcommand first
loads the database and then starts a command loop so that you can repeatedly
run `inspect` and `query` subcommands on the database without having to wait
to reload the data each time you want to run a new command, which saves an
extraordinary amount of time. This can be extremely helpful, as it lets you
speed up your development cycle and even show off the project more easily to
friends.

Here's what an example session might look like:

```
$ python3 main.py interactive
Explore close approaches of near-Earth objects. Type `help` or `?` to list commands and `exit` to exit.

(neo) inspect --pdes 433
NEO 433 (Eros) has a diameter of 16.840 km and is not potentially hazardous.
(neo) help i
Shorthand for `inspect`.
(neo) i --name Halley
NEO 1P (Halley) has a diameter of 11.000 km and is not potentially hazardous.
(neo) query --date 2020-12-31 --limit 2
On 2020-12-31 05:48, '2010 PQ10' approaches Earth at a distance of 0.45 au and a velocity of 21.69 km/s.
On 2020-12-31 16:00, '2015 YA' approaches Earth at a distance of 0.17 au and a velocity of 5.65 km/s.
(neo) q --date 2021-3-14 --min-velocity 10
On 2021-03-14 06:17, '2019 DS1' approaches Earth at a distance of 0.39 au and a velocity of 20.17 km/s.
On 2021-03-14 20:19, '483656' approaches Earth at a distance of 0.06 au and a velocity of 12.09 km/s.
...
```

The prompt is `(neo) `. At the prompt, you can enter either an `inspect` or a
`query` subcommand, with the exact same options and behavior as you would on
the command line. You can use the special command `quit`, `exit`, or `CTRL+D`
to exit this session and return to the command line. The command `help` or `?`
shows a help menu, and `help <command>` (e.g. `help query`) shows a help menu
specific to that command. In this environment only, you can also use the short
forms `i` and `q` for `inspect` and `query` (e.g. `(neo) i --verbose --name Ganymed)`).

All in all, the `interactive` subcommand has the following options:

```
$ python3 main.py interactive --help
usage: main.py interactive [-h] [-a]

Start an interactive command session to repeatedly run `interact` and `query` commands.

optional arguments:
  -h, --help        show this help message and exit
  -a, --aggressive  If specified, kill the session whenever a project file is modified.
```

## Project Scaffolding

```
.
├── data
│   ├── neos.csv
│   └── cad.json
│
├── tests
│   ├── test-neos-2020.csv
│   ├── test-cad-2020.json
│   ├── test_*.py
│   ├── ...
│   └── test_*.py
│
├── database.py
├── extract.py
├── filters.py
├── helpers.py     
├── main.py
├── models.py       
├── README.md
├── requirements.txt
└── write.py
```
