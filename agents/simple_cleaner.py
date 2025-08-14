#!/usr/bin/env python3
"""
Simple Data Cleaner Agent (No Dependencies Version)
Handles basic data processing without external libraries
"""

import sys
import json
import csv
from pathlib import Path

def clean_data_simple(file_path, parameters=None):
    """
    Simple data cleaning without pandas
    """
    try:
        file_path = Path(file_path)
        
        if not file_path.exists():
            return {'status': 'error', 'error': 'File not found'}
        
        if file_path.suffix.lower() != '.csv':
            return {'status': 'error', 'error': 'Only CSV files supported in simple mode'}
        
        # Read CSV data
        rows = []
        headers = []
        
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader, [])
            for row in reader:
                if any(cell.strip() for cell in row):  # Skip empty rows
                    rows.append(row)
        
        # Basic cleaning
        original_count = len(rows)
        
        # Remove duplicates (simple string comparison)
        unique_rows = []
        seen = set()
        for row in rows:
            row_str = ','.join(row)
            if row_str not in seen:
                seen.add(row_str)
                unique_rows.append(row)
        
        cleaned_count = len(unique_rows)
        duplicates_removed = original_count - cleaned_count
        
        # Save cleaned data
        output_path = file_path.parent / f"cleaned_{file_path.name}"
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            writer.writerows(unique_rows)
        
        result = {
            'status': 'success',
            'original_rows': original_count,
            'cleaned_rows': cleaned_count,
            'duplicates_removed': duplicates_removed,
            'output_file': str(output_path),
            'headers': headers,
            'sample_data': unique_rows[:3] if unique_rows else [],
            'agent_version': 'simple_cleaner_v1.0'
        }
        
        return result
        
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'agent_version': 'simple_cleaner_v1.0'
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
    
    result = clean_data_simple(file_path, parameters)
    print(json.dumps(result, default=str))

if __name__ == '__main__':
    main()
