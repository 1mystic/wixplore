#!/usr/bin/env python3
"""
Data Reasoning Agent
Provides insights, patterns, and reasoning about data using AI/ML techniques
"""

import sys
import json
import pandas as pd
import numpy as np
from pathlib import Path
from collections import defaultdict

def reason_about_data(file_path, parameters=None):
    """
    Analyze data and provide intelligent insights and reasoning
    
    Args:
        file_path (str): Path to the data file
        parameters (dict): Optional reasoning parameters
    
    Returns:
        dict: Reasoning results and insights
    """
    try:
        # Default parameters
        default_params = {
            'include_patterns': True,
            'include_anomalies': True,
            'include_predictions': False,
            'confidence_threshold': 0.7,
            'max_insights': 10
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
        
        insights = []
        patterns = []
        anomalies = []
        relationships = []
        
        # Pattern Detection
        if default_params['include_patterns']:
            patterns = detect_patterns(df)
            insights.extend([f"Pattern: {pattern}" for pattern in patterns])
        
        # Anomaly Detection
        if default_params['include_anomalies']:
            anomalies = detect_anomalies(df)
            insights.extend([f"Anomaly: {anomaly}" for anomaly in anomalies])
        
        # Relationship Analysis
        relationships = analyze_relationships(df)
        insights.extend([f"Relationship: {rel}" for rel in relationships])
        
        # Statistical Insights
        statistical_insights = generate_statistical_insights(df)
        insights.extend(statistical_insights)
        
        # Data Distribution Analysis
        distribution_analysis = analyze_distributions(df)
        
        # Trend Analysis (for time-series or sequential data)
        trend_analysis = analyze_trends(df)
        
        # Business Insights (domain-agnostic)
        business_insights = generate_business_insights(df)
        
        # Compile final insights (limit to max_insights)
        final_insights = insights[:default_params['max_insights']]
        
        result = {
            'status': 'success',
            'insights': final_insights,
            'patterns': patterns,
            'anomalies': anomalies,
            'relationships': relationships,
            'statistical_summary': generate_statistical_summary(df),
            'distribution_analysis': distribution_analysis,
            'trend_analysis': trend_analysis,
            'business_insights': business_insights,
            'reasoning_confidence': calculate_confidence(df, insights),
            'recommendations': generate_reasoning_recommendations(df, insights),
            'parameters_used': default_params
        }
        
        return result
        
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'traceback': str(e.__class__.__name__)
        }

def detect_patterns(df):
    """Detect patterns in the data"""
    patterns = []
    
    # Seasonal patterns (if date column exists)
    date_cols = df.select_dtypes(include=['datetime64']).columns
    if len(date_cols) > 0:
        patterns.append("Time-series data detected - potential for seasonal analysis")
    
    # Categorical patterns
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if df[col].nunique() < 10:  # Low cardinality
            value_counts = df[col].value_counts()
            if value_counts.iloc[0] / len(df) > 0.5:
                patterns.append(f"Column '{col}' is dominated by value '{value_counts.index[0]}'")
    
    # Numeric patterns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].std() == 0:
            patterns.append(f"Column '{col}' has constant values")
        elif df[col].skew() > 2:
            patterns.append(f"Column '{col}' is highly right-skewed")
        elif df[col].skew() < -2:
            patterns.append(f"Column '{col}' is highly left-skewed")
    
    return patterns

def detect_anomalies(df):
    """Detect anomalies in the data"""
    anomalies = []
    
    # Numeric anomalies using IQR method
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        if len(outliers) > 0:
            anomalies.append(f"Column '{col}' has {len(outliers)} outliers")
    
    # Missing value anomalies
    for col in df.columns:
        missing_pct = df[col].isnull().sum() / len(df) * 100
        if missing_pct > 30:
            anomalies.append(f"Column '{col}' has unusually high missing values ({missing_pct:.1f}%)")
    
    return anomalies

def analyze_relationships(df):
    """Analyze relationships between columns"""
    relationships = []
    
    # Numeric correlations
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr()
        
        # Find strong correlations
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                if abs(corr_val) > 0.7:
                    col1, col2 = corr_matrix.columns[i], corr_matrix.columns[j]
                    relationships.append(f"Strong correlation between '{col1}' and '{col2}' (r={corr_val:.2f})")
    
    return relationships

def generate_statistical_insights(df):
    """Generate statistical insights"""
    insights = []
    
    # Dataset size insights
    if len(df) > 100000:
        insights.append("Large dataset - suitable for machine learning applications")
    elif len(df) < 100:
        insights.append("Small dataset - statistical inference may be limited")
    
    # Feature richness
    if len(df.columns) > len(df):
        insights.append("More features than samples - potential for overfitting")
    
    # Data completeness
    completeness = (1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
    if completeness > 95:
        insights.append(f"High data completeness ({completeness:.1f}%) - good data quality")
    elif completeness < 70:
        insights.append(f"Low data completeness ({completeness:.1f}%) - data cleaning recommended")
    
    return insights

def analyze_distributions(df):
    """Analyze data distributions"""
    distribution_info = {}
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        col_data = df[col].dropna()
        if len(col_data) > 0:
            distribution_info[col] = {
                'distribution_type': 'normal' if abs(col_data.skew()) < 0.5 else 'skewed',
                'skewness': float(col_data.skew()),
                'kurtosis': float(col_data.kurtosis()),
                'range': float(col_data.max() - col_data.min()),
                'coefficient_of_variation': float(col_data.std() / col_data.mean()) if col_data.mean() != 0 else None
            }
    
    return distribution_info

def analyze_trends(df):
    """Analyze trends in data"""
    trends = {}
    
    # Look for sequential patterns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        col_data = df[col].dropna()
        if len(col_data) > 10:  # Minimum data points for trend analysis
            # Simple trend detection using linear regression slope
            x = np.arange(len(col_data))
            slope = np.polyfit(x, col_data, 1)[0]
            
            if abs(slope) > col_data.std() * 0.01:  # Significant trend
                trend_direction = 'increasing' if slope > 0 else 'decreasing'
                trends[col] = {
                    'direction': trend_direction,
                    'slope': float(slope),
                    'strength': 'strong' if abs(slope) > col_data.std() * 0.1 else 'weak'
                }
    
    return trends

def generate_business_insights(df):
    """Generate business-relevant insights"""
    insights = []
    
    # Data freshness insights
    date_cols = df.select_dtypes(include=['datetime64']).columns
    if len(date_cols) > 0:
        for col in date_cols:
            latest_date = df[col].max()
            insights.append(f"Latest date in '{col}': {latest_date}")
    
    # Key performance indicators
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        # Find potential KPI columns (those with high variability)
        for col in numeric_cols:
            cv = df[col].std() / df[col].mean() if df[col].mean() != 0 else 0
            if cv > 1:
                insights.append(f"'{col}' shows high variability - potential KPI")
    
    return insights

def generate_statistical_summary(df):
    """Generate comprehensive statistical summary"""
    summary = {
        'total_records': len(df),
        'total_features': len(df.columns),
        'numeric_features': len(df.select_dtypes(include=[np.number]).columns),
        'categorical_features': len(df.select_dtypes(include=['object']).columns),
        'datetime_features': len(df.select_dtypes(include=['datetime64']).columns),
        'missing_values_total': int(df.isnull().sum().sum()),
        'duplicate_records': int(df.duplicated().sum()),
        'memory_usage_mb': float(df.memory_usage(deep=True).sum() / 1024**2)
    }
    
    return summary

def calculate_confidence(df, insights):
    """Calculate confidence score for reasoning"""
    confidence_factors = []
    
    # Data size factor
    size_factor = min(len(df) / 1000, 1.0)  # Up to 1000 records = 100% confidence
    confidence_factors.append(size_factor * 0.3)
    
    # Data completeness factor
    completeness = 1 - df.isnull().sum().sum() / (len(df) * len(df.columns))
    confidence_factors.append(completeness * 0.3)
    
    # Feature richness factor
    feature_factor = min(len(df.columns) / 20, 1.0)  # Up to 20 features = 100% confidence
    confidence_factors.append(feature_factor * 0.2)
    
    # Insights quality factor
    insight_factor = min(len(insights) / 10, 1.0)  # Up to 10 insights = 100% confidence
    confidence_factors.append(insight_factor * 0.2)
    
    return round(sum(confidence_factors), 2)

def generate_reasoning_recommendations(df, insights):
    """Generate recommendations based on reasoning"""
    recommendations = []
    
    if len(insights) < 5:
        recommendations.append("Limited insights available - consider data enrichment")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 5:
        recommendations.append("Rich numeric data available - suitable for statistical modeling")
    
    categorical_cols = df.select_dtypes(include=['object']).columns
    if len(categorical_cols) > 3:
        recommendations.append("Multiple categorical features - consider encoding for ML")
    
    if df.isnull().sum().sum() > len(df) * 0.1:
        recommendations.append("Significant missing data - implement imputation strategy")
    
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
    
    result = reason_about_data(file_path, parameters)
    print(json.dumps(result, default=str))

if __name__ == '__main__':
    main()
