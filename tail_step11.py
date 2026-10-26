# -*- coding: utf-8 -*-
"""
Coding Challenge #141: Step 11 - Binary File Handling & Line Ending Normalization
Python 2.7 Compliant Script with Strict Ground Rule Compliance
"""
import sys                                  # Import sys module for stream redirection
import os                                   # Import os module for path checking

MAX_LOOP_LIMIT = 1000                       # Constant: Fixed upper bound for loop limits (Rule #6)
DEFAULT_LINE_COUNT = 3                      # Constant: Default fallback line count (Rule #7)

def normalize_line_endings(raw_binary_data):
    # Function to normalize diverse line endings (\r\n, \r, \n) into standard Unix (\n) lines
    assert isinstance(raw_binary_data, str), "Raw data must be a string"           # Assertion 1: Validate input type (Rule #9, #11)
    assert len(raw_binary_data) < MAX_LOOP_LIMIT * 10, "Raw data exceeds size bounds" # Assertion 2: Validate size bounds (Rule #9, #11)
    
    # Replace Windows CRLF (\r\n) with Unix LF (\n)
    step1_normalized = raw_binary_data.replace("\r\n", "\n") # Replace CRLF sequences
    # Replace remaining standalone classic Mac CR (\r) with Unix LF (\n)
    step2_normalized = step1_normalized.replace("\r", "\n") # Replace lone CR sequences
    
    normalized_lines_list = step2_normalized.splitlines(True) # Split normalized text into lines preserving delimiters
    
    assert isinstance(normalized_lines_list, list), "Normalized result must be a list" # Assertion 3: Validate return type (Rule #11)
    return normalized_lines_list            # Return normalized lines list

def extract_normalized_tail(file_path, target_count):
    # Function to read binary file, normalize line endings, and extract last N lines securely
    assert isinstance(file_path, str), "File path must be a string"              # Assertion 1: Validate input type (Rule #9, #11)
    assert isinstance(target_count, int), "Target count must be an integer"       # Assertion 2: Validate input type (Rule #9, #11)
    assert target_count >= 0, "Target count cannot be negative"                 # Assertion 3: Validate numeric bounds (Rule #9, #11)
    
    file_handle = open(file_path, "rb")     # Open target file in binary read mode (Rule #11)
    try:
        binary_content = file_handle.read() # Read entire binary content from stream
    finally:
        file_handle.close()                 # Ensure file handle is closed securely
        
    normalized_lines = normalize_line_endings(binary_content) # Normalize line endings
    total_lines = len(normalized_lines)     # Calculate total normalized line count
    
    start_index = total_lines - target_count # Calculate starting index for tail extraction
    if start_index < 0:                     # Check if requested count exceeds total lines
        start_index = 0                     # Clamp start index to zero if file is smaller than N
        
    extracted_tail_list = []                # Initialize output tail container list (Rule #7, #10)
    line_idx = start_index                  # Initialize line iteration index variable (Rule #10)
    extraction_counter = 0                  # Initialize extraction counter variable (Rule #10)
    
    while line_idx < total_lines and extraction_counter < MAX_LOOP_LIMIT: # Bounded loop execution (Rule #6)
        extracted_tail_list.append(normalized_lines[line_idx]) # Append line to result list
        line_idx += 1                       # Increment line iteration index variable
        extraction_counter += 1             # Increment extraction counter variable
        
    assert isinstance(extracted_tail_list, list), "Tail result must be a list"  # Assertion 4: Validate return type (Rule #11)
    return extracted_tail_list              # Return final extracted tail lines list

def run_step11_harness():
    # Main orchestration function for Step 11 execution and logging
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Retrieve absolute directory path of script (Rule #11)
    output_filename = os.path.join(script_dir, "tail_step11_output.txt") # Define absolute path for log output (Rule #2, #4)
    sample_filename = os.path.join(script_dir, "test_sample_step11.bin") # Define absolute path for binary sample test file
    
    try:
        log_handle = open(output_filename, "w") # Open output file for logging streams (Rule #7)
    except IOError, io_err:
        sys.stderr.write("FATAL: Could not open output file at %s: %s\n" % (output_filename, str(io_err))) # Write to stderr on failure
        return False                        # Return failure status code
        
    original_stdout = sys.stdout            # Save reference to original standard output stream
    original_stderr = sys.stderr            # Save reference to original standard error stream
    
    sys.stdout = log_handle                 # Redirect standard output stream to log file (Rule #2, #4)
    sys.stderr = log_handle                 # Redirect standard error stream to log file (Rule #2, #4)
    
    try:
        print "=== CODING CHALLENGE #141: STEP 11 INITIALIZED ===" # Trace statement start marker (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer to disk
        
        # Create a binary test file containing mixed line endings (\r\n, \r, \n)
        sample_file_handle = open(sample_filename, "wb") # Open binary sample file for writing
        try:
            mixed_binary_payload = "Binary Line 1 (CRLF)\r\nBinary Line 2 (LF)\nBinary Line 3 (CR)\rBinary Line 4 (Target 1)\r\nBinary Line 5 (Target 2)\n"
            sample_file_handle.write(mixed_binary_payload) # Write mixed line-ending payload
        finally:
            sample_file_handle.close()      # Ensure sample file handle is closed securely
            
        print "TRACE: Binary sample test file created with mixed line endings at %s" % sample_filename # Trace file creation step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        tail_results = extract_normalized_tail(sample_filename, DEFAULT_LINE_COUNT) # Extract normalized tail lines
        print "TRACE: Successfully extracted normalized tail (%d lines)" % len(tail_results) # Trace extraction step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        print "--- BINARY NORMALIZED TAIL OUTPUT RESULTS ---" # Print header for output section
        print_idx = 0                       # Initialize print iteration index (Rule #10)
        while print_idx < len(tail_results) and print_idx < MAX_LOOP_LIMIT: # Bounded loop for printing results (Rule #6)
            sys.stdout.write(tail_results[print_idx]) # Write each normalized line directly to output stream
            print_idx += 1                  # Increment print iteration index variable
            
        print "=== STEP 11 EXECUTION COMPLETED SUCCESSFULLY ===" # Trace success completion marker (Rule #3)
        sys.stdout.flush()                  # Force final flush of output stream
        return True                         # Return success status code
        
    except Exception, err_inst:
        sys.stdout = original_stdout        # Restore original stdout stream temporarily for error output
        sys.stderr = original_stderr        # Restore original stderr stream temporarily
        print "CRITICAL ERROR: Exception caught during execution: %s" % str(err_inst) # Log exception details
        return False                        # Return failure status code
        
    finally:
        sys.stdout = original_stdout        # Ensure standard output stream is fully restored
        sys.stderr = original_stderr        # Ensure standard error stream is fully restored
        log_handle.close()                  # Ensure log file handle is closed securely

if __name__ == "__main__":
    execution_result = run_step11_harness() # Execute main harness orchestration function
    assert execution_result == True, "Main execution harness failed" # Final return assertion check (Rule #11)
