# -*- coding: utf-8 -*-
"""
Coding Challenge #141: Step 7 - Reverse Byte/Line Traversal Buffer Algorithm
Python 2.7 Compliant Script with Strict Ground Rule Compliance
"""
import sys                                  # Import sys module for stream redirection
import os                                   # Import os module for path checking

MAX_LOOP_LIMIT = 1000                       # Constant: Fixed upper bound for loop limits (Rule #6)
BLOCK_SIZE = 4096                           # Constant: Block size for reverse chunk reading (Rule #7)
DEFAULT_LINE_COUNT = 4                      # Constant: Default fallback line count (Rule #7)

def reverse_read_last_n_lines(file_path, target_count):
    # Function to read last N lines by traversing file backwards in blocks
    assert isinstance(file_path, str), "File path must be a string"              # Assertion 1: Validate input type (Rule #9, #11)
    assert isinstance(target_count, int), "Target count must be an integer"       # Assertion 2: Validate input type (Rule #9, #11)
    assert target_count >= 0, "Target count cannot be negative"                 # Assertion 3: Validate numeric bounds (Rule #9, #11)
    
    extracted_lines_list = []               # Initialize output lines container list (Rule #7, #10)
    file_handle = open(file_path, "rb")     # Open target file in binary read mode (Rule #11)
    try:
        file_handle.seek(0, 2)              # Seek to the absolute end of the file stream
        file_size = file_handle.tell()      # Retrieve total file size in bytes
        
        if file_size == 0:                  # Check if file is completely empty
            return extracted_lines_list     # Return empty list immediately if no content
            
        blocks_data_list = []               # Initialize blocks storage list (Rule #7, #10)
        remaining_bytes = file_size         # Initialize remaining bytes counter variable (Rule #10)
        loop_counter = 0                    # Initialize block traversal loop counter (Rule #10)
        
        while remaining_bytes > 0 and loop_counter < MAX_LOOP_LIMIT: # Bounded loop execution (Rule #6)
            current_read_size = BLOCK_SIZE  # Determine read size for current block chunk
            if remaining_bytes < BLOCK_SIZE: # Check if remaining bytes are less than standard block size
                current_read_size = remaining_bytes # Set read size to exact remaining byte count
                
            remaining_bytes -= current_read_size # Decrement remaining bytes counter variable
            file_handle.seek(remaining_bytes, 0) # Seek to calculated block start position
            block_bytes = file_handle.read(current_read_size) # Read block chunk into memory
            blocks_data_list.insert(0, block_bytes) # Prepend block chunk to preserve correct sequential order
            loop_counter += 1               # Increment loop counter variable
            
        assert loop_counter < MAX_LOOP_LIMIT, "Block traversal exceeded maximum loop bounds" # Assertion check on loop completion (Rule #9)
        
        combined_content = "".join(blocks_data_list) # Concatenate all retrieved block chunks together
        all_lines = combined_content.splitlines(True) # Split combined content into lines preserving newline chars
        total_lines = len(all_lines)        # Calculate total line count in file
        
        start_index = total_lines - target_count # Calculate starting index for tail extraction
        if start_index < 0:                 # Check if requested count exceeds total lines
            start_index = 0                 # Clamp start index to zero if file is smaller than N
            
        line_idx = start_index              # Initialize line iteration index variable (Rule #10)
        extraction_counter = 0              # Initialize extraction counter variable (Rule #10)
        
        while line_idx < total_lines and extraction_counter < MAX_LOOP_LIMIT: # Bounded extraction loop (Rule #6)
            extracted_lines_list.append(all_lines[line_idx]) # Append line to extracted result list
            line_idx += 1                   # Increment line iteration index variable
            extraction_counter += 1         # Increment extraction counter variable
            
    finally:
        file_handle.close()                 # Ensure file handle is closed securely
        
    assert isinstance(extracted_lines_list, list), "Result must be a list"      # Assertion 4: Validate return type (Rule #11)
    return extracted_lines_list             # Return final reverse-traversed lines list

def run_step7_harness():
    # Main orchestration function for Step 7 execution and logging
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Retrieve absolute directory path of script (Rule #11)
    output_filename = os.path.join(script_dir, "tail_step7_output.txt") # Define absolute path for log output (Rule #2, #4)
    sample_filename = os.path.join(script_dir, "test_sample_step7.txt") # Define absolute path for sample test file
    
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
        print "=== CODING CHALLENGE #141: STEP 7 INITIALIZED ===" # Trace statement start marker (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer to disk
        
        # Create a sample test file containing 10 lines to verify reverse traversal extraction
        sample_file_handle = open(sample_filename, "w") # Open sample test file for writing
        try:
            write_idx = 1                   # Initialize write index variable (Rule #10)
            while write_idx <= 10 and write_idx < MAX_LOOP_LIMIT: # Bounded loop for test data creation (Rule #6)
                sample_file_handle.write("Reverse Test Line %d\n" % write_idx) # Write formatted test line
                write_idx += 1              # Increment write index variable
        finally:
            sample_file_handle.close()      # Ensure sample file handle is closed securely
            
        print "TRACE: Sample test file created with 10 lines at %s" % sample_filename # Trace file creation step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        reverse_results = reverse_read_last_n_lines(sample_filename, DEFAULT_LINE_COUNT) # Execute reverse tail extraction
        print "TRACE: Extracted last %d lines successfully using reverse block traversal" % len(reverse_results) # Trace extraction step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        print "--- REVERSE TAIL OUTPUT RESULTS ---" # Print header for tail output section
        print_idx = 0                       # Initialize print iteration index (Rule #10)
        while print_idx < len(reverse_results) and print_idx < MAX_LOOP_LIMIT: # Bounded loop for printing results (Rule #6)
            sys.stdout.write(reverse_results[print_idx]) # Write each tail line directly to output stream
            print_idx += 1                  # Increment print iteration index variable
            
        print "=== STEP 7 EXECUTION COMPLETED SUCCESSFULLY ===" # Trace success completion marker (Rule #3)
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
    execution_result = run_step7_harness()  # Execute main harness orchestration function
    assert execution_result == True, "Main execution harness failed" # Final return assertion check (Rule #11)
