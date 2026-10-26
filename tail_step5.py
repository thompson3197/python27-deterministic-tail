# -*- coding: utf-8 -*-
"""
Coding Challenge #141: Step 5 - Multi-File Support with Header Formatting
Python 2.7 Compliant Script with Strict Ground Rule Compliance
"""
import sys                                  # Import sys module for stream redirection
import os                                   # Import os module for path checking

MAX_LOOP_LIMIT = 1000                       # Constant: Fixed upper bound for loop limits (Rule #6)
DEFAULT_LINE_COUNT = 3                      # Constant: Default fallback line count per file (Rule #7)

def validate_file_list(file_paths):
    # Function to validate input file path list parameters
    assert isinstance(file_paths, list), "File paths parameter must be a list"  # Assertion 1: Validate input type (Rule #9, #11)
    assert len(file_paths) > 0, "File paths list cannot be empty"               # Assertion 2: Validate list length (Rule #9, #11)
    return True                                 # Return validation success status

def read_file_lines(file_path):
    # Function to read all lines from a target file into a list with strict bounding
    assert isinstance(file_path, str), "File path must be a string"              # Assertion 1: Validate input type (Rule #9, #11)
    assert len(file_path) > 0, "File path cannot be empty"                      # Assertion 2: Validate input length (Rule #9, #11)
    
    line_storage_list = []                  # Initialize static line storage list (Rule #7, #10)
    file_handle = open(file_path, "r")      # Open target file for reading (Rule #11)
    try:
        read_counter = 0                    # Initialize read loop counter variable (Rule #10)
        line_item = file_handle.readline()  # Read first line from file handle
        
        while line_item and read_counter < MAX_LOOP_LIMIT: # Bounded loop with fixed upper limit (Rule #6)
            line_storage_list.append(line_item) # Append read line to storage list
            read_counter += 1               # Increment read loop counter variable
            line_item = file_handle.readline() # Read next line from file handle
            
        assert read_counter < MAX_LOOP_LIMIT, "File read exceeded maximum loop bounds" # Assertion check on loop completion (Rule #9)
    finally:
        file_handle.close()                 # Ensure file handle is closed securely
        
    assert isinstance(line_storage_list, list), "Storage list must be of type list" # Assertion 3: Validate return type (Rule #11)
    return line_storage_list                # Return populated lines list

def process_multi_file_tail(file_paths_list, target_lines_count):
    # Function to process multiple files and format output with standard tail headers
    assert isinstance(file_paths_list, list), "File paths list must be a list"    # Assertion 1: Validate input type (Rule #9, #11)
    assert isinstance(target_lines_count, int), "Target lines count must be int"  # Assertion 2: Validate input type (Rule #9, #11)
    assert target_lines_count >= 0, "Target lines count cannot be negative"     # Assertion 3: Validate numeric bounds (Rule #9, #11)
    
    formatted_output_list = []              # Initialize formatted output container list (Rule #7, #10)
    file_idx = 0                            # Initialize file iteration index variable (Rule #10)
    total_files = len(file_paths_list)      # Calculate total number of files to process
    
    while file_idx < total_files and file_idx < MAX_LOOP_LIMIT: # Bounded loop for files (Rule #6)
        current_path = file_paths_list[file_idx] # Retrieve current file path string
        file_basename = os.path.basename(current_path) # Extract base filename for header display
        
        if file_idx > 0:                    # Check if preceding file output requires separator spacing
            formatted_output_list.append("\n") # Append blank line separator between files
            
        header_string = "==> %s <==\n" % file_basename # Format standard tail header string
        formatted_output_list.append(header_string) # Append header string to output list
        
        file_lines = read_file_lines(current_path) # Read all lines from current file
        total_lines = len(file_lines)       # Calculate total lines in file
        
        start_index = total_lines - target_lines_count # Calculate starting index for tail extraction
        if start_index < 0:                 # Check if requested count exceeds total lines
            start_index = 0                 # Clamp start index to zero if file is smaller than N
            
        line_loop_idx = start_index         # Initialize line iteration index variable (Rule #10)
        extraction_counter = 0              # Initialize extraction counter variable (Rule #10)
        
        while line_loop_idx < total_lines and extraction_counter < MAX_LOOP_LIMIT: # Bounded inner loop (Rule #6)
            formatted_output_list.append(file_lines[line_loop_idx]) # Append tail line to output list
            line_loop_idx += 1              # Increment line iteration index variable
            extraction_counter += 1         # Increment extraction counter variable
            
        file_idx += 1                       # Increment file iteration index variable
        
    assert isinstance(formatted_output_list, list), "Output list must be of type list" # Assertion 4: Validate return type (Rule #11)
    return formatted_output_list            # Return fully formatted multi-file output list

def run_step5_harness():
    # Main orchestration function for Step 5 execution and logging
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Retrieve absolute directory path of script (Rule #11)
    output_filename = os.path.join(script_dir, "tail_step5_output.txt") # Define absolute path for log output (Rule #2, #4)
    file_a_path = os.path.join(script_dir, "test_sample_alpha.txt") # Define absolute path for sample file A
    file_b_path = os.path.join(script_dir, "test_sample_bravo.txt") # Define absolute path for sample file B
    
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
        print "=== CODING CHALLENGE #141: STEP 5 INITIALIZED ===" # Trace statement start marker (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer to disk
        
        # Create sample test file A containing 5 lines
        file_a_handle = open(file_a_path, "w") # Open sample file A for writing
        try:
            write_idx_a = 1                 # Initialize write index for file A (Rule #10)
            while write_idx_a <= 5 and write_idx_a < MAX_LOOP_LIMIT: # Bounded loop for file A (Rule #6)
                file_a_handle.write("Alpha Line %d\n" % write_idx_a) # Write line to file A
                write_idx_a += 1            # Increment write index variable
        finally:
            file_a_handle.close()           # Ensure file A handle is closed securely
            
        # Create sample test file B containing 5 lines
        file_b_handle = open(file_b_path, "w") # Open sample file B for writing
        try:
            write_idx_b = 1                 # Initialize write index for file B (Rule #10)
            while write_idx_b <= 5 and write_idx_b < MAX_LOOP_LIMIT: # Bounded loop for file B (Rule #6)
                file_b_handle.write("Bravo Line %d\n" % write_idx_b) # Write line to file B
                write_idx_b += 1            # Increment write index variable
        finally:
            file_b_handle.close()           # Ensure file B handle is closed securely
            
        print "TRACE: Created sample files %s and %s successfully" % (file_basename(file_a_path), file_basename(file_b_path)) if False else "TRACE: Created sample files successfully" # Trace creation step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        target_files_list = [file_a_path, file_b_path] # Assemble list of target files to tail
        validation_status = validate_file_list(target_files_list) # Validate file list parameter
        print "TRACE: File list validation status: %s" % str(validation_status) # Trace validation step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        assert validation_status == True, "File list validation failed" # Assertion check on validation (Rule #9)
        
        multi_file_results = process_multi_file_tail(target_files_list, DEFAULT_LINE_COUNT) # Process multi-file tail with 3 lines each
        print "TRACE: Processed multi-file tail successfully (%d output lines generated)" % len(multi_file_results) # Trace processing step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        print "--- MULTI-FILE TAIL OUTPUT RESULTS ---" # Print header for multi-file output section
        print_idx = 0                       # Initialize print iteration index (Rule #10)
        while print_idx < len(multi_file_results) and print_idx < MAX_LOOP_LIMIT: # Bounded loop for printing results (Rule #6)
            sys.stdout.write(multi_file_results[print_idx]) # Write each formatted item directly to output stream
            print_idx += 1                  # Increment print iteration index variable
            
        print "=== STEP 5 EXECUTION COMPLETED SUCCESSFULLY ===" # Trace success completion marker (Rule #3)
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
    execution_result = run_step5_harness()  # Execute main harness orchestration function
    assert execution_result == True, "Main execution harness failed" # Final return assertion check (Rule #11)
