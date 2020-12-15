# Shafi Inheritance 

## Introduction

In the Name of Allah, the Most Merciful and Compassionate,

This repository builds an inheritance solver for a reduced list of inheritors under the Shafi school of islamic jurispudence. 

It consists of 3 main pieces: 

1. [cases_geneator.py](src/cases_generator.py)

    This generates all valid inheritance cases of a certain size permuting the list of inheritors found in [family_config.csv](config/family_config.csv). 
    These are unsolved cases and are meant for practice and as input to the solver. An optional filter yml can be passed to 
    force certain inheritors to be present and others to be excluded. A sample file can be found [here](config/filter.yml).
2. [solver.py](src/solver.py)

    This solver produces the fractional shares of each inheritor without asaba and radd. Asaba is left only as 'A'. 
3. [full_solver.py](src/full_solver.py)

    This is the final solver. In this step we solve for Asaba, Radd and
    find the Asl (base shares) of the problem and finally assign integers to
    each inheritor.

## Sample Usage 

```buildoutcfg
python -m src.cases_generator --config config/family_config.csv \
                              --n_types 3 \
                              --output inheritance_3_filtered.csv \
                              --filter config/filter.yml
```   
This command uses all the inheritors found in [family_config.csv](config/family_config.csv), 
generates all valid cases of size 3, and output the fully solved cases to the output file inheritance_3_filtered.csv.
It will also filter using the filtration yml file.  


## Contributing 

To contribute to the repository please adhere to the following protocol: 

1. Ensure python 3.7 is installed in your environment. 
2. Clone the repository: 
    ```buildoutcfg
    git clone https://github.com/shafi-fiqh/inheritance.git
    ```
3. Activate the virtual environment you wish to work on, and 
    ```
    pip install -r requirements.txt 
    ```
4. Create a branch with the following naming convention: 
    ```buildoutcfg
    git checkout -b <feature_type>/<feature_name> 
    ```

    feature_type can either be 
    * doc: Documentation only, no code 
    * feature: Adding a feature 
    * bug: Fixing something that is not working as intended 
    
    Please use feature names that are indicative of the addition, for example: 
    ```
    git checkout -b feature/add_grandfather_rules
    ```
5. After completing your changes add a testing module under the [tests](tests) folder. Sample tests can be found, 
    with the appropriate naming convention. If logic is added, additional test cases for inheritors can be added [here](config/cases.json).
    
    Ensure tests pass by running 
    ```buildoutcfg
    python -m pytest    
    ```
   
6. Install black with 
    ```buildoutcfg
    pip install black
    ```
   and run 
   ```
   black . 
   ``` 
   from the root directory. 
7. After you make your changes, commit them to the branch 
    ```
    git commit
    ```
    
8. Push your changes to the repository: 
   ```
   git push 
   ```
9. Create a pull request to merge your feature to the master branch. 