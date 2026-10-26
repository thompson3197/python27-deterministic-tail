# -*- coding: utf-8 -*-
"""
Coding Challenge #141: Step 8 - Follow Mode (-f / --follow) File Polling Harness
Python 2.7 Compliant Script with Strict Ground Rule Compliance
"""
import sys                                  # Import sys module for stream redirection
import os                                   # Import os module for path checking
import time                                 # Import time module for simulated polling delay

MAX_LOOP_LIMIT = 1000                       # Constant: Fixed upper bound for loop limits (Rule #6)
DEFAULT_POLL_CYCLES = 3                     # Constant: Default number of simulation poll cycles (Rule #7)

def validate_follow_parameters(file_path, poll_cycles):
    # Function to validate follow mode input parameters
    assert isinstance(file_path, str), "File path must be a string"              # Assertion 1: Validate input type (Rule #9, #11)
    assert isinstance(poll_cycles, int), "Poll cycles must be an integer"       # Assertion 2: Validate input type (Rule #9, #11)
    assert poll_cycles >= 1, "Poll cycles must be at least 1"                   # Assertion 3: Validate numeric bounds (Rule #9, #11)
    return True                                 # Return validation success status

def simulate_file_polling(file_path, poll_cycles):
    # Function to simulate continuous file polling and incremental line reading for follow mode
    assert isinstance(file_path, str), "File path must be a string"              # Assertion 1: Validate input type (Rule #9, #11)
    assert isinstance(poll_cycles, int), "Poll cycles must be an integer"       # Assertion 2: Validate input type (Rule #9, #11)
    
    appended_output_list = []               # Initialize output container list (Rule #7, #10)
    file_handle = open(file_path, "r+")     # Open target file in read/write mode (Rule #11)
    try:
        file_handle.seek(0, 2)              # Seek to the end of the file to establish initial baseline
        last_position = file_handle.tell()  # Record initial byte offset position
        
        cycle_idx = 0                       # Initialize poll cycle iteration index variable (Rule #10)
        while cycle_idx < poll_cycles and cycle_idx < MAX_LOOP_LIMIT: # Bounded loop execution (Rule #6)
            time.sleep(0.1)                 # Pause briefly to simulate polling interval delay
            
            # Simulate external process appending a new line to the file
            file_handle.seek(0, 2)          # Seek to end of file before appending
            new_line_text = "Follow Appended Line %d\n" % (cycle_idx + 1) # Construct new line string
            file_handle.write(new_line_text) # Write new line to file stream
            file_handle.flush()             # Force flush buffer to ensure data is written to disk
            
            file_handle.seek(last_position, 0) # Seek back to last recorded read position
            new_data_chunk = file_handle.read() # Read all newly appended data from stream
            if len(new_data_chunk) > 0:     # Check if new data was successfully read
                appended_output_list.append(new_data_chunk) # Append new data chunk to result list
                last_position = file_handle.tell() # Update last recorded byte offset position
                
            cycle_idx += 1                  # Increment poll cycle iteration index variable
            
        assert cycle_idx == poll_cycles, "Poll cycles did not complete expected iterations" # Assertion check on completion (Rule #9)
    finally:
        file_handle.close()                 # Ensure file handle is closed securely
        
    assert isinstance(appended_output_list, list), "Output must be a list"      # Assertion 3: Validate return type (Rule #11)
    return appended_output_list             # Return list of polled output chunks

def run_step8_harness():
    # Main orchestration function for Step 8 execution and logging
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Retrieve absolute directory path of script (Rule #11)
    output_filename = os.path.join(script_dir, "tail_step8_output.txt") # Define absolute path for log output (Rule #2, #4)
    sample_filename = os.path.join(script_dir, "test_sample_step8.txt") # Define absolute path for sample test file
    
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
        print "=== CODING CHALLENGE #141: STEP 8 INITIALIZED ===" # Trace statement start marker (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer to disk
        
        # Create initial baseline sample test file
        sample_file_handle = open(sample_filename, "w") # Open sample test file for writing
        try:
            sample_file_handle.write("Initial Baseline Line 1\n") # Write baseline content line
        finally:
            sample_file_handle.close()      # Ensure sample file handle is closed securely
            
        print "TRACE: Sample baseline test file created at %s" % sample_filename # Trace file creation step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        param_validation = validate_follow_parameters(sample_filename, DEFAULT_POLL_CYCLES) # Validate follow parameters
        print "TRACE: Follow parameter validation status: %s" % str(param_validation) # Trace validation step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        assert param_validation == True, "Follow parameter validation failed" # Assertion check on validation (Rule #9)
        
        polled_results = simulate_file_polling(sample_filename, DEFAULT_POLL_CYCLES) # Execute follow mode polling simulation
        print "TRACE: Successfully polled %d incremental updates in follow mode" % len(polled_results) # Trace polling step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        print "--- FOLLOW MODE OUTPUT RESULTS (-f) ---" # Print header for follow output section
        print_idx = 0                       # Initialize print iteration index (Rule #10)
        while print_idx < len(polled_results) and print_idx < MAX_LOOP_LIMIT: # Bounded loop for printing results (Rule #6)
            sys.stdout.write(polled_results[print_idx]) # Write each polled chunk directly to output stream
            print_idx += 1                  # Increment print iteration index variable
            
        print "=== STEP 8 EXECUTION COMPLETED SUCCESSFULLY ===" # Trace success completion marker (Rule #3)
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
    execution_result = run_step8_harness()  # Execute main harness orchestration function
    assert execution_result == True, "Main execution harness failed" # Final return assertion check (Rule #11)
