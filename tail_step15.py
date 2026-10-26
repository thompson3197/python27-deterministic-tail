# -*- coding: utf-8 -*-
"""
Coding Challenge #141: Step 15 - Advanced Extension 2: Inverted Line Matching (--exclude)
Python 2.7 Compliant Script with Strict Ground Rule Compliance
"""
import sys                                  # Import sys module for stream redirection
import os                                   # Import os module for path checking

MAX_LOOP_LIMIT = 1000                       # Constant: Fixed upper bound for loop limits (Rule #6)
DEFAULT_EXCLUDE_PATTERN = "DEBUG"           # Constant: Default fallback exclusion pattern (Rule #7)

def parse_exclude_argument(arg_list):
    # Function to parse exclusion pattern string from argument list (--exclude flag)
    assert isinstance(arg_list, list), "Argument list must be a list"           # Assertion 1: Validate input type (Rule #9, #11)
    assert len(arg_list) < MAX_LOOP_LIMIT, "Argument list exceeds maximum bounds" # Assertion 2: Validate size bounds (Rule #9, #11)
    
    exclude_pattern = DEFAULT_EXCLUDE_PATTERN # Initialize pattern string with default (Rule #10)
    arg_idx = 0                             # Initialize argument iteration index variable (Rule #10)
    
    while arg_idx < len(arg_list) and arg_idx < MAX_LOOP_LIMIT: # Bounded loop execution (Rule #6)
        current_arg = arg_list[arg_idx]     # Retrieve current argument string from list
        if current_arg == "-x" or current_arg == "--exclude": # Check for exclusion flag identifier
            assert arg_idx + 1 < len(arg_list), "Missing value following exclude flag" # Assertion check for value existence (Rule #9, #11)
            exclude_pattern = arg_list[arg_idx + 1] # Retrieve exclusion pattern string argument
            break                           # Exit loop once flag and value are processed
        arg_idx += 1                        # Increment argument iteration index variable
        
    assert isinstance(exclude_pattern, str), "Exclude pattern must evaluate to a string" # Assertion 3: Validate return type (Rule #11)
    assert len(exclude_pattern) > 0, "Exclude pattern cannot be empty"            # Assertion 4: Validate pattern length (Rule #9, #11)
    return exclude_pattern                  # Return validated exclusion pattern string

def exclude_lines_by_pattern(lines_list, pattern_str):
    # Function to filter a list of lines, excluding any that contain the target pattern
    assert isinstance(lines_list, list), "Lines parameter must be a list"         # Assertion 1: Validate input type (Rule #9, #11)
    assert isinstance(pattern_str, str), "Pattern parameter must be a string"     # Assertion 2: Validate input type (Rule #9, #11)
    
    filtered_results_list = []              # Initialize filtered results container list (Rule #7, #10)
    line_idx = 0                            # Initialize line iteration index variable (Rule #10)
    total_lines = len(lines_list)           # Calculate total lines count in input list
    retained_counter = 0                    # Initialize retained line counter variable (Rule #10)
    
    while line_idx < total_lines and retained_counter < MAX_LOOP_LIMIT: # Bounded loop execution (Rule #6)
        current_line = lines_list[line_idx] # Retrieve current line string from list
        if pattern_str not in current_line: # Check that target pattern does NOT exist within line
            filtered_results_list.append(current_line) # Append non-matching line to result list
            retained_counter += 1           # Increment retained line counter variable
        line_idx += 1                       # Increment line iteration index variable
        
    assert len(filtered_results_list) <= total_lines, "Filtered count cannot exceed total lines" # Assertion 3: Validate size bounds (Rule #9)
    assert isinstance(filtered_results_list, list), "Result must be a list"     # Assertion 4: Validate return type (Rule #11)
    return filtered_results_list            # Return filtered non-matching lines list

def run_step15_harness():
    # Main orchestration function for Step 15 execution and logging
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Retrieve absolute directory path of script (Rule #11)
    output_filename = os.path.join(script_dir, "tail_step15_output.txt") # Define absolute path for log output (Rule #2, #4)
    sample_filename = os.path.join(script_dir, "test_sample_step15.txt") # Define absolute path for sample test file
    
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
        print "=== CODING CHALLENGE #141: STEP 15 INITIALIZED (ADVANCED EXTENSION 2) ===" # Trace statement start marker (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer to disk
        
        # Create sample test file containing mixed log entries including DEBUG noise
        sample_file_handle = open(sample_filename, "w") # Open sample test file for writing
        try:
            sample_file_handle.write("INFO: Application boot initialized\n")
            sample_file_handle.write("DEBUG: Verbose memory state dump line 1\n")
            sample_file_handle.write("WARNING: High CPU utilization observed\n")
            sample_file_handle.write("DEBUG: Verbose memory state dump line 2\n")
            sample_file_handle.write("ERROR: Failed database ping response\n")
        finally:
            sample_file_handle.close()      # Ensure sample file handle is closed securely
            
        print "TRACE: Sample log test file created at %s" % sample_filename # Trace file creation step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        # Simulate command-line arguments requesting exclusion of 'DEBUG' pattern via --exclude flag
        simulated_args = ["tail.py", "--exclude", "DEBUG"] # Define simulated argument list with flag and value
        parsed_exclude = parse_exclude_argument(simulated_args) # Parse exclusion pattern string from arguments
        print "TRACE: Parsed exclusion pattern from arguments: '%s'" % parsed_exclude # Trace parse step (Rule #3)
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
            
        excluded_results = exclude_lines_by_pattern(file_lines, parsed_exclude) # Exclude lines matching pattern
        print "TRACE: Excluded matching lines successfully (%d lines retained)" % len(excluded_results) # Trace filtering step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        print "--- INVERTED MATCHING OUTPUT RESULTS (--exclude DEBUG) ---" # Print header for output section
        print_idx = 0                       # Initialize print iteration index (Rule #10)
        while print_idx < len(excluded_results) and print_idx < MAX_LOOP_LIMIT: # Bounded loop for printing results (Rule #6)
            sys.stdout.write(excluded_results[print_idx]) # Write each retained line directly to output stream
            print_idx += 1                  # Increment print iteration index variable
            
        print "=== STEP 15 EXECUTION COMPLETED SUCCESSFULLY ===" # Trace success completion marker (Rule #3)
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
    execution_result = run_step15_harness() # Execute main harness orchestration function
    assert execution_result == True, "Main execution harness failed" # Final return assertion check (Rule #11)
