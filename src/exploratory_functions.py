import numpy as np
import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.impute import KNNImputer
from scipy.stats import boxcox, kstest, anderson, chi2, logistic, weibull_min, gamma, poisson, beta, lognorm, triang, chi2_contingency, bartlett
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller, kpss, grangercausalitytests
from statsmodels.tsa.seasonal import seasonal_decompose

def load_data(file_path, sep, date_column):   
    # Read CSV file into a Pandas DataFrame
    data = pd.read_csv(file_path, sep=sep, parse_dates=[date_column], dayfirst=True)
    return data
def process_observation_period(df, date_column):
    # Define a function to process each observation period
    def extract_first_date(period):
        first_date = period.split('/')[0]
        return first_date.split('T')[0]  # Take only the date part

    # Apply the function to the 'observation period' column
    df[date_column] = df[date_column].apply(extract_first_date)

    # Convert the column to datetime
    df[date_column] = pd.to_datetime(df[date_column])

    return df
def preprocess_data(data, date_column, target_column, renamed_target):

    data = data.sort_values(by=date_column)
    # Set the Date column as the index
    data.set_index(date_column, inplace=True)
    # Rename the column 
    data.rename(columns={target_column: renamed_target}, inplace=True)
    return data

def replace_commas_with_points(value):
    try:
        # If the value is already a dot, return it as it is
        if isinstance(value, str) and value == '.':
            return value
        # Otherwise, attempt to convert the value to a float and replace commas with dots
        elif isinstance(value, str):
            return float(value.replace(',', '.'))
        else:
            return value
    except ValueError:
        # If conversion fails or the value is not a string, return the original value
        return value
    
def temporal_serie(data, target):
    plt.figure(figsize=(12,6))
    plt.plot(data[target], color='black')
    min_timestamp = data.index.min()
    new_timestamp = min_timestamp - pd.DateOffset(days=30)
    max_timestamp = data.index.max()
    new_timestamp_max = max_timestamp + pd.DateOffset(days=30)
    plt.xlim([new_timestamp, new_timestamp_max])
    plt.xlabel('Time (years)')    
    plt.ylabel(f'{target}')
    plt.show()

def seasonal_decompositions(data, col):

    additive_decomposition = seasonal_decompose(data[col], model='additive', period=30)
    multiplicative_decomposition = seasonal_decompose(data[col], model='multiplicative', period=30)

    # Calculate the standard deviation of residuals for each decomposition
    additive_residual_std = additive_decomposition.resid.std()
    multiplicative_residual_std = multiplicative_decomposition.resid.std()

    # Select the decomposition with lower standard deviation of residuals
    if multiplicative_residual_std < additive_residual_std:
        selected_decomposition = 'multiplicative'
        decomposition = multiplicative_decomposition
    else:
        selected_decomposition = 'additive'
        decomposition = additive_decomposition
    # Plot the residual component for both additive and multiplicative decompositions
    plt.figure(figsize=(12, 6))

    plt.plot(additive_decomposition.resid, label='Aditiva', color='black')
    plt.plot(multiplicative_decomposition.resid, label='Multiplicative', color='brown')

    plt.title('Resudual Components')
    plt.xlabel('Time (years)')
    plt.ylabel('Residual')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    print('This is the selected decomposition', selected_decomposition)

    return decomposition, selected_decomposition

def trend(data, target):
    plt.subplots(figsize=(8,4))
    data.trend.plot(color='black')
    plt.xlabel('Time (years)')    
    plt.ylabel(f'{target}')
    plt.show()

def seasonality_decomposition(data, target):
    plt.subplots(figsize=(8,4))
    data.seasonal.plot(color='black')
    plt.xlabel('Time (years)')    
    plt.ylabel(f'{target}')
    plt.show()

def seasonality(data, target):
    plt.figure(figsize=(12,8))
    sns.boxplot(data=data, x=data.index.year, y=target, color= 'black')
    plt.xlabel('Time (years)')
    plt.ylabel(f'{target}')
    plt.show()

def hist_plot(data, target):
    try:
        # Filter out infinite values from the target data
        filtered_data = data[~np.isinf(data[target])]

        # Plot histogram and KDE using kdeplot
        plt.figure(figsize=(12, 6))
        sns.histplot(filtered_data[target], color="black", bins=30, kde=True)
        plt.xlabel('Daily Maximum Temperature Distribution')
        plt.ylabel('Density')
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")


#Transformation functions
def homogeneity_variance_test(data, target):
    # Divide the time series into two equal parts
    n = len(data[target])
    part1 = data[target][:n//2]
    part2 = data[target][n//2:]

    # Evaluate homogeneity with Bartlett's test
    bartlett_test = bartlett(part1, part2)

    # Determine test result based on p-value
    if bartlett_test[1] > 0.05:
        print("---------------------------------------------------------------------------------------------------\n"
            "The null hypothesis of homoscedasticity is not rejected. We do not have sufficient evidence to claim\n"
            "This implies that: there are significant differences in variance between the groups.")
        return(bartlett_test)
    else:
        print("---------------------------------------------------------------------------------------------------\n"
            "Alert: The null hypothesis of homoscedasticity is rejected. There is no constant variation; this is, the outliers\n"
            "are very significant")
        return(bartlett_test)
        
def apply_boxcox(data, renamed_target):
    """
    If lambda is between 0 and 1: A family of power transformations is applied:
    - If lambda equals 0: A logarithmic transformation is applied.
    - If lambda equals 0.5: A square root transformation is applied.
    - If lambda equals 1: No transformation is applied.
    """
    transformed_df = data.copy()
    # Apply Box-Cox transformation to the specified column
    transformed_col, lambda_val = boxcox(transformed_df[renamed_target] + 1)  # Adding 1 to handle zero and negative values
    transformed_df[renamed_target] = transformed_col

    # Print the estimated lambda value
    
    if float(lambda_val) < 1:
        print("---------------------------------------------------------------------------------------------------")
        print(homogeneity_variance_test(transformed_df, renamed_target))
        print(f"Lambda value for Box-Cox transformation of '{renamed_target}': {lambda_val}\n"
        "---------------------------------------------------------------------------------------------------\n")
        print(transformed_df.describe().T)
        hist_plot(transformed_df, renamed_target)
        return transformed_df
    else:
        print("---------------------------------------------------------------------------------------------------\n"
            "If lambda equals 1: No transformation is applied\n"
            "---------------------------------------------------------------------------------------------------")

        print(data.describe().T)
        return data
    
def handle_missing_values(data, target):
    # Check if there are null values in the specified column
    if data[target].isnull().any():
        # Perform KNN imputation only if there are null values
        _knn = data.copy(deep=True)
        knn_imputer = KNNImputer(n_neighbors=2, weights="uniform")
        _knn[[target]] = knn_imputer.fit_transform(_knn[[target]])
        print("---------------------------------------------------------------------------------------------------\n"
            "Null values after imputation:", _knn[[target]].isnull().sum())
        return _knn
    else:
        print("---------------------------------------------------------------------------------------------------\n"
            "No null values found in the column. Skipping imputation.")
        return data
# Functions to explore the distribution
def find_best_distribution(data, distributions_list):
    p_values = []
    best_distribution = None
    best_p_value = 0
    
    for distribution in distributions_list:
        # Fit the distribution to the data
        params = getattr(stats, distribution).fit(data)
        
        # Perform the Kolmogorov-Smirnov test
        _, p_value = stats.kstest(data, distribution, args=params)
        
        # Save the p-value
        p_values.append(p_value)
        
        # Update the best distribution if necessary
        if p_value > best_p_value:
            best_p_value = p_value
            best_distribution = distribution
    
    return best_p_value, best_distribution



def goodness_of_fit_test(data, bins=10):
    """
    Perform a goodness-of-fit test using the Chi-squared test.
    This provides information about the adequacy of the observed data 
    to a specific distribution
    Returns:
    float: The p-value from the Chi-squared test.
    
    """
    print("---------------------------------------------------------------------------------------------------\n"
    "Null Hypotesis (H_o) Distribution:\n"
    "---------------------------------------------------------------------------------------------------\n"
    "There is no significant difference between the observed frequencies and the expected frequencies\n" 
    "assuming a uniform distribution\n"
    "---------------------------------------------------------------------------------------------------")
    # Compute the observed frequencies in each bin
    observed, bin_edges = np.histogram(data, bins=bins)

    # Compute the expected frequencies assuming uniform distribution
    expected = np.full_like(observed, len(data) / bins)

    # Form the contingency table
    contingency_table = np.vstack((observed, expected))

    # Perform the Chi-squared test
    chi2_stat, p_value, _, _ = chi2_contingency(contingency_table)

    if p_value > 0.05:
        print("we fail to reject the null hypothesis. This outcome suggests that there is no significant difference between the observed frequencies and\n"
      "the expected frequencies assuming a uniform distribution. In simpler terms, it implies that the data fits well with the idea of being\n"
      "uniformly distributed across the defined bins or categories. This means that the observed data does not deviate significantly from what\n"
      "would be expected if it followed a uniform distribution pattern. Therefore, we can conclude that the observed frequencies align reasonably\n"
      "well with the expected frequencies under the assumption of uniformity.")

    elif p_value <= 0.05:
        print("We reject the null hypothesis. This indicates that there is a significant difference between the observed frequencies and the expected \n"
         "frequencies assuming a uniform distribution. We can conclude that the data does not fit the uniform distribution well, and there may be a \n"
         "systematic deviation from uniformity.")
    elif p_value < 0.001:
        print("It suggests strong evidence against the null hypothesis. It indicates that the observed data significantly deviates from what would be \n"
         "expected under a uniform distribution.")
    
    elif p_value > 0.999:
        print("suggests strong evidence in favor of the null hypothesis. It indicates that there is no significant difference between the observed \n" 
        "and expected frequencies, supporting the adequacy of the uniform distribution assumption")
    
    else:
        print("The p-value does not fall into any predefined conditions.")

    return p_value


def perform_kpss_and_dfuller_test(data, target, regression='ct'):
    print("----------------------------------------------------------------------------------------\n"
        "Null Hypotesis ADF and KPSS tests:\n"
        "- ADF test Ho: If the p-value is less than the significance level, we reject the null hypothesis\n" 
        "and conclude that the time series is stationary.\n"
        "- KPSS test Ho: If the p-value is greater than the significance level, we fail to reject the null\n"
        "hypothesis, indicating that there is not enough evidence to conclude that the time series is stationary.")
    # Perform KPSS test
    kpss_result = kpss(data[target], regression=regression)
    dftest = adfuller(data[target], autolag='AIC')
    adf_results = {
        'ADF': dftest[0],
        'P-Value': dftest[1],
        'Num Of Lags': dftest[2],
        'Num Of Observations Used For ADF Regression and Critical Values Calculation': dftest[3],
        'Critical Values': dftest[4]
    }
    # Print the test results
    print("----------------------------------------------------------------------------------------\n"
        "Resuls ADF test\n"
    "----------------------------------------------------------------------------------------")
    for key, value in adf_results.items():
        print(f"   {key}: {value}")

    print("----------------------------------------------------------------------------------------\n"
        "Resuls KPSS test\n"
        "----------------------------------------------------------------------------------------")
    print("KPSS Statistic:", kpss_result[0])
    print("p-value:", kpss_result[1])
    print("Lags Used:", kpss_result[2])
    print("Critical Values:")
    for key, value in kpss_result[3].items():
        print(f"   {key}: {value}")
    return dftest, kpss_result

def make_stationary(data, target, threshold):
    dftest = adfuller(data[target], autolag=None, maxlag=20)
    kpss_result = kpss(data[target], regression='ct')
    if (dftest[1] > threshold) | (kpss_result[1]<threshold):
        print ('Data is non-stationary. Applying first differencitation...\n'
               'Note: You should compute dftest, and kpss test again')
        stationary_data = data[target].diff().dropna() 
        stationary_data_df = pd.DataFrame(stationary_data) # First-order differencing
        return stationary_data_df
    else:
        print("The time series is already stationary.")
        return data
    
#Autocorrelation functions
def acf_test(data, target):
    fig, ax = plt.subplots(figsize=(8, 5))
    plot_acf(data[target], ax=ax, color='black')
    plt.ylim((-1,1.5))
    ax.set_xlabel(f'Temporal Lag {target}')
    ax.set_ylabel('Autocorrelation')
    plt.show()

def pacf_test(data, target):
    fig, ax = plt.subplots(figsize=(8, 5))
    plot_pacf(data[target], ax=ax, color='black')
    plt.ylim((-1,1.5))
    ax.set_xlabel(f'Temporal Lag {target}')
    ax.set_ylabel('Partial Autocorrelation')
    plt.show()


def grangers_causation_matrix(data, target_column, variables, test='ssr_chi2test', verbose=False):    
    """Check Granger Causality of all possible combinations of the Time series.
    The rows are the response variable, columns are predictors. The values in the table
    are the P-Values. P-Values lesser than the significance level (0.05), implies
    the Null Hypothesis that the coefficients of the corresponding past values is
    zero, that is, the X does not cause Y can be rejected.
 
    data      : pandas dataframe containing the time series variables
    variables : list containing names of the time series variables.
    """
    maxlag=30
    nivel_sig = 0.05
    df = pd.DataFrame(np.zeros((len(variables), len(variables))), columns=variables, index=variables)
    for c in df.columns:
        #print(c)
        for r in df.index:
            #print(r)
            test_result = grangercausalitytests(data[[r, c]], maxlag=maxlag, verbose=False)
            p_values = [round(test_result[i+1][0][test][1],4) for i in range(maxlag)]
            if verbose: print(f'Y = {r}, X = {c}, P Values = {p_values}')  
            for i in range(0,len(p_values)):
                if i == len(p_values)-1:
                    min_p_value = f'{np.min(p_values)}_{np.argmin(p_values)+1}'
                if p_values[i] <= nivel_sig:
                    break
            min_p_value = f'{p_values[i]}_{i+1}'
            df.loc[r, c] = min_p_value
    df.columns = [var + '_x' for var in variables]
    df.index = [var + '_y' for var in variables]
    causation_dict = {}
    for c in variables:
        if c != target_column:
            causation_dict[c] = {}
            test_result = grangercausalitytests(data[[target_column, c]], maxlag=maxlag, verbose=False)
            p_values = [round(test_result[i+1][0][test][1], 4) for i in range(maxlag)]
            
            for i in range(len(p_values)):
                if p_values[i] <= nivel_sig:
                    causation_dict[c] = i+1
                    break
                        
 
    return df, causation_dict #df.to_excel('GargerCausalityVolumen.xlsx', engine='xlsxwriter')

