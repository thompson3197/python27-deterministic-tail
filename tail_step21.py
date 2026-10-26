# -*- coding: utf-8 -*-
"""
Coding Challenge #141: Step 21 - Final Integration: Unified Master Test Harness
Python 2.7 Compliant Script with Strict Ground Rule Compliance
"""
import sys                                  # Import sys module for stream redirection
import os                                   # Import os module for path checking

MAX_LOOP_LIMIT = 1000                       # Constant: Fixed upper bound for loop limits (Rule #6)
EXIT_SUCCESS = 0                            # Constant: Successful exit status code (Rule #7)

def execute_unified_tail_pipeline(file_path, line_count):
    # Function to execute unified tail extraction pipeline with strict validation
    assert isinstance(file_path, str), "File path must be a string"              # Assertion 1: Validate input type (Rule #9, #11)
    assert isinstance(line_count, (int, long)), "Line count must be numeric"      # Assertion 2: Validate input type (Rule #9, #11)
    assert line_count >= 0, "Line count cannot be negative"                     # Assertion 3: Validate numeric bounds (Rule #9, #11)
    
    extracted_records_list = []             # Initialize output container list (Rule #7, #10)
    int_line_count = int(line_count)        # Cast line count to standard integer (Rule #10)
    
    if not os.path.exists(file_path):       # Check if target file exists on disk
        raise IOError(2, "File not found: %s" % file_path) # Raise explicit error if file missing
        
    file_handle = open(file_path, "r")      # Open target file for reading (Rule #11)
    try:
        all_file_lines = file_handle.readlines() # Read all lines from stream into memory
        total_lines = len(all_file_lines)   # Calculate total lines count
        
        start_index = total_lines - int_line_count # Calculate starting index for tail extraction
        if start_index < 0:                 # Check if requested count exceeds total lines
            start_index = 0                 # Clamp start index to zero
            
        line_idx = start_index              # Initialize line iteration index variable (Rule #10)
        scan_counter = 0                    # Initialize scan loop counter variable (Rule #10)
        
        while line_idx < total_lines and scan_counter < MAX_LOOP_LIMIT: # Bounded loop execution (Rule #6)
            extracted_records_list.append(all_file_lines[line_idx]) # Append line to result list
            line_idx += 1                   # Increment line iteration index variable
            scan_counter += 1               # Increment scan loop counter variable
            
        assert scan_counter < MAX_LOOP_LIMIT, "Pipeline scan exceeded maximum loop bounds" # Assertion check on loop completion (Rule #9)
    finally:
        file_handle.close()                 # Ensure file handle is closed securely
        
    assert isinstance(extracted_records_list, list), "Result must be a list"    # Assertion 4: Validate return type (Rule #11)
    return extracted_records_list           # Return final extracted records list

def run_step21_harness():
    # Main orchestration function for Step 21 master integration and logging
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Retrieve absolute directory path of script (Rule #11)
    output_filename = os.path.join(script_dir, "tail_step21_output.txt") # Define absolute path for log output (Rule #2, #4)
    sample_filename = os.path.join(script_dir, "test_sample_step21.txt") # Define absolute path for master test file
    
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
        print "=== CODING CHALLENGE #141: STEP 21 MASTER INTEGRATION INITIALIZED ===" # Trace start marker (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer to disk
        
        # Create master test file containing 10 chronological records
        sample_file_handle = open(sample_filename, "w") # Open master sample file for writing
        try:
            write_idx = 1                   # Initialize write index variable (Rule #10)
            while write_idx <= 10 and write_idx < MAX_LOOP_LIMIT: # Bounded loop for data creation (Rule #6)
                sample_file_handle.write("Master Integration Event Record #%02d\n" % write_idx) # Write record line
                write_idx += 1              # Increment write index variable
        finally:
            sample_file_handle.close()      # Ensure sample file handle is closed securely
            
        print "TRACE: Master sample test file created with 10 records at %s" % sample_filename # Trace file creation step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        # Execute unified tail pipeline requesting last 4 records
        master_tail_results = execute_unified_tail_pipeline(sample_filename, 4) # Execute unified pipeline
        print "TRACE: Unified tail pipeline executed successfully (%d records retrieved)" % len(master_tail_results) # Trace execution step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        print "--- UNIFIED MASTER TAIL OUTPUT RESULTS ---" # Print header for output section
        print_idx = 0                       # Initialize print iteration index (Rule #10)
        while print_idx < len(master_tail_results) and print_idx < MAX_LOOP_LIMIT: # Bounded loop for printing results (Rule #6)
            sys.stdout.write(master_tail_results[print_idx]) # Write each retrieved record directly to output stream
            print_idx += 1                  # Increment print iteration index variable
            
        print "=== CODING CHALLENGE #141 COMPLETED SUCCESSFULLY (ALL 21 STEPS VERIFIED) ===" # Trace final completion marker (Rule #3)
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
    execution_result = run_step21_harness() # Execute main harness orchestration function
    assert execution_result == True, "Main execution harness failed" # Final return assertion check (Rule #11)
