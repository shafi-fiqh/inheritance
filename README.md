# Shafi Inheritance 

## Introduction

In the Name of Allah, the Most Merciful and Compassionate,

The purpose of this repository is to provide educational resources for students of inheritance laws under the Shafi school of jurispudence.

## Sample Usage 

```buildoutcfg
python -m src.cases_generator --config config/family_config.csv --n_types 2 --output inheritance_2.csv
```   
where n_types is the number of inheritors. 


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

5. After you make your changes, commit them to the branch 
    ```
    git commit
    ```
    
6. Push your changes to the repository: 
   ```
   git push 
   ```
7. Create a pull request to merge your feature to the master branch. 