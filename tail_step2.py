# -*- coding: utf-8 -*-
"""
Coding Challenge #141: Step 2 - Custom Line Count via -n / --lines Flag
Python 2.7 Compliant Script with Strict Ground Rule Compliance
"""
import sys                                  # Import sys module for stream and argument handling
import os                                   # Import os module for path checking

MAX_LOOP_LIMIT = 1000                       # Constant: Fixed upper bound for loop limits (Rule #6)
DEFAULT_LINE_COUNT = 5                      # Constant: Default fallback line count (Rule #7)

def parse_line_argument(arg_list):
    # Function to parse custom line count from argument list simulating -n / --lines flags
    assert isinstance(arg_list, list), "Argument list must be a list"           # Assertion 1: Validate input type (Rule #9, #11)
    assert len(arg_list) < MAX_LOOP_LIMIT, "Argument list exceeds maximum bounds" # Assertion 2: Validate size bounds (Rule #9, #11)
    
    parsed_count = DEFAULT_LINE_COUNT       # Initialize parsed count with default value (Rule #10)
    arg_idx = 0                             # Initialize argument iteration index variable (Rule #10)
    
    while arg_idx < len(arg_list) and arg_idx < MAX_LOOP_LIMIT: # Bounded loop execution (Rule #6)
        current_arg = arg_list[arg_idx]     # Retrieve current argument string from list
        if current_arg == "-n" or current_arg == "--lines": # Check for line count flag identifier
            assert arg_idx + 1 < len(arg_list), "Missing value following line count flag" # Assertion check for flag value existence (Rule #9, #11)
            value_arg = arg_list[arg_idx + 1] # Retrieve value argument following the flag
            parsed_count = int(value_arg)   # Convert value string to integer line count
            break                           # Exit loop once flag and value are processed
        arg_idx += 1                        # Increment argument iteration index variable
        
    assert isinstance(parsed_count, int), "Parsed count must evaluate to an integer" # Assertion 3: Validate return type (Rule #11)
    assert parsed_count >= 0, "Parsed count cannot be negative"                 # Assertion 4: Validate numeric range (Rule #9, #11)
    return parsed_count                     # Return validated custom line count integer

def extract_last_n_lines(lines_list, target_count):
    # Function to extract the last N lines from a given list of lines
    assert isinstance(lines_list, list), "Lines parameter must be a list"         # Assertion 1: Validate input type (Rule #9, #11)
    assert isinstance(target_count, int), "Target count must be an integer"       # Assertion 2: Validate input type (Rule #9, #11)
    assert target_count >= 0, "Target count cannot be negative"                 # Assertion 3: Validate numeric bounds (Rule #9, #11)
    
    extracted_lines = []                    # Initialize output slice list (Rule #7, #10)
    total_lines = len(lines_list)           # Calculate total number of lines in input list
    
    start_index = total_lines - target_count # Calculate starting index for tail extraction
    if start_index < 0:                     # Check if requested count exceeds total lines
        start_index = 0                     # Clamp start index to zero if file is smaller than N
        
    loop_idx = start_index                  # Initialize iteration index variable (Rule #10)
    extraction_counter = 0                  # Initialize extraction counter variable (Rule #10)
    
    while loop_idx < total_lines and extraction_counter < MAX_LOOP_LIMIT: # Bounded loop execution (Rule #6)
        extracted_lines.append(lines_list[loop_idx]) # Append line to extracted result list
        loop_idx += 1                       # Increment iteration index variable
        extraction_counter += 1             # Increment extraction counter variable
        
    assert len(extracted_lines) <= total_lines, "Extracted lines exceed total lines" # Assertion check on slice size (Rule #9)
    return extracted_lines                  # Return final tail lines list

def run_step2_harness():
    # Main orchestration function for Step 2 execution and logging
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Retrieve absolute directory path of script (Rule #11)
    output_filename = os.path.join(script_dir, "tail_step2_output.txt") # Define absolute path for log output (Rule #2, #4)
    sample_filename = os.path.join(script_dir, "test_sample_step2.txt") # Define absolute path for sample test file
    
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
        print "=== CODING CHALLENGE #141: STEP 2 INITIALIZED ===" # Trace statement start marker (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer to disk
        
        # Create a sample test file containing 12 lines to verify custom tail extraction
        sample_file_handle = open(sample_filename, "w") # Open sample test file for writing
        try:
            sample_write_idx = 1            # Initialize sample write index variable (Rule #10)
            while sample_write_idx <= 12 and sample_write_idx < MAX_LOOP_LIMIT: # Bounded loop for test data creation (Rule #6)
                sample_file_handle.write("Custom Test Line %d\n" % sample_write_idx) # Write formatted test line
                sample_write_idx += 1       # Increment sample write index variable
        finally:
            sample_file_handle.close()      # Ensure sample file handle is closed securely
            
        print "TRACE: Sample test file created with 12 lines at %s" % sample_filename # Trace file creation step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        # Simulate command-line arguments requesting custom tail count of 4 lines via -n flag
        simulated_args = ["tail.py", "-n", "4"] # Define simulated argument list with flag and value
        custom_count = parse_line_argument(simulated_args) # Parse custom line count from arguments
        print "TRACE: Parsed custom line count from arguments: %d" % custom_count # Trace parse step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        # Read all lines from sample test file
        file_lines = []                     # Initialize file lines container list (Rule #7, #10)
        read_file_handle = open(sample_filename, "r") # Open sample test file for reading
        try:
            read_idx = 0                    # Initialize read index variable (Rule #10)
            line_val = read_file_handle.readline() # Read first line from file handle
            while line_val and read_idx < MAX_LOOP_LIMIT: # Bounded loop for reading file (Rule #6)
                file_lines.append(line_val) # Append line to list
                read_idx += 1               # Increment read index variable
                line_val = read_file_handle.readline() # Read next line
        finally:
            read_file_handle.close()        # Ensure read file handle is closed securely
            
        tail_results = extract_last_n_lines(file_lines, custom_count) # Extract custom last N lines
        print "TRACE: Extracted last %d lines successfully using custom argument" % len(tail_results) # Trace extraction step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        print "--- TAIL OUTPUT RESULTS (-n 4) ---" # Print header for tail output section
        print_idx = 0                       # Initialize print iteration index (Rule #10)
        while print_idx < len(tail_results) and print_idx < MAX_LOOP_LIMIT: # Bounded loop for printing results (Rule #6)
            sys.stdout.write(tail_results[print_idx]) # Write each tail line directly to output stream
            print_idx += 1                  # Increment print iteration index variable
            
        print "=== STEP 2 EXECUTION COMPLETED SUCCESSFULLY ===" # Trace success completion marker (Rule #3)
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
    execution_result = run_step2_harness()  # Execute main harness orchestration function
    assert execution_result == True, "Main execution harness failed" # Final return assertion check (Rule #11)
