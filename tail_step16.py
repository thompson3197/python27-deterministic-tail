# -*- coding: utf-8 -*-
"""
Coding Challenge #141: Step 16 - Advanced Extension 3: Byte-Offset Boundary Clamping & Recovery
Python 2.7 Compliant Script with Strict Ground Rule Compliance
"""
import sys                                  # Import sys module for stream redirection
import os                                   # Import os module for path checking

MAX_LOOP_LIMIT = 1000                       # Constant: Fixed upper bound for loop limits (Rule #6)
DEFAULT_BYTE_OFFSET = 10                    # Constant: Default fallback byte offset (Rule #7)

def clamp_byte_offset(file_size, requested_offset):
    # Function to clamp requested byte offset within valid file boundary limits
    assert isinstance(file_size, (int, long)), "File size must be an integer or long" # Assertion 1: Validate input type for Python 2.7 win32 (Rule #9, #11)
    assert isinstance(requested_offset, (int, long)), "Requested offset must be numeric" # Assertion 2: Validate input type (Rule #9, #11)
    assert file_size >= 0, "File size cannot be negative"                       # Assertion 3: Validate numeric bounds (Rule #9, #11)
    
    clamped_offset = int(requested_offset)  # Cast requested offset to standard integer (Rule #10)
    int_file_size = int(file_size)          # Cast file size to standard integer (Rule #10)
    
    if clamped_offset < 0:                  # Check if requested offset is negative
        clamped_offset = 0                  # Clamp negative offset to absolute zero start
    elif clamped_offset > int_file_size:    # Check if requested offset exceeds total file size
        clamped_offset = int_file_size      # Clamp excessive offset to maximum file size
        
    assert isinstance(clamped_offset, int), "Clamped offset must evaluate to an integer" # Assertion 4: Validate return type (Rule #11)
    assert clamped_offset >= 0 and clamped_offset <= int_file_size, "Clamped offset out of bounds" # Assertion 5: Validate final range bounds (Rule #9, #11)
    return clamped_offset                   # Return validated clamped offset integer

def safe_seek_and_extract_bytes(file_path, requested_offset):
    # Function to securely seek to clamped offset and extract remaining file stream bytes
    assert isinstance(file_path, str), "File path must be a string"              # Assertion 1: Validate input type (Rule #9, #11)
    assert isinstance(requested_offset, (int, long)), "Requested offset must be numeric" # Assertion 2: Validate input type (Rule #9, #11)
    
    extracted_chunk = ""                    # Initialize output chunk container string (Rule #7, #10)
    file_handle = open(file_path, "rb")     # Open target file in binary read mode (Rule #11)
    try:
        file_handle.seek(0, 2)              # Seek to absolute end of file stream
        file_size = file_handle.tell()      # Retrieve total file size in bytes (returns long on win32)
        
        safe_offset = clamp_byte_offset(file_size, requested_offset) # Clamp offset securely
        file_handle.seek(safe_offset, 0)    # Seek to safe clamped byte position
        
        extracted_chunk = file_handle.read() # Read remaining bytes from clamped position
    except (IOError, OSError), seek_err:
        sys.stderr.write("WARNING: Seek operation adjusted due to error: %s\n" % str(seek_err)) # Log seek warning to stderr
    finally:
        file_handle.close()                 # Ensure file handle is closed securely
        
    assert isinstance(extracted_chunk, str), "Extracted chunk must be of type string" # Assertion 3: Validate return type (Rule #11)
    return extracted_chunk                  # Return extracted byte chunk string

def run_step16_harness():
    # Main orchestration function for Step 16 execution and logging
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Retrieve absolute directory path of script (Rule #11)
    output_filename = os.path.join(script_dir, "tail_step16_output.txt") # Define absolute path for log output (Rule #2, #4)
    sample_filename = os.path.join(script_dir, "test_sample_step16.bin") # Define absolute path for sample binary file
    
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
        print "=== CODING CHALLENGE #141: STEP 16 INITIALIZED (ADVANCED EXTENSION 3) ===" # Trace statement start marker (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer to disk
        
        # Create a sample binary file containing exactly 25 bytes
        sample_file_handle = open(sample_filename, "wb") # Open sample binary file for writing
        try:
            payload_data = "ABCDEFGHIJKLMNOPQRSTUVWXY" # Define 25-byte sample payload string
            sample_file_handle.write(payload_data) # Write payload data to file
        finally:
            sample_file_handle.close()      # Ensure sample file handle is closed securely
            
        print "TRACE: Sample binary test file created with 25 bytes at %s" % sample_filename # Trace file creation step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        # Test Case A: Normal valid offset (Offset 15 -> should yield last 10 bytes 'PQRSTUVWXY')
        result_normal = safe_seek_and_extract_bytes(sample_filename, 15) # Extract bytes starting from offset 15
        print "TRACE: Extraction at normal offset 15 successful (%d bytes)" % len(result_normal) # Trace result step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        # Test Case B: Out-of-bounds excessive offset (Offset 100 -> should clamp to file size 25)
        result_overflow = safe_seek_and_extract_bytes(sample_filename, 100) # Extract bytes starting from excessive offset 100
        print "TRACE: Overflow offset 100 clamped successfully (%d bytes yielded)" % len(result_overflow) # Trace result step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        # Test Case C: Negative offset (Offset -50 -> should clamp to 0 start)
        result_underflow = safe_seek_and_extract_bytes(sample_filename, -50) # Extract bytes starting from negative offset -50
        print "TRACE: Underflow offset -50 clamped successfully (%d bytes yielded)" % len(result_underflow) # Trace result step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        print "--- BOUNDARY CLAMPING OUTPUT RESULTS ---" # Print header for output section
        print "Normal Offset (15): %s" % result_normal # Print normal offset result
        print "Overflow Offset (100 -> clamped): %s" % (result_overflow if len(result_overflow) > 0 else "[EOF Reached]") # Print overflow result
        print "Underflow Offset (-50 -> clamped to 0): %s" % result_underflow[:10] # Print partial underflow result preview
            
        print "=== STEP 16 EXECUTION COMPLETED SUCCESSFULLY ===" # Trace success completion marker (Rule #3)
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
    execution_result = run_step16_harness() # Execute main harness orchestration function
    assert execution_result == True, "Main execution harness failed" # Final return assertion check (Rule #11)
