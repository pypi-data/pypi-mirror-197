# Witter

## What's Witter?

Witter accepts text input, splits it into sections, or "chains", and then works out which character is most likely to follow that "chain" whenever it appears in the source text.

Once it has analyzed the source text, it generates a number of random sample pieces of text based on the source text.

Because of the way it uses the source text, the text that it produces will be "in the style" of the original text.

It's worth noting that this isn't Machine Learning (ML), or any kind of Artificial Intelligence (AI). It's statistics.

## How Do I Use Witter?

Run `witter` from within a virtual environment using the syntax:

```python
witter --help
```

or from the command line using:

```python
python -m witter --help
```

Both of these examples will display the command line options.

A simple example to get you started is:

* download a large text file - perhaps [The Complete Works of Shakespeare from Project Gutenberg](https://www.gutenberg.org/ebooks/100)
* pass the contents of the file to `witter`

In Windows or Linux, in a Python virtual environment, the following command will produce samples:

```bash
witter filepath.txt
```

or, if you want to use piping in Linux:

```bash
cat filepath.txt | witter
```