# -*- coding: utf-8 -*-
"""
Coding Challenge #141: Step 12 - Standard Input (stdin / -) Stream Processing
Python 2.7 Compliant Script with Strict Ground Rule Compliance
"""
import sys                                  # Import sys module for stream and stdin handling
import os                                   # Import os module for path checking
from StringIO import StringIO               # Import StringIO module to simulate stdin stream safely

MAX_LOOP_LIMIT = 1000                       # Constant: Fixed upper bound for loop limits (Rule #6)
DEFAULT_LINE_COUNT = 3                      # Constant: Default fallback line count (Rule #7)

def read_stream_lines(input_stream):
    # Function to read all lines from a given input stream into a list securely
    assert input_stream is not None, "Input stream cannot be None"             # Assertion 1: Validate stream existence (Rule #9, #11)
    assert hasattr(input_stream, "readline"), "Stream must support readline"    # Assertion 2: Validate stream capability (Rule #9, #11)
    
    stream_lines_list = []                  # Initialize static lines storage list (Rule #7, #10)
    read_counter = 0                        # Initialize read loop counter variable (Rule #10)
    line_item = input_stream.readline()     # Read first line from stream handle
    
    while line_item and read_counter < MAX_LOOP_LIMIT: # Bounded loop with fixed upper limit (Rule #6)
        stream_lines_list.append(line_item) # Append read line to storage list
        read_counter += 1                   # Increment read loop counter variable
        line_item = input_stream.readline() # Read next line from stream handle
        
    assert read_counter < MAX_LOOP_LIMIT, "Stream read exceeded maximum loop bounds" # Assertion check on loop completion (Rule #9)
    assert isinstance(stream_lines_list, list), "Storage list must be of type list" # Assertion 3: Validate return type (Rule #11)
    return stream_lines_list                # Return populated lines list

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

def run_step12_harness():
    # Main orchestration function for Step 12 execution and logging
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Retrieve absolute directory path of script (Rule #11)
    output_filename = os.path.join(script_dir, "tail_step12_output.txt") # Define absolute path for log output (Rule #2, #4)
    
    try:
        log_handle = open(output_filename, "w") # Open output file for logging streams (Rule #7)
    except IOError, io_err:
        sys.stderr.write("FATAL: Could not open output file at %s: %s\n" % (output_filename, str(io_err))) # Write to stderr on failure
        return False                        # Return failure status code
        
    original_stdout = sys.stdout            # Save reference to original standard output stream
    original_stderr = sys.stderr            # Save reference to original standard error stream
    original_stdin = sys.stdin              # Save reference to original standard input stream
    
    sys.stdout = log_handle                 # Redirect standard output stream to log file (Rule #2, #4)
    sys.stderr = log_handle                 # Redirect standard error stream to log file (Rule #2, #4)
    
    try:
        print "=== CODING CHALLENGE #141: STEP 12 INITIALIZED ===" # Trace statement start marker (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer to disk
        
        # Simulate standard input stream (stdin) using StringIO buffer containing 6 lines
        simulated_stdin_data = "Stdin Stream Line 1\nStdin Stream Line 2\nStdin Stream Line 3\nStdin Stream Line 4\nStdin Stream Line 5\nStdin Stream Line 6\n"
        simulated_stdin_handle = StringIO(simulated_stdin_data) # Create StringIO stream mock
        sys.stdin = simulated_stdin_handle  # Assign mock stream to sys.stdin
        
        print "TRACE: Simulated stdin stream established successfully" # Trace simulation step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        stream_lines = read_stream_lines(sys.stdin) # Read all lines from standard input stream
        print "TRACE: Read %d lines from stdin stream successfully" % len(stream_lines) # Trace read step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        tail_results = extract_last_n_lines(stream_lines, DEFAULT_LINE_COUNT) # Extract last 3 lines from stdin stream
        print "TRACE: Extracted last %d lines from stdin stream successfully" % len(tail_results) # Trace extraction step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        print "--- STDIN TAIL OUTPUT RESULTS (-) ---" # Print header for stdin output section
        print_idx = 0                       # Initialize print iteration index (Rule #10)
        while print_idx < len(tail_results) and print_idx < MAX_LOOP_LIMIT: # Bounded loop for printing results (Rule #6)
            sys.stdout.write(tail_results[print_idx]) # Write each tail line directly to output stream
            print_idx += 1                  # Increment print iteration index variable
            
        print "=== STEP 12 EXECUTION COMPLETED SUCCESSFULLY ===" # Trace success completion marker (Rule #3)
        sys.stdout.flush()                  # Force final flush of output stream
        return True                         # Return success status code
        
    except Exception, err_inst:
        sys.stdout = original_stdout        # Restore original stdout stream temporarily for error output
        sys.stderr = original_stderr        # Restore original stderr stream temporarily
        print "CRITICAL ERROR: Exception caught during execution: %s" % str(err_inst) # Log exception details
        return False                        # Return failure status code
        
    finally:
        sys.stdin = original_stdin          # Ensure standard input stream is fully restored
        sys.stdout = original_stdout        # Ensure standard output stream is fully restored
        sys.stderr = original_stderr        # Ensure standard error stream is fully restored
        log_handle.close()                  # Ensure log file handle is closed securely

if __name__ == "__main__":
    execution_result = run_step12_harness() # Execute main harness orchestration function
    assert execution_result == True, "Main execution harness failed" # Final return assertion check (Rule #11)
