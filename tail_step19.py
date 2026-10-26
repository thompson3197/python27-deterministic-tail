# -*- coding: utf-8 -*-
"""
Coding Challenge #141: Step 19 - Advanced Extension 6: Multi-File Batch Processing & Headers
Python 2.7 Compliant Script with Strict Ground Rule Compliance
"""
import sys                                  # Import sys module for stream redirection
import os                                   # Import os module for path checking

MAX_LOOP_LIMIT = 1000                       # Constant: Fixed upper bound for loop limits (Rule #6)
DEFAULT_LINE_COUNT = 2                      # Constant: Default fallback line count (Rule #7)

def extract_simple_tail_lines(file_path, target_count):
    # Function to extract the last N lines from a specified file path
    assert isinstance(file_path, str), "File path must be a string"              # Assertion 1: Validate input type (Rule #9, #11)
    assert isinstance(target_count, (int, long)), "Target count must be numeric"  # Assertion 2: Validate input type (Rule #9, #11)
    assert target_count >= 0, "Target count cannot be negative"                 # Assertion 3: Validate numeric bounds (Rule #9, #11)
    
    extracted_lines_list = []               # Initialize output lines container list (Rule #7, #10)
    int_target_count = int(target_count)    # Cast target count to standard integer (Rule #10)
    
    file_handle = open(file_path, "r")      # Open target file for reading (Rule #11)
    try:
        file_lines_all = file_handle.readlines() # Read all lines from file handle into memory
        total_lines = len(file_lines_all)   # Calculate total line count
        
        start_idx = total_lines - int_target_count # Calculate starting index for tail slice
        if start_idx < 0:                   # Check if requested count exceeds total lines
            start_idx = 0                   # Clamp start index to zero
            
        line_idx = start_idx                # Initialize line iteration index variable (Rule #10)
        scan_counter = 0                    # Initialize scan loop counter variable (Rule #10)
        
        while line_idx < total_lines and scan_counter < MAX_LOOP_LIMIT: # Bounded loop execution (Rule #6)
            extracted_lines_list.append(file_lines_all[line_idx]) # Append line to result list
            line_idx += 1                   # Increment line iteration index variable
            scan_counter += 1               # Increment scan loop counter variable
            
        assert scan_counter < MAX_LOOP_LIMIT, "Tail extraction scan exceeded maximum loop bounds" # Assertion check on loop completion (Rule #9)
    finally:
        file_handle.close()                 # Ensure file handle is closed securely
        
    assert isinstance(extracted_lines_list, list), "Result must be a list"      # Assertion 4: Validate return type (Rule #11)
    return extracted_lines_list             # Return extracted tail lines list

def process_multi_file_batch(file_paths_list, target_count):
    # Function to process multiple files in batch, formatting output with standard headers
    assert isinstance(file_paths_list, list), "File paths list must be a list"   # Assertion 1: Validate input type (Rule #9, #11)
    assert isinstance(target_count, (int, long)), "Target count must be numeric"  # Assertion 2: Validate input type (Rule #9, #11)
    
    batch_output_list = []                  # Initialize batch output lines container list (Rule #7, #10)
    total_files = len(file_paths_list)      # Determine total number of files in batch
    file_idx = 0                            # Initialize file iteration index variable (Rule #10)
    
    while file_idx < total_files and file_idx < MAX_LOOP_LIMIT: # Bounded loop execution (Rule #6)
        current_path = file_paths_list[file_idx] # Retrieve current file path string
        assert isinstance(current_path, str), "File path item must be a string" # Assertion 3: Validate path type (Rule #9, #11)
        
        # If multiple files are processed, prepend standard UNIX header format
        if total_files > 1:                 # Check if batch contains multiple files
            if file_idx > 0:                # Check if this is a subsequent file in the batch
                batch_output_list.append("\n") # Append blank separator line between file outputs
            header_str = "==> %s <==\n" % current_path # Format header string with file path
            batch_output_list.append(header_str) # Append header string to batch output list
            
        file_tail_lines = extract_simple_tail_lines(current_path, target_count) # Extract tail for current file
        batch_output_list.extend(file_tail_lines) # Extend batch output list with file tail lines
        
        file_idx += 1                       # Increment file iteration index variable
        
    assert isinstance(batch_output_list, list), "Batch output must be a list"   # Assertion 4: Validate return type (Rule #11)
    return batch_output_list                # Return complete formatted batch output list

def run_step19_harness():
    # Main orchestration function for Step 19 execution and logging
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Retrieve absolute directory path of script (Rule #11)
    output_filename = os.path.join(script_dir, "tail_step19_output.txt") # Define absolute path for log output (Rule #2, #4)
    file_alpha_path = os.path.join(script_dir, "test_sample_alpha.txt") # Define absolute path for sample file alpha
    file_beta_path = os.path.join(script_dir, "test_sample_beta.txt")   # Define absolute path for sample file beta
    
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
        print "=== CODING CHALLENGE #141: STEP 19 INITIALIZED (ADVANCED EXTENSION 6) ===" # Trace statement start marker (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer to disk
        
        # Create sample file Alpha with 4 lines
        alpha_handle = open(file_alpha_path, "w") # Open sample alpha file for writing
        try:
            alpha_handle.write("Alpha Line 1\nAlpha Line 2\nAlpha Line 3\nAlpha Line 4\n") # Write alpha content
        finally:
            alpha_handle.close()            # Ensure alpha file handle is closed securely
            
        # Create sample file Beta with 4 lines
        beta_handle = open(file_beta_path, "w")   # Open sample beta file for writing
        try:
            beta_handle.write("Beta Line 1\nBeta Line 2\nBeta Line 3\nBeta Line 4\n")   # Write beta content
        finally:
            beta_handle.close()             # Ensure beta file handle is closed securely
            
        print "TRACE: Sample test files Alpha and Beta created successfully" # Trace file creation step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        # Execute multi-file batch processing with header formatting requesting last 2 lines per file
        batch_file_list = [file_alpha_path, file_beta_path] # Assemble list of target file paths
        batch_results = process_multi_file_batch(batch_file_list, DEFAULT_LINE_COUNT) # Process batch
        print "TRACE: Multi-file batch processing completed successfully (%d lines generated)" % len(batch_results) # Trace processing step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        print "--- MULTI-FILE BATCH OUTPUT RESULTS ---" # Print header for output section
        print_idx = 0                       # Initialize print iteration index (Rule #10)
        while print_idx < len(batch_results) and print_idx < MAX_LOOP_LIMIT: # Bounded loop for printing results (Rule #6)
            sys.stdout.write(batch_results[print_idx]) # Write each batch line directly to output stream
            print_idx += 1                  # Increment print iteration index variable
            
        print "=== STEP 19 EXECUTION COMPLETED SUCCESSFULLY ===" # Trace success completion marker (Rule #3)
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
    execution_result = run_step19_harness() # Execute main harness orchestration function
    assert execution_result == True, "Main execution harness failed" # Final return assertion check (Rule #11)
