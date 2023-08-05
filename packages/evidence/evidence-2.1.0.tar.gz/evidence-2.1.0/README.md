# Description

Differential analysis of DFXML idifference2.py output.

# Installation

`pip install evidence`

# Usage

**From command line:**

`python -m evidence --path PATH [--output OUTPUT]`

| Option | Short | Type | Default | Description |
|---|---|---|---|---|
|--path | -p | String | - | Path to idifference output dir |
|--output | -o | String | output | Path to result dir |


# Example

Given the following files, where the first placeholer describes
the action and the secon placeholder describes the number of execution.

IMPORTANT: noise.1.idiff needs to exsists. It contains only information 
with no action applied.  

```
ge/
    *.*.idiff
    noise.1.idiff
```

Important: the first placeholder is used as an identifier and must be
the same for each following execution. Example:

```
ge/
    a.1.idiff
    a.2.idiff
    a.3.idiff
    noise.1.idiff
```


`python -m evidence -p path/to/idifference2result`

```
################################################################################

evidence by 5f0
Differential analysis of DFXML idifference2.py output

Current working directory: path/to/evidence

Datetime: 01/01/1970 10:20:30

################################################################################

--> Creating folder structure
    --> path/to/evidence/output

--> Prepare Evidence
    --> Write File: path/to/evidence/output/pe/a.1.pe
    --> Write File: path/to/evidence/output/pe/a.2.pe
    --> Write File: path/to/evidence/output/pe/a.3.pe
    --> Write File: path/to/evidence/output/pe/b.1.pe
    --> Write File: path/to/evidence/output/pe/b.2.pe
    --> Write File: path/to/evidence/output/pe/b.3.pe
    --> Write File: path/to/evidence/output/pe/c.1.pe
    --> Write File: path/to/evidence/output/pe/c.2.pe
    --> Write File: path/to/evidence/output/pe/c.3.pe
    --> Write File: path/to/evidence/output/pe/noise.1.pe

--> Merge Evidence
    --> Write File: path/to/evidence/output/me/a.me
    --> Write File: path/to/evidence/output/me/b.me
    --> Write File: path/to/evidence/output/me/c.me
    --> Write File: path/to/evidence/output/me/noise.me

--> Characterize Evidence
    --> Calculate Characteristic Evidence for a
        --> Action for Evidence Sum: b
        --> Action for Evidence Sum: c
        --> Action for Evidence Sum: noise
        --> Write File: path/to/evidence/output/ce/a.ce
    --> Calculate Characteristic Evidence for b
        --> Action for Evidence Sum: a
        --> Action for Evidence Sum: c
        --> Action for Evidence Sum: noise
        --> Write File: path/to/evidence/output/ce/b.ce
    --> Calculate Characteristic Evidence for c
        --> Action for Evidence Sum: a
        --> Action for Evidence Sum: b
        --> Action for Evidence Sum: noise
        --> Write File: path/to/evidence/output/ce/c.ce

################################################################################

Execution Time: 2.519259 sec
```

# License

MIT