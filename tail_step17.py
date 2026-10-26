# -*- coding: utf-8 -*-
"""
Coding Challenge #141: Step 17 - Advanced Extension 4: Line Number Caching & Index Acceleration
Python 2.7 Compliant Script with Strict Ground Rule Compliance
"""
import sys                                  # Import sys module for stream redirection
import os                                   # Import os module for path checking

MAX_LOOP_LIMIT = 1000                       # Constant: Fixed upper bound for loop limits (Rule #6)
DEFAULT_TARGET_LINE = 5                     # Constant: Default fallback target line index (Rule #7)

def build_line_index_cache(file_path):
    # Function to scan file once and construct a byte-offset index cache for every line start
    assert isinstance(file_path, str), "File path must be a string"              # Assertion 1: Validate input type (Rule #9, #11)
    assert len(file_path) > 0, "File path cannot be empty"                      # Assertion 2: Validate input length (Rule #9, #11)
    
    offset_index_list = [0]                 # Initialize static offset index list with start byte 0 (Rule #7, #10)
    file_handle = open(file_path, "rb")     # Open target file in binary read mode (Rule #11)
    try:
        scan_counter = 0                    # Initialize scan loop counter variable (Rule #10)
        byte_chunk = file_handle.read(1)    # Read single byte from stream to inspect boundaries
        current_offset = 0                  # Initialize current byte offset tracker (Rule #10)
        
        while len(byte_chunk) > 0 and scan_counter < MAX_LOOP_LIMIT: # Bounded loop execution (Rule #6)
            current_offset += 1             # Increment current byte offset counter
            if byte_chunk == b"\n":         # Check if byte encountered is a newline delimiter
                offset_index_list.append(int(current_offset)) # Append byte offset where next line begins
            byte_chunk = file_handle.read(1) # Read next single byte from stream
            scan_counter += 1               # Increment scan loop counter variable
            
        assert scan_counter < MAX_LOOP_LIMIT, "File index scan exceeded maximum loop bounds" # Assertion check on loop completion (Rule #9)
    finally:
        file_handle.close()                 # Ensure file handle is closed securely
        
    assert isinstance(offset_index_list, list), "Offset index must be a list"   # Assertion 3: Validate return type (Rule #11)
    assert len(offset_index_list) > 0, "Offset index cache cannot be empty"     # Assertion 4: Validate cache size bounds (Rule #9, #11)
    return offset_index_list                # Return populated byte-offset index cache list

def fetch_line_via_cache_index(file_path, index_cache, target_line_number):
    # Function to jump directly to a target line using the pre-computed byte offset cache
    assert isinstance(file_path, str), "File path must be a string"              # Assertion 1: Validate input type (Rule #9, #11)
    assert isinstance(index_cache, list), "Index cache must be a list"          # Assertion 2: Validate input type (Rule #9, #11)
    assert isinstance(target_line_number, int), "Target line must be integer"   # Assertion 3: Validate input type (Rule #9, #11)
    assert target_line_number >= 0, "Target line number cannot be negative"     # Assertion 4: Validate numeric bounds (Rule #9, #11)
    
    retrieved_line_text = ""                # Initialize retrieved line container string (Rule #7, #10)
    total_cached_lines = len(index_cache)   # Determine total cached lines available in index
    
    if target_line_number >= total_cached_lines: # Check if requested line exceeds cached range
        return "[Line Index Out of Range]"  # Return boundary notification string
        
    file_handle = open(file_path, "rb")     # Open target file in binary read mode (Rule #11)
    try:
        start_byte_offset = index_cache[target_line_number] # Retrieve exact byte offset for target line
        file_handle.seek(int(start_byte_offset), 0) # Jump directly to line start position via seek
        retrieved_line_text = file_handle.readline() # Read the target line directly from stream
    except (IOError, OSError), seek_err:
        sys.stderr.write("WARNING: Indexed seek operation failed: %s\n" % str(seek_err)) # Write warning to stderr
    finally:
        file_handle.close()                 # Ensure file handle is closed securely
        
    assert isinstance(retrieved_line_text, str), "Retrieved line must be a string" # Assertion 5: Validate return type (Rule #11)
    return retrieved_line_text              # Return fetched line string

def run_step17_harness():
    # Main orchestration function for Step 17 execution and logging
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Retrieve absolute directory path of script (Rule #11)
    output_filename = os.path.join(script_dir, "tail_step17_output.txt") # Define absolute path for log output (Rule #2, #4)
    sample_filename = os.path.join(script_dir, "test_sample_step17.txt") # Define absolute path for sample test file
    
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
        print "=== CODING CHALLENGE #141: STEP 17 INITIALIZED (ADVANCED EXTENSION 4) ===" # Trace statement start marker (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer to disk
        
        # Create sample test file containing 8 distinct numbered lines
        sample_file_handle = open(sample_filename, "w") # Open sample test file for writing
        try:
            write_idx = 1                   # Initialize write index variable (Rule #10)
            while write_idx <= 8 and write_idx < MAX_LOOP_LIMIT: # Bounded loop for test data creation (Rule #6)
                sample_file_handle.write("Indexed Record Line %d\n" % write_idx) # Write formatted record line
                write_idx += 1              # Increment write index variable
        finally:
            sample_file_handle.close()      # Ensure sample file handle is closed securely
            
        print "TRACE: Sample test file created with 8 records at %s" % sample_filename # Trace file creation step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        # Build line offset index cache
        line_cache_index = build_line_index_cache(sample_filename) # Construct byte offset index cache
        print "TRACE: Built line index cache successfully (%d index entries)" % len(line_cache_index) # Trace cache step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        # Test direct indexed lookup for Line 3 (0-based index 2) and Line 6 (0-based index 5)
        fetched_line_three = fetch_line_via_cache_index(sample_filename, line_cache_index, 2) # Fetch line index 2
        fetched_line_six = fetch_line_via_cache_index(sample_filename, line_cache_index, 5) # Fetch line index 5
        print "TRACE: Direct indexed lookups completed successfully" # Trace lookup step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        print "--- INDEX ACCELERATION OUTPUT RESULTS ---" # Print header for output section
        print "Indexed Lookup [Line Index 2 -> Expected Record 3]: %s" % fetched_line_three.strip() # Print lookup 1 result
        print "Indexed Lookup [Line Index 5 -> Expected Record 6]: %s" % fetched_line_six.strip() # Print lookup 2 result
            
        print "=== STEP 17 EXECUTION COMPLETED SUCCESSFULLY ===" # Trace success completion marker (Rule #3)
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
    execution_result = run_step17_harness() # Execute main harness orchestration function
    assert execution_result == True, "Main execution harness failed" # Final return assertion check (Rule #11)
