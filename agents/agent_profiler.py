#!/usr/bin/env python3
"""
Data Profiling Agent
Analyzes data structure, quality, and characteristics
"""

import sys
import json
import pandas as pd
import numpy as np
from pathlib import Path
from collections import Counter

def profile_data(file_path, parameters=None):
    """
    Generate comprehensive data profile
    
    Args:
        file_path (str): Path to the data file
        parameters (dict): Optional profiling parameters
    
    Returns:
        dict: Data profiling results
    """
    try:
        # Default parameters
        default_params = {
            'include_correlations': True,
            'include_distributions': True,
            'sample_size': 1000,  # For large datasets
            'detect_patterns': True
        }
        
        if parameters:
            default_params.update(parameters)
        
        # Read data
        file_path = Path(file_path)
        
        if file_path.suffix.lower() == '.csv':
            df = pd.read_csv(file_path)
        elif file_path.suffix.lower() == '.json':
            df = pd.read_json(file_path)
        elif file_path.suffix.lower() in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")
        
        # Sample if dataset is too large
        if len(df) > default_params['sample_size']:
            df_sample = df.sample(n=default_params['sample_size'], random_state=42)
        else:
            df_sample = df
        
        # Basic information
        basic_info = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
            'file_size_mb': file_path.stat().st_size / 1024**2
        }
        
        # Column analysis
        column_analysis = {}
        for col in df.columns:
            col_data = df[col]
            col_info = {
                'data_type': str(col_data.dtype),
                'non_null_count': int(col_data.count()),
                'null_count': int(col_data.isnull().sum()),
                'null_percentage': float(col_data.isnull().sum() / len(col_data) * 100),
                'unique_count': int(col_data.nunique()),
                'unique_percentage': float(col_data.nunique() / len(col_data) * 100)
            }
            
            # Type-specific analysis
            if col_data.dtype in ['int64', 'float64']:
                col_info.update({
                    'min_value': float(col_data.min()) if not col_data.empty else None,
                    'max_value': float(col_data.max()) if not col_data.empty else None,
                    'mean': float(col_data.mean()) if not col_data.empty else None,
                    'median': float(col_data.median()) if not col_data.empty else None,
                    'std_dev': float(col_data.std()) if not col_data.empty else None,
                    'outliers_count': len(col_data[(np.abs(col_data - col_data.mean()) > 2 * col_data.std())]) if col_data.std() > 0 else 0
                })
            elif col_data.dtype == 'object':
                # Text analysis
                value_counts = col_data.value_counts().head(10)
                col_info.update({
                    'top_values': value_counts.to_dict(),
                    'avg_length': float(col_data.astype(str).str.len().mean()) if not col_data.empty else 0,
                    'max_length': int(col_data.astype(str).str.len().max()) if not col_data.empty else 0
                })
            
            column_analysis[col] = col_info
        
        # Data quality assessment
        quality_score = 0
        quality_factors = []
        
        # Completeness (weight: 30%)
        completeness = (1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 30
        quality_score += completeness
        quality_factors.append({
            'factor': 'completeness',
            'score': completeness,
            'description': 'Percentage of non-missing values'
        })
        
        # Uniqueness (weight: 25%)
        duplicate_ratio = df.duplicated().sum() / len(df)
        uniqueness = (1 - duplicate_ratio) * 25
        quality_score += uniqueness
        quality_factors.append({
            'factor': 'uniqueness',
            'score': uniqueness,
            'description': 'Percentage of unique records'
        })
        
        # Consistency (weight: 25%)
        # Simple consistency check based on data types
        type_consistency = 25  # Placeholder - can be enhanced
        quality_score += type_consistency
        quality_factors.append({
            'factor': 'consistency',
            'score': type_consistency,
            'description': 'Data type and format consistency'
        })
        
        # Validity (weight: 20%)
        # Simple validity check
        validity = 20  # Placeholder - can be enhanced
        quality_score += validity
        quality_factors.append({
            'factor': 'validity',
            'score': validity,
            'description': 'Data validity and constraints adherence'
        })
        
        # Correlations (for numeric columns)
        correlations = {}
        if default_params['include_correlations']:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 1:
                corr_matrix = df[numeric_cols].corr()
                correlations = corr_matrix.to_dict()
        
        # Compile results
        result = {
            'status': 'success',
            'basic_info': basic_info,
            'column_analysis': column_analysis,
            'data_quality': {
                'overall_score': round(quality_score, 2),
                'factors': quality_factors
            },
            'correlations': correlations,
            'recommendations': generate_recommendations(df, column_analysis),
            'profiling_parameters': default_params
        }
        
        return result
        
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'traceback': str(e.__class__.__name__)
        }

def generate_recommendations(df, column_analysis):
    """Generate data improvement recommendations"""
    recommendations = []
    
    # High null percentage columns
    for col, analysis in column_analysis.items():
        if analysis['null_percentage'] > 50:
            recommendations.append(f"Column '{col}' has {analysis['null_percentage']:.1f}% missing values - consider removal or imputation")
    
    # Low uniqueness columns
    for col, analysis in column_analysis.items():
        if analysis['unique_percentage'] < 1 and analysis['unique_count'] > 1:
            recommendations.append(f"Column '{col}' has very low uniqueness - might be categorical")
    
    # Potential identifier columns
    for col, analysis in column_analysis.items():
        if analysis['unique_percentage'] > 95:
            recommendations.append(f"Column '{col}' appears to be an identifier (high uniqueness)")
    
    return recommendations

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
    
    result = profile_data(file_path, parameters)
    print(json.dumps(result, default=str))

if __name__ == '__main__':
    main()
