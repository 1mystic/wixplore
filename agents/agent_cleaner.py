#!/usr/bin/env python3
"""
Data Cleaning Agent
Handles data preprocessing, cleaning, and standardization
"""

import sys
import json
import pandas as pd
import numpy as np
from pathlib import Path

def clean_data(file_path, parameters=None):
    """
    Clean and preprocess the uploaded data file
    
    Args:
        file_path (str): Path to the data file
        parameters (dict): Optional cleaning parameters
    
    Returns:
        dict: Cleaning results and statistics
    """
    try:
        # Default parameters
        default_params = {
            'remove_duplicates': True,
            'handle_missing': 'drop',  # 'drop', 'fill', 'interpolate'
            'normalize_text': True,
            'remove_outliers': False
        }
        
        if parameters:
            default_params.update(parameters)
        
        # Determine file type and read data
        file_path = Path(file_path)
        
        if file_path.suffix.lower() == '.csv':
            df = pd.read_csv(file_path)
        elif file_path.suffix.lower() == '.json':
            df = pd.read_json(file_path)
        elif file_path.suffix.lower() in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")
        
        # Store original stats
        original_shape = df.shape
        original_missing = df.isnull().sum().sum()
        
        # Cleaning operations
        cleaned_df = df.copy()
        
        # Remove duplicates
        if default_params['remove_duplicates']:
            cleaned_df = cleaned_df.drop_duplicates()
        
        # Handle missing values
        if default_params['handle_missing'] == 'drop':
            cleaned_df = cleaned_df.dropna()
        elif default_params['handle_missing'] == 'fill':
            # Fill numeric columns with mean, categorical with mode
            for col in cleaned_df.columns:
                if cleaned_df[col].dtype in ['int64', 'float64']:
                    cleaned_df[col].fillna(cleaned_df[col].mean(), inplace=True)
                else:
                    cleaned_df[col].fillna(cleaned_df[col].mode()[0] if not cleaned_df[col].mode().empty else 'Unknown', inplace=True)
        
        # Normalize text columns
        if default_params['normalize_text']:
            text_cols = cleaned_df.select_dtypes(include=['object']).columns
            for col in text_cols:
                cleaned_df[col] = cleaned_df[col].astype(str).str.strip().str.lower()
        
        # Save cleaned data
        output_path = file_path.parent / f"cleaned_{file_path.name}"
        if file_path.suffix.lower() == '.csv':
            cleaned_df.to_csv(output_path, index=False)
        elif file_path.suffix.lower() == '.json':
            cleaned_df.to_json(output_path, orient='records', indent=2)
        
        # Return results
        result = {
            'status': 'success',
            'original_shape': original_shape,
            'cleaned_shape': cleaned_df.shape,
            'rows_removed': original_shape[0] - cleaned_df.shape[0],
            'missing_values_original': int(original_missing),
            'missing_values_cleaned': int(cleaned_df.isnull().sum().sum()),
            'output_file': str(output_path),
            'parameters_used': default_params,
            'data_types': cleaned_df.dtypes.to_dict(),
            'summary_stats': cleaned_df.describe().to_dict() if not cleaned_df.empty else {}
        }
        
        return result
        
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'traceback': str(e.__class__.__name__)
        }

def main():
    if len(sys.argv) < 2:
        print(json.dumps({'error': 'File path required'}))
        sys.exit(1)
    
    file_path = sys.argv[1]
    parameters = {}
    
    if len(sys.argv) > 2:
        try:
            parameters = json.loads(sys.argv[2])
        except json.JSONDecodeError:
            pass
    
    result = clean_data(file_path, parameters)
    print(json.dumps(result, default=str))

if __name__ == '__main__':
    main()
