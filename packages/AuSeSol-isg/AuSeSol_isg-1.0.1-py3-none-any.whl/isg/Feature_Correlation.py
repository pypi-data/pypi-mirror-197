
from datetime import datetime, timedelta
import dask.dataframe as dd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mutual_info_score
from sklearn.linear_model import Lasso
from sklearn.feature_selection import SelectFromModel
from tqdm import tqdm
import os
import warnings
import pdb
from scipy.stats import pointbiserialr, pearsonr, spearmanr
import heapq
from sklearn.preprocessing import StandardScaler
from pathlib import Path
import pandas as pd
from os import listdir
import time




# --------------------------------------------------------------------------- #
#             create_folder                                       #
# --------------------------------------------------------------------------- #
def create_folder(path):
	Path(path).mkdir(parents=True, exist_ok=True)



# --------------------------------------------------------------------------- #
#             read_parquet_and_resample                                       #
# --------------------------------------------------------------------------- #

def read_parquet_and_resample(file_path, columns):
    # Read the Parquet file into a pandas DataFrame
    df = dd.read_parquet(file_path, columns=columns, index="Datetime").compute()
    print(f'Loaded Parquet file -> {file_path}')
    df.index = pd.to_datetime(df.index)     
    df = df.resample('1T').mean() 

    # Print some basic information about the resampled DataFrame
    print(f"DataFrame shape: {df.shape}")
    print(f"DataFrame columns: {df.columns}")
    print(f"DataFrame index range: {df.index.min()} to {df.index.max()}")
    print(f"DataFrame missing values:\n{df.isna().sum()}")
    # Create Csv
    path_to_created_csv = 'data/resampled_df_2020.csv'
    df.to_csv(path_to_created_csv)
    print(f'Csv created as {path_to_created_csv}')
    # Return the resampled DataFrame
    return df


def read_csv_resampled():
    df = pd.read_csv('data/resampled_df_2020.csv')
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df = df.set_index('Datetime')    
    # Print some basic information about the resampled DataFrame
    print(f"DataFrame shape: {df.shape}")
    print(f"DataFrame columns: {df.columns}")
    print(f"DataFrame index range: {df.index.min()} to {df.index.max()}")
    print(f"DataFrame missing values:\n{df.isna().sum()}")
    return df


    
# =========================================================================== #
#             other functions                                                 #
# =========================================================================== #

def get_consecutive_nan(df, column='DNI'):
    # Find consecutive NaN values in column A
    groups = df[column].isna().cumsum()
    consec_nans = groups[df[column].isna()].value_counts()

    # Create dictionary of consecutive NaN values and index of first NaN in group
    nan_dict = {}
    for group in consec_nans.index:
        first_nan_index = df.index[groups.eq(group)].min()
        nan_dict[first_nan_index] = consec_nans[group]

    return nan_dict

def first_nan_value(df, column='DNI'):
    # Check which values in column 'A' are missing
    is_missing = df[column].isnull()

    # Get the index of the first missing value
    first_missing_idx = is_missing.idxmax()

    # Print the first missing value in column 'A'
    print(f"The first missing value in column {column} occurs at index {first_missing_idx}")
    print(f"Value: {df.loc[first_missing_idx, column]}")
    return first_missing_idx
    
    
    
def check_n_prev_next_values_from_idx(df, timestamp, n_values=3, direction='past', column='DNI'):
    # get the index of the timestamp
    ts_index = df.index.get_loc(timestamp)
    for i in range(1, n_values+1):
        # get the index of the previous row
        if direction == 'past':
            prev_index = ts_index - i
        elif direction == 'future':
            prev_index = ts_index + i
        print(df.index[prev_index])  # output: 2019-03-15 11:48:00
        print(df.loc[df.index[prev_index], column] )


# ========================================================================================== #
# 1)     Function to be called from main
# ========================================================================================== #
def generate_feature_importances(df, methods=['pearson', 'spearman', 'kendall', 'tree', 'mi']):
    """
    Generates feature importances for all columns of the input DataFrame using the specified feature selection methods.
    Saves the resulting DataFrames to disk in the "correlation_csvs" directory.
    
    Parameters:
    df (pandas.DataFrame): The input DataFrame.
    methods (list): A list of feature selection methods to use. Defaults to ['pearson', 'spearman', 'kendall', 'tree', 'mi'].
    """
    # Turn off warnings
    warnings.filterwarnings('ignore')
    df.dropna(axis=0, how='any', inplace=True)
    # Iterate over all columns in the DataFrame
    for target in tqdm(df.columns):
        # Iterate over all feature selection methods
        for method in methods:
            # Generate feature importances
            feature_importances_df = feature_importances(df, target=target, method=method)
            # Save feature importances
            target_dir = f"correlation_csvs/{target}"
            create_folder(target_dir)
            filename = f"{method}.csv"

            feature_importances_df.to_csv(os.path.join(target_dir, filename), index=False)

# ========================================================================================== #
#  2)  called from generate_feature_importances
# ========================================================================================== #

def feature_importances(df, target, method='pearson', n=7, alpha=1):
    """
    Plots the n most important features according to the specified feature selection method.

    Parameters:
    df (pandas.DataFrame): The input DataFrame.
    target (str): The name of the target column.
    method (str): The feature selection method to use. Can be 'pearson', 'spearman', 'kendall', 'tree', 'mi', or 'lasso'.
        Defaults to 'pearson'.
    n (int): The number of top features to display. Defaults to 5.
    alpha (float): The regularization parameter for the Lasso method. Only used if method is 'lasso'. Defaults to 1.

    Returns:
    pandas.DataFrame: The feature importances ranked by importance.
    """
    
    if method == 'pearson':
        corr_matrix = df.corr(method='pearson')
        feature_importances_df = _pearson_kendall_spearman(corr_matrix, target)
        
    elif method == 'spearman':
        corr_matrix = df.corr(method='spearman')
        feature_importances_df = _pearson_kendall_spearman(corr_matrix, target)
        
    elif method == 'kendall':
        corr_matrix = df.corr(method='kendall')
        feature_importances_df = _pearson_kendall_spearman(corr_matrix, target)
        
    elif method == 'tree':
        features = df.drop(target, axis=1)
        targets = df[target]
        model = DecisionTreeRegressor(random_state=42)
        model.fit(features, targets)
        feature_importances = model.feature_importances_
        indices = np.argsort(feature_importances)[::-1]
        feature_importances_df = pd.DataFrame({'Feature': features.columns[indices], 'Importance': feature_importances[indices]})
        
    elif method == 'mi':
        features = df.drop(target, axis=1)
        targets = df[target]
        mi_scores = []
        for feature in features:
            mi_score = mutual_info_score(features[feature], targets)
            mi_scores.append(mi_score)
        feature_importances_df = pd.DataFrame({'Feature': features.columns, 'Importance': mi_scores})
        feature_importances_df.sort_values(by='Importance', ascending=False, inplace=True)

    elif method == 'lasso':
        features = df.drop(target, axis=1)
        target = df[target]
        clf = Lasso(alpha=alpha)
        sfm = SelectFromModel(clf)
        sfm.fit(features, target)
        selected_features = sfm.transform(features)
        feature_importances_df = pd.DataFrame({'Feature': features.columns[sfm.get_support()], 'Importance': np.abs(clf.coef_[sfm.get_support()])})
        feature_importances_df.sort_values(by='Importance', ascending=False, inplace=True)

    else:
        raise ValueError(f"Method '{method}' not recognized.")
    
    # Plot barplot
    barplot_features(feature_importances_df, target, method, n)
    generate_heatmap(df, target, n)
        
    return feature_importances_df

# ------------------------------------------------------------------------------------------ #

def _pearson_kendall_spearman(corr_matrix, target):
    feature_importances_df = pd.DataFrame({'Feature': corr_matrix.columns, 'Importance': corr_matrix[target].abs()})
    feature_importances_df.sort_values(by='Importance', ascending=False, inplace=True)
    return feature_importances_df

# ------------------------------------------------------------------------------------------ #
    
def barplot_features(df, target, method, n):
    # df contains the most important features
    fig, ax = plt.subplots(figsize=(12,6))
    sns.barplot(x='Importance', y='Feature', data=df.head(n), ax=ax)
    ax.set_title(f'Top most important features for {target} using {method}')
    ax.set_xlabel('Feature importance')
    ax.set_ylabel('Feature')
    target_dir = f'images/{target}'
    create_folder(target_dir)
    plt.savefig(f'{target_dir}/{method}.png', bbox_inches='tight')
    plt.close()

# ------------------------------------------------------------------------------------------ #

def generate_heatmap(df, target_col, n):
    # Generate a heatmap of the top n most correlated features to the target column in a DataFrame.
    corr = df.corr()
    corr_target = abs(corr[target_col])
    top_features = corr_target.nlargest(n).index.tolist()
    top_features.append(target_col)
    top_features = list(set(top_features))
    plt.figure(figsize=(10, 8))
    mask = np.zeros_like(df[top_features].corr())
    mask[np.triu_indices_from(mask, k=0)] = True
    mask[np.diag_indices_from(mask)] = False
    sns.heatmap(df[top_features].corr(), annot=True, cmap='coolwarm', mask=mask, center=0)
    plt.title(f'{target_col}Top {n} Most Correlated Features')
    plt.savefig(f'images/{target_col}/Heatmap.png')
    
# ------------------------------------------------------------------------------------------ #

# ----------------------------   PriorityQ with correlation as priority  --------------------------------- # 

class PriorityQueue:
    '''
    Keeps track of the best subset with its corresponding correlation value
    '''
    def __init__(self):
        self.heap = []
        self.set = set()

    def isEmpty(self):
        return len(self.heap) == 0

    def push(self, subset, priority):
        # Priority = Merit, higher priority offered first
        if frozenset(subset) in self.set:
            return
        heapq.heappush(self.heap, (-priority, subset))
        # frozenset as a dictionary key
        self.set.add(frozenset(subset))

    def pop(self):
        # return item with the highest priority and remove it from queue
        (priority, item) = heapq.heappop(self.heap)
        self.set.remove(frozenset(item))
        return (item, -priority) 
    
# ----------------------------   Get the target-feature-subset correlation  --------------------------------- #

def get_correlation(df, feature1, feature2):
    if df[feature1].nunique() == 1 or df[feature2].nunique() == 1:
        # use point-biserial correlation if one or both variables are binary
        corr, _ = pointbiserialr(df[feature1], df[feature2])
    else:
        # use Pearson's correlation for continuous variables
        corr, _ = pearsonr(df[feature1].dropna(), df[feature2].dropna())
        
    return corr

def get_Merit(df, feature_subset, label):
    '''
    For a subset of features, returns the correlation with target
    '''
    if not feature_subset[0]:
        # no best Feature was found
        return 0
    
    # average feature-class correlation
    rcf_all = []
    for feature in feature_subset:
        coeff = get_correlation(df, label, feature)
        rcf_all.append(abs(coeff))
    rcf = np.mean(rcf_all)
    
    # average feature-feature correlation
    corr = df[feature_subset].corr().abs()
    corr.values[np.tril_indices_from(corr.values)] = np.nan
    rff = corr.unstack().mean()

    k = len(feature_subset)
    return (k * rcf) / np.sqrt(k + k * (k-1) * rff)

# ----------------------------   Get highest correlated feature  --------------------------------- #

def get_first_best_feature(df, features, label):
    '''
    Out of all the possible features, returns the feature that yields the highest correlation with target
    '''
    best_value = -1
    best_feature = ''
    for feature in features:
        coeff = get_correlation(df, label, feature)
        abs_coeff = abs(coeff)
        if abs_coeff > best_value:
            best_value = abs_coeff
            best_feature = feature
    print("For Sensor: [%s] Feature [%s] with merit %.4f" % (label, best_feature, best_value))
    return best_feature, best_value



# ----------------------------   Plot feat vs target  --------------------------------- #
def plot_feat(df, feature, target, merit_score, path=None, n=10):
    length_of_day = 1440

    daily_hr_str = [f'day_{i}' for i in range(1, n+1)]
    day_range = np.arange(0, length_of_day*len(daily_hr_str), length_of_day)
    
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.set_xticks(day_range)
    ax1.set_xticklabels(daily_hr_str)
    ax1.grid(True)
    
    x = df[feature].values.reshape(-1, 1)
    y = df[target].values.reshape(-1, 1)
    X = StandardScaler().fit_transform(x)
    Y = StandardScaler().fit_transform(y)
    
    sns.lineplot(data=X[:length_of_day*len(daily_hr_str)], color="blue", alpha=0.7, ax=ax1)
    sns.lineplot(data=Y[:length_of_day*len(daily_hr_str)], color="red", alpha=0.9, ax=ax1)
    ax1.axhline(y=0, color='black', linestyle='--', alpha=0.4)
    
    ax1.set_xlabel("Time in days", fontsize=12)
    ax1.set_ylabel("Normalized values of features", fontsize=12)
    ax1.set_title(f'Target: {target} for feature {feature} | Corr_score : {merit_score}', fontsize=14)
    
    ax1.legend(['Feature: '+ feature, 'Target: '+target], loc='upper right', fontsize=12, title='Legend')
    
    if path:
        create_folder(path)
        feature_path = f'{path}/{target}'
        create_folder(feature_path)
        plt.savefig(feature_path + '/' + f'Target_{target}_with_feature_{feature}.png', bbox_inches='tight')
        plt.close()
    # plt.show()

# ----------------------------   get_related_features  --------------------------------- #


def get_related_features(df, target, save_path=None):
    '''
    Main function that returns the subset of possible features with the highest correlation to target.
    '''    
    delta = 0.01  # correlation change to consider new feature
    features = df.columns.tolist()
    features.remove(target)

    best_feature, best_value = get_first_best_feature(df, features, target)

    # initialize queue
    queue = PriorityQueue()
    # push first tuple (subset, merit)
    queue.push([best_feature], best_value)
    # list for visited nodes
    visited = []
    # counter for backtracks
    n_backtrack = 0
    best_subset = [best_feature]
    # limit of backtracks
    max_backtrack = 10
    # repeat until queue is empty
    # or the maximum number of backtracks is reached
    while not queue.isEmpty():
        # get element of queue with highest merit
        subset, priority = queue.pop()
        # check whether the priority of this subset
        # is higher than the current best subset
        if priority <= best_value + delta:
            n_backtrack += 1
        else:
            best_value = priority
            best_subset = subset
        # goal condition
        if n_backtrack == max_backtrack:
            break
        # iterate through all features and look of one can
        # increase the merit
        for feature in features:
            temp_subset = subset + [feature]
            # check if this subset has already been evaluated
            for node in visited:
                if set(node) == set(temp_subset):
                    break
            else:
                # ... mark it as visited
                visited.append(temp_subset)
                # ... compute merit
                merit = get_Merit(df, temp_subset, target)  
                # and push it to the queue
                queue.push(temp_subset, merit)
    # Get best_value
    best_value = round(best_value, 3)
    # Print to screen
    print(f"for Sensor: [{target}] -> best subset [{best_subset}] with merit score: [{best_value}]")
    # Plot/Save images from features
    for feat in best_subset:
        plot_feat(df, feat, target, best_value, path=save_path, n=20)
    
    return target, best_subset, best_value

# ----------------------------   get_virtual_sensors_for_feature --------------------------------- #

def get_virtual_sensors_for_feature(df, target, save_path=None):
    '''
    :param features: list of str, sensors (columns) names
    :param target: str of target column
    '''
    start = time.time()
    target, best_subset, best_value = get_related_features(df, target, save_path=save_path)
    end = time.time()
    conversion = timedelta(seconds=(end - start))
    print(f"\nElapsed time: {conversion}")
    print("\n**********************************************************************")
    return target, best_subset, best_value


# ----------------------------   build_complete_sensor_network --------------------------------- #

def build_complete_sensor_network(df, save_path=None):
    '''
    Loads CSV(s) - for every sensor in sensor list:
     - Returns best subset of features with highest correlation.
     - Trains a neural network
    '''
    sensor_list = []
    features_l = df.columns.tolist()
    for idx, target in enumerate(features_l):
        df_copy = df.copy()
        target, best_subset, best_value = get_virtual_sensors_for_feature(df_copy, target, save_path=save_path)
        sensor_dict = {'target':target, 'best_subset':best_subset, 'best_value':best_value}
        sensor_list.append(sensor_dict)
    df = pd.DataFrame.from_dict(sensor_list)
    return df


def drop_non_changing_features(df):
    # Drop columns that never change
    unchanged_cols = df.columns[df.nunique() == 1]
    df = df.drop(columns=unchanged_cols)
    print(f'Dropped columns with constant values: {unchanged_cols}')
    return df

# ============================================================================== #
#              MAIN                                                              #
# ============================================================================== #
save_path = 'save_path_feature_selection'
# .............................................................................. #

def feature_selection_main(df, save_path=None):
    # -------------------------------------------------- #
    df = drop_non_changing_features(df)
    # Build sensor network
    sensor_df = build_complete_sensor_network(df=df, save_path=save_path)
    # Save Sensor network into a csv
    save_sensors = "data/sensors_correlation/sensors_df_correlation.csv"
    sensor_df.to_csv(save_sensors, index=False)
