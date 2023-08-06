# Import libraries 
import sys as sys
import glob as glob 
import logging as logging
import os as os 
import random as random 
import torch as torch 

import linearmodels as linearmodels
from linearmodels import PanelOLS as PanelOLS
from linearmodels import RandomEffects as RandomEffects
from linearmodels import BetweenOLS as BetweenOLS

import simpletransformers as simpletransformers
from simpletransformers.classification import ClassificationModel as ClassificationModel 
from simpletransformers.classification import ClassificationArgs as ClassificationArgs 

from sklearn.model_selection import train_test_split as train_test_split
from sklearn.metrics import confusion_matrix, f1_score, classification_report, average_precision_score, auc, precision_recall_fscore_support, roc_curve

# global pd, np, plt, tf, tfds, stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import tensorflow as tf 
import tensorflow_datasets as tfds 
import scipy.stats as stats

### Function 1: Define seed.all() 
def seed_all(seed_value):
    """
    Set seed for python, PYTHONHASHSEED, CPU, and GPU vars. 
    """
    random.seed(seed_value) # Python
    np.random.seed(seed_value) # cpu vars
    torch.manual_seed(seed_value) # cpu  vars
    torch.cuda.manual_seed(seed_value) # gpu vars
    torch.cuda.manual_seed_all(seed_value) # gpu vars
    torch.backends.cudnn.deterministic = True # gpu vars
    torch.backends.cudnn.benchmark = False # gpu vars
    os.environ['PYTHONHASHSEED'] = str(seed_value) # Pythonhashseed

### Function 2: evaluate_classification() 
def evaluate_classification(y_true, y_pred):
    """
    Computes and prints classification report, confusion matrix, and F1 score for a classification task.
    
    Args:
    - y_true (series): True labels for the classification task.
    - y_pred (list): Predicted labels for the classification task.
    """
    # Print classification report
    print("Classification Report:")
    print(classification_report(y_true, y_pred))
    
    # Print confusion matrix
    print("Confusion Matrix:")
    print(confusion_matrix(y_true, y_pred))
    
    # Compute and print F1 score
    f1 = f1_score(y_true, y_pred)
    print(f"F1 Score: {f1:.3f}")

#### Function 3: predicted_probabilities()
def predicted_probabilities(raw_output): 
    """
    Extracts predicted probabilities.
    
    Args:
    - raw_out (array-like): Raw model outputs for each text.

    Returns:
    - (series-like): Predicted probabilities for the classification task.
    """
    raw_out = pd.DataFrame(raw_output)
    from scipy.special import expit
    return expit(raw_out)[1]

### Function 4: evaluate_plots()
def evaluate_plots(y_true, y_proba):
    """
    Computes and plots the precision-recall and ROC curves for a classification task using predicted probabilities.
    
    Args:
    - y_true (series-like): True labels for the classification task.
    - y_proba (series-like): Predicted probabilities for the positive class in the classification task.
    """
    # Compute precision-recall curve and area under the curve
    precision, recall, _ = precision_recall_curve(y_true, y_proba)
    pr_auc = auc(recall, precision)

    # Compute ROC curve and area under the curve
    fpr, tpr, _ = roc_curve(y_true, y_proba)
    roc_auc = auc(fpr, tpr)

    # Plot the curves
    plt.plot(recall, precision, color='darkorange', lw=2, label='Precision-Recall curve (AUC = %0.2f)' % pr_auc)
    plt.plot(fpr, tpr, color='blue', lw=2, label='ROC curve (AUC = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='gray', lw=2, linestyle='--')
    plt.xlabel('Recall / False Positive Rate')
    plt.ylabel('Precision / True Positive Rate')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.legend(loc="lower right")
    plt.show()

### Function 5: random_seeds()
def random_seeds(start, end, num):
    """
    Generate specified number of random seed numbers in a given range. 
    """
    random_numbers = []
    for j in range(num):
        random_numbers.append(np.random.randint(start, end))
    return random_numbers

### Function 6: train_with_seeds()
def train_with_seeds(seeds, train_args, train_data, validation_data, model_type, model_name, output_dir, train_metric, use_cuda=True, num_labels=2):
    """
    Train multiple models for a list of seeds. 

    Args:
    - seeds (list): List of random seeds to use for training.
    - train_args (ClassificationArgs): Arguments to use for training.
    - train_data (pandas.DataFrame): Training data.
    - validation_data (pandas.DataFrame): Validation data.
    - model_type (str): Type of model to use (e.g. 'bert', 'roberta', etc.).
    - model_name (str): Name of the pre-trained model to use.
    - output_dir (str): Path to directory to save the trained models.
    - use_cuda (bool): Whether or not to use GPU acceleration.
    - num_labels (int): Number of unique labels in the data.
    - train_metric (function): Function to use for evaluation metric (e.g. accuracy_score, f1_score, etc.).
    """
    models = []
    for seed in seeds:

        random.seed(seed) # Python
        np.random.seed(seed) # cpu vars
        torch.manual_seed(seed) # cpu  vars
        torch.cuda.manual_seed(seed) # gpu vars
        torch.cuda.manual_seed_all(seed) # gpu vars
        torch.backends.cudnn.deterministic = True # gpu vars
        torch.backends.cudnn.benchmark = False # gpu vars
        os.environ['PYTHONHASHSEED'] = str(seed) # Pythonhashseed

        # Update the random seed in train_args
        train_args['manual_seed'] = seed
        # Define the classification arguments
        train_args['output_dir'] = f"{output_dir}-seed-{seed}"

        # Initialize the model
        if use_cuda:
            model = ClassificationModel(
                model_type,
                model_name,
                args=train_args,
                use_cuda=True,
                num_labels=num_labels
            )
        else:
            model = ClassificationModel(
                model_type,
                model_name,
                args=train_args,
                use_cuda=False,
                num_labels=num_labels
            )

        # Train the model
        model.train_model(train_data, metric=train_metric,  eval_df=validation_data)

        # Add the trained model to the list of models
        models.append(model)

    # Return the list of trained models
    return models


### Function 7: evaluate_models()
def evaluate_models(model_paths, test_data):
    """
    Evaluates multiple models from path and given test dataset.

    Args: 
    - model_paths: A path where model folders are stored..
    - test_data (pandas.DataFrame): Test data.
    """
    results = []
    
    for i, path in enumerate(model_paths):
        print(f"Evaluating model {i+1} of {len(model_paths)}")
        
        # Load the model
        model = ClassificationModel('bert', path, use_cuda=True)
        
        # Evaluate the model on the test set
        predictions, _ = model.predict(list(test_data['text']))
        precision, recall, f1, _ = precision_recall_fscore_support(test_data['label'], predictions, average='weighted')
        
        # Record the evaluation metrics
        metrics = {'model_seed': f"model{i+1}", 'precision': precision, 'recall': recall, 'f1': f1}
        results.append(metrics)
    
    # Convert the results to a Pandas DataFrame
    results_df = pd.DataFrame(results)
    
    # Return results
    return results_df

### Function 8: apply_models()
def apply_models(models, data, subset_len=10000):
    """
    Applies models trained with multiple seeds on unseen data.

    Args: 
    - models: List of name of models loaded. 
    - data: Name of dataset to apply models.
    - subset_len: If 'data' is big, divide it into multiple sets to not run into memory issues.
    """
    results = []
    
    # Check if the data needs to be split into subsets
    if len(data) > subset_len:
        num_subsets = (len(data) + subset_len - 1) // subset_len
        subsets = [data[i*subset_len:(i+1)*subset_len] for i in range(num_subsets)]
    else:
        subsets = [data]
    
    # Apply each model to each subset of the data
    for i, subset in enumerate(subsets):
        print(f"Applying models to subset {i+1} of {len(subsets)}")
        subset_results = []
        for j, model in enumerate(models):
            model_results, _ = model.predict(list(subset['text']))
            model_results = pd.DataFrame({'model': f"model{j+1}", 'prediction': model_results})
            subset_results.append(model_results)
        results.append(pd.concat(subset_results, axis=1))
    
    return results

### Function 9: run_panel_models()
def run_panel_models(directory_path, file_type, models_to_run, dependent_var, independent_vars, entity_id_var, time_var):
    """
    Runs panel pooled OLS, random effects, and between effects models on multiple Excel/CSV files in a directory.

    Args:
        directory_path (str): Path to directory containing Excel/CSV files.
        file_type (str): File type. Possible values: 'excel', 'csv'.
        models_to_run (list): List of models to run. Possible values: 'pooled_ols', 'random_effects', 'between_effects', 'fixed_effects'.
        dependent_var (str): Name of dependent variable.
        independent_vars (list): List of names of independent variables.
        entity_id_var (str): Name of entity ID variable.
        time_var (str): Name of time variable.

    Returns:
        A list of model summaries.
    """
    results = {}

    # Get list of Excel/CSV files in directory
    if file_type == 'excel':
        files = glob.glob(directory_path + '*.xlsx')
    elif file_type == 'csv':
        files = glob.glob(directory_path + '*.csv')
    else:
        print('Invalid file type.')
        return

    # Loop through Excel/CSV files and run models
    for file in files:
        # Read in Excel/CSV file
        if file_type == 'excel':
            df = pd.read_excel(file)
        elif file_type == 'csv':
            df = pd.read_csv(file)

        # Define panel data
        panel_data = df.set_index([entity_id_var, time_var])

        # Panel pooled OLS
        if 'pooled_ols' in models_to_run:
            formula = dependent_var + ' ~ ' + '1 +' + ' + '.join(independent_vars)
            pooled_ols = PanelOLS.from_formula(formula, panel_data)
            pooled_ols_results = pooled_ols.fit()
            results['pooled_ols_' + file] = pd.DataFrame({'coefficients': pooled_ols_results.params, 'standard_errors': pooled_ols_results.std_errors})

        # Fixed effects
        if 'fixed_effects' in models_to_run:
            formula = dependent_var + ' ~ ' + '1 +' + ' + '.join(independent_vars)
            fixed_effects = PanelOLS.from_formula(formula, panel_data, entity_effects=True)
            fixed_effects_results = fixed_effects.fit()
            results['fixed_effects_' + file] = pd.DataFrame({'coefficients': fixed_effects_results.params, 'standard_errors': fixed_effects_results.std_errors})

        # Random effects
        if 'random_effects' in models_to_run:
            formula = dependent_var + ' ~ ' + '1 +' + ' + '.join(independent_vars)
            random_effects = RandomEffects.from_formula(formula, panel_data)
            random_effects_results = random_effects.fit()
            results['random_effects_' + file] = pd.DataFrame({'coefficients': random_effects_results.params, 'standard_errors': random_effects_results.std_errors})

        # Between effects
        if 'between_effects' in models_to_run:
            formula = dependent_var + ' ~ ' + '1 +' + ' + '.join(independent_vars)
            between_effects = BetweenOLS.from_formula(formula, panel_data)
            between_effects_results = between_effects.fit()
            results['between_effects_' + file] = pd.DataFrame({'coefficients': between_effects_results.params, 'standard_errors': between_effects_results.std_errors})

    return results

### Function 10: pooled_estimates()
def pooled_estimates(results):
    """
    Calculates the pooled estimates for each coefficient across all files and models.

    Args:
        results (dict): Dictionary of data frames containing coefficients and standard errors for each model and file.

    Returns:
        A data frame containing the pooled estimates for each coefficient.
    """
    # Create an empty dictionary to hold the coefficient estimates for each model
    model_coefficients = {}

    # Loop through the keys of the results dictionary and extract the coefficient estimates
    for key in results.keys():
        # Extract the coefficient estimates for the current model
        coefficients = results[key]['coefficients']
        # Add the coefficient estimates to the dictionary, creating a new list if necessary
        if key.split('_')[0] not in model_coefficients:
            model_coefficients[key.split('_')[0]] = [coefficients]
        else:
            model_coefficients[key.split('_')[0]].append(coefficients)

    # Calculate the pooled estimates for each coefficient and create a data frame to hold the results
    pooled_estimates = {}
    for model in model_coefficients.keys():
        # Concatenate the coefficient estimates for the current model across all files
        all_coefficients = pd.concat(model_coefficients[model], axis=1)
        # Calculate the pooled estimate for each coefficient and add it to the dictionary
        pooled_estimates[model] = np.mean(all_coefficients, axis=1)

    # Convert the pooled_estimates dictionary to a data frame and return it
    df = pd.DataFrame(pooled_estimates)
    df.columns = ["0"]
    return df
    
### Function 11: within_variance_estimate() # to calculate within-imputation variance
def within_variance_estimate(results):
    """
    Calculates the within imputation variance estimate for each coefficient across all files and models.

    Args:
        results (dict): Dictionary of data frames containing coefficients and standard errors for each model and file.

    Returns:
        A data frame containing the within variance estimate for each coefficient.
    """
    # Create an empty dictionary to hold the squared standard errors for each model
    model_se_squared = {}

    # Loop through the keys of the results dictionary and extract the squared standard errors
    for key in results.keys():
        # Extract the squared standard errors for the current model
        se_squared = results[key]['standard_errors']**2
        # Add the squared standard errors to the model_se_squared dictionary
        model_se_squared[key] = se_squared

    # Convert the model_se_squared dictionary to a data frame
    se_squared_df = pd.DataFrame(model_se_squared)

    # Calculate the average of the squared standard errors for each coefficient across all files and models
    avg_se_squared = se_squared_df.mean(axis=1)

    # Convert the within_var_estimate to a data frame and return it
    return pd.DataFrame(avg_se_squared)

### Function 12: within_variance_estimate() # to calculate within between-imputation variance
def between_variance_estimate(results, pooled_estimates):
    """
    Calculates the between variance estimate for each coefficient across all files and models.

    Args:
        results (dict): Dictionary of data frames containing coefficients and standard errors for each model and file.
        pooled_estimates (data frame): Data frame containing the pooled estimates for each coefficient.

    Returns:
        A data frame containing the between variance estimate for each coefficient.
    """
    # Create an empty dictionary to hold the coefficient estimates for each model
    model_coefficients = {}

    # Loop through the keys of the results dictionary and extract the coefficient estimates
    for key in results.keys():
        # Extract the coefficient estimates for the current model
        coefficients = results[key]['coefficients']
        # Add the coefficient estimates to the model_coefficients dictionary
        model_coefficients[key] = coefficients

    # Convert the model_coefficients dictionary to a data frame
    coefficients_df = pd.DataFrame(model_coefficients)

    # Subtract the pooled estimates from the coefficient estimates for each model and take the square
    deviations = (coefficients_df - pooled_estimates.values)**2

    # Calculate the sum of the squared deviations for each coefficient across all files and models
    sum_deviations_squared = deviations.sum(axis=1)

    # Calculate the between variance estimate for each coefficient as the sum of the squared deviations divided by the number of files minus one
    m = len(results.keys())
    between_var_estimate = sum_deviations_squared / (m-1)

    # Convert the between_var_estimate to a data frame and return it
    return pd.DataFrame(between_var_estimate)

### Function 13: pooled_standard_error() 
def pooled_standard_error(within_var_estimate, between_var_estimate, num_files):
    """
    Calculates the pooled standard error for each coefficient across all files and models.

    Args:
        within_var_estimate (data frame): Data frame containing the within variance estimate for each coefficient.
        between_var_estimate (data frame): Data frame containing the between variance estimate for each coefficient.
        num_files (int): The number of files.

    Returns:
        A data frame containing the pooled standard error for each coefficient.
    """
    # Calculate the between variance estimate divided by m
    between_var_by_m = between_var_estimate / num_files

    # Calculate the pooled variance estimate by summing the within variance estimate, between variance estimate, and between variance estimate divided by m
    pooled_var_estimate = within_var_estimate + between_var_estimate + between_var_by_m

    # Take the square root of the pooled variance estimate to get the pooled standard error
    pooled_std_error = np.sqrt(pooled_var_estimate)

    # Convert the pooled_std_error to a data frame and return it
    return pd.DataFrame(pooled_std_error)

### Function 14: calculate_p_values
def calculate_p_values(pooled_estimates, pooled_se):
    """
    Calculates the two-tailed p-values for each coefficient using the pooled estimate and pooled standard error.

    Args:
        pooled_estimates (pd.DataFrame): DataFrame containing the pooled estimates for each coefficient.
        pooled_se (pd.DataFrame): DataFrame containing the pooled standard errors for each coefficient.

    Returns:
        A DataFrame containing the two-tailed p-values for each coefficient.
    """
    # Calculate the absolute value of the pooled estimate divided by the pooled standard error
    z_values = abs(pooled_estimates.iloc[:, 0] / pooled_se.iloc[:, 0])

    # Calculate the two-tailed p-value using the cumulative distribution function of the standard normal distribution
    p_values = 2 * (1 - stats.norm.cdf(z_values))

    # Create a DataFrame to hold the p-values and return it
    return pd.DataFrame({'p_value': p_values})

### Function 15: regression_table()
def regression_table(coefficients, std_errors, p_values):
    """
    Creates a regression table with pooled estimates, pooled standard errors, and p-values.

    Args:
        coefficients (pd.DataFrame): Dataframe containing the pooled estimates for each coefficient.
        std_errors  (pd.DataFrame): Dataframe containing the pooled standard error for each coefficient.
        p_values (pd.DataFrame): Dataframe containing the p-values for each coefficient.

    Returns:
        A formatted regression table.
        A latex regression table
    """

    # Round numbers to 3 decimal places
    coefficients = coefficients.round(3)
    std_errors = std_errors.round(3)
    p_value = p_values.round(5)

    # Create empty dataframe to hold the regression table
    reg_table = pd.DataFrame(columns=['', 'Coefficient', 'Std. Error', 'p-value'])

    # Fill the dataframe with coefficient estimates, standard errors, and p-values
    for i, coeff in enumerate(coefficients.index):
        reg_table.loc[i] = [coeff, coefficients.values[i], std_errors.values[i], p_value.values[i]]

    # Convert the table to LaTeX format
    reg_table_latex = reg_table.to_latex(index=False)

    return reg_table_latex, reg_table