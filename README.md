# Trust The Dice

This script will pick from a list of outcomes, each with its own probability.

I wrote it to pick decisions for me randomly so that I wouldn't have to expend
the mental effort to do so.

[http://youcanbecueball.com/2019/05/13/trust-the-dice-1/](http://youcanbecueball.com/2019/05/13/trust-the-dice-1/)


# Installation

```
$ pip install trustthedice
```


# Usage

Give it outcomes with probabilities (represented as `x in y`) and it will pick one.

```
$ trustthedice random --outcome 'Heads: 1 in 2' --outcome 'Tails: 1 in 2'
Tails
```

You can abbreviate `--outcome` to `-oc`

```
$ trustthedice random -oc 'Heads: 1 in 2' -oc 'Tails: 1 in 2'
Tails
```

It's as random as [Python's `random.random`](https://docs.python.org/3/library/random.html#random.random) function is.


```
$ for i in {1..100}; do trustthedice random --outcome 'Heads: 1 in 2' --outcome 'Tails: 1 in 2'; done | sort | uniq -c
  49 Heads
  51 Tails
```

You can have as many outcomes as you want ...

```
$ trustthedice random -oc 'red: 18 in 37' -oc 'black: 18 in 37' -oc 'green: 1 in 37'
black
```

Just make sure the total probability is 1.

```
$ trustthedice random -oc 'red: 18 in 37' -oc 'black: 18 in 37' -oc 'green: 2 in 37'
Error: Total probability can't be more than one

The total of all the probabilities is more than 1.
Make sure that the total doesn't exceed 1!<
```

If you want, you can omit the final outcome and let `trustthedice` calculate
the final probability using the `--otherwise` option (it'll be 
`1 - total_of_other_probabilities`).

```
$ trustthedice random -oc 'red: 18 in 37' -oc 'black: 18 in 37' --otherwise 'green'
red
```

It can be tedious to type these out each time. If you init a project (i.e.
let `trustthedice` create a `.trustthedice` directory) you can save the
outcomes and re-run them.

```
$ trustthedice init
$ trustthedice events save 'coin flip' -oc 'Heads: 1 in 2' -oc 'Tails: 1 in 2'
$ trustthedice random --from-saved 'coin flip'
Heads
```


# Changelog


## v0.0.2

Make installation actually work ... (v0.0.1 didn't include any code)


## v0.0.1

Initial release

