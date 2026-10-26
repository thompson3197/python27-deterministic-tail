# -*- coding: utf-8 -*-
"""
Coding Challenge #141: Step 18 - Advanced Extension 5: Memory-Mapped File I/O Optimization
Python 2.7 Compliant Script with Strict Ground Rule Compliance
"""
import sys                                  # Import sys module for stream redirection
import os                                   # Import os module for path checking
import mmap                                 # Import mmap module for memory-mapped file operations

MAX_LOOP_LIMIT = 1000                       # Constant: Fixed upper bound for loop limits (Rule #6)
DEFAULT_TAIL_COUNT = 3                      # Constant: Default fallback tail line count (Rule #7)

def mmap_extract_last_n_lines(file_path, target_count):
    # Function to extract last N lines from file using memory-mapped I/O optimization
    assert isinstance(file_path, str), "File path must be a string"              # Assertion 1: Validate input type (Rule #9, #11)
    assert isinstance(target_count, (int, long)), "Target count must be numeric"  # Assertion 2: Validate input type (Rule #9, #11)
    assert target_count >= 0, "Target count cannot be negative"                 # Assertion 3: Validate numeric bounds (Rule #9, #11)
    
    extracted_lines_list = []               # Initialize output lines container list (Rule #7, #10)
    int_target_count = int(target_count)    # Cast target count to standard integer (Rule #10)
    
    file_handle = open(file_path, "rb")     # Open target file in binary read mode (Rule #11)
    try:
        file_handle.seek(0, 2)              # Seek to absolute end of file stream
        file_size = file_handle.tell()      # Retrieve total file size in bytes
        
        if file_size == 0:                  # Check if file is completely empty
            return extracted_lines_list     # Return empty list immediately if no content
            
        # Create memory map object over the file descriptor
        memory_map_obj = mmap.mmap(file_handle.fileno(), 0, access=mmap.ACCESS_READ) # Map file into memory
        try:
            current_offset = int(file_size) - 1 # Initialize search offset from end of file (Rule #10)
            found_newlines_count = 0        # Initialize newline counter variable (Rule #10)
            scan_counter = 0                # Initialize backward scan loop counter (Rule #10)
            
            while current_offset >= 0 and scan_counter < MAX_LOOP_LIMIT: # Bounded backward loop execution (Rule #6)
                if memory_map_obj[current_offset] == b"\n": # Check if byte is a newline character
                    found_newlines_count += 1 # Increment newline match counter
                    if found_newlines_count > int_target_count: # Check if requested line threshold is met
                        break               # Exit scan loop once enough trailing lines are isolated
                current_offset -= 1         # Decrement offset position to move backwards
                scan_counter += 1           # Increment scan loop counter variable
                
            assert scan_counter < MAX_LOOP_LIMIT, "Memory map scan exceeded maximum loop bounds" # Assertion check on loop completion (Rule #9)
            
            # Slice memory map from calculated offset to end of file
            start_slice_offset = current_offset + 1 if current_offset >= 0 else 0 # Determine exact start byte offset
            mapped_byte_chunk = memory_map_obj[start_slice_offset:file_size] # Extract byte chunk from memory map
            extracted_lines_list = mapped_byte_chunk.splitlines(True) # Split byte chunk into lines preserving delimiters
            
        finally:
            memory_map_obj.close()          # Ensure memory map object is closed securely
            
    finally:
        file_handle.close()                 # Ensure underlying file handle is closed securely
        
    assert isinstance(extracted_lines_list, list), "Result must be a list"      # Assertion 4: Validate return type (Rule #11)
    return extracted_lines_list             # Return final memory-mapped extracted lines list

def run_step18_harness():
    # Main orchestration function for Step 18 execution and logging
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Retrieve absolute directory path of script (Rule #11)
    output_filename = os.path.join(script_dir, "tail_step18_output.txt") # Define absolute path for log output (Rule #2, #4)
    sample_filename = os.path.join(script_dir, "test_sample_step18.txt") # Define absolute path for sample test file
    
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
        print "=== CODING CHALLENGE #141: STEP 18 INITIALIZED (ADVANCED EXTENSION 5) ===" # Trace statement start marker (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer to disk
        
        # Create sample test file containing 6 distinct log records
        sample_file_handle = open(sample_filename, "w") # Open sample test file for writing
        try:
            write_idx = 1                   # Initialize write index variable (Rule #10)
            while write_idx <= 6 and write_idx < MAX_LOOP_LIMIT: # Bounded loop for test data creation (Rule #6)
                sample_file_handle.write("Memory Mapped Record Line %d\n" % write_idx) # Write formatted record line
                write_idx += 1              # Increment write index variable
        finally:
            sample_file_handle.close()      # Ensure sample file handle is closed securely
            
        print "TRACE: Sample test file created with 6 records at %s" % sample_filename # Trace file creation step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        mmap_results = mmap_extract_last_n_lines(sample_filename, DEFAULT_TAIL_COUNT) # Execute memory-mapped tail extraction
        print "TRACE: Memory-mapped tail extraction completed successfully (%d lines)" % len(mmap_results) # Trace extraction step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        print "--- MEMORY-MAPPED TAIL OUTPUT RESULTS ---" # Print header for output section
        print_idx = 0                       # Initialize print iteration index (Rule #10)
        while print_idx < len(mmap_results) and print_idx < MAX_LOOP_LIMIT: # Bounded loop for printing results (Rule #6)
            sys.stdout.write(mmap_results[print_idx]) # Write each extracted line directly to output stream
            print_idx += 1                  # Increment print iteration index variable
            
        print "=== STEP 18 EXECUTION COMPLETED SUCCESSFULLY ===" # Trace success completion marker (Rule #3)
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
    execution_result = run_step18_harness() # Execute main harness orchestration function
    assert execution_result == True, "Main execution harness failed" # Final return assertion check (Rule #11)
