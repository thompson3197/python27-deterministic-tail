# -*- coding: utf-8 -*-
"""
Coding Challenge #141: Step 4 - Custom Byte Count via -c / --bytes Flag
Python 2.7 Compliant Script with Strict Ground Rule Compliance
"""
import sys                                  # Import sys module for stream and argument handling
import os                                   # Import os module for path checking

MAX_LOOP_LIMIT = 1000                       # Constant: Fixed upper bound for loop limits (Rule #6)
DEFAULT_BYTE_COUNT = 20                     # Constant: Default fallback byte count (Rule #7)

def parse_bytes_argument(arg_list):
    # Function to parse custom byte count from argument list simulating -c / --bytes flags
    assert isinstance(arg_list, list), "Argument list must be a list"           # Assertion 1: Validate input type (Rule #9, #11)
    assert len(arg_list) < MAX_LOOP_LIMIT, "Argument list exceeds maximum bounds" # Assertion 2: Validate size bounds (Rule #9, #11)
    
    parsed_bytes = DEFAULT_BYTE_COUNT       # Initialize parsed bytes with default value (Rule #10)
    arg_idx = 0                             # Initialize argument iteration index variable (Rule #10)
    
    while arg_idx < len(arg_list) and arg_idx < MAX_LOOP_LIMIT: # Bounded loop execution (Rule #6)
        current_arg = arg_list[arg_idx]     # Retrieve current argument string from list
        if current_arg == "-c" or current_arg == "--bytes": # Check for byte count flag identifier
            assert arg_idx + 1 < len(arg_list), "Missing value following byte count flag" # Assertion check for flag value existence (Rule #9, #11)
            value_arg = arg_list[arg_idx + 1] # Retrieve value argument following the flag
            parsed_bytes = int(value_arg)   # Convert value string to integer byte count
            break                           # Exit loop once flag and value are processed
        arg_idx += 1                        # Increment argument iteration index variable
        
    assert isinstance(parsed_bytes, int), "Parsed bytes must evaluate to an integer" # Assertion 3: Validate return type (Rule #11)
    assert parsed_bytes >= 0, "Parsed bytes cannot be negative"                 # Assertion 4: Validate numeric range (Rule #9, #11)
    return parsed_bytes                     # Return validated custom byte count integer

def extract_last_n_bytes(file_path, target_bytes):
    # Function to extract the last N bytes from a target file securely
    assert isinstance(file_path, str), "File path must be a string"              # Assertion 1: Validate input type (Rule #9, #11)
    assert isinstance(target_bytes, int), "Target bytes must be an integer"       # Assertion 2: Validate input type (Rule #9, #11)
    assert target_bytes >= 0, "Target bytes cannot be negative"                 # Assertion 3: Validate numeric bounds (Rule #9, #11)
    
    extracted_data = ""                     # Initialize output data container string (Rule #7, #10)
    file_handle = open(file_path, "rb")     # Open target file in binary read mode (Rule #11)
    try:
        file_content = file_handle.read()   # Read entire file content into memory buffer
        content_length = len(file_content)  # Calculate total byte length of file content
        
        start_index = content_length - target_bytes # Calculate starting byte index for tail extraction
        if start_index < 0:                 # Check if requested byte count exceeds total length
            start_index = 0                 # Clamp start index to zero if file is smaller than N bytes
            
        byte_idx = start_index              # Initialize byte iteration index variable (Rule #10)
        copy_counter = 0                    # Initialize copy counter variable (Rule #10)
        
        while byte_idx < content_length and copy_counter < MAX_LOOP_LIMIT: # Bounded loop execution (Rule #6)
            extracted_data += file_content[byte_idx] # Append byte to extracted data string
            byte_idx += 1                   # Increment byte iteration index variable
            copy_counter += 1               # Increment copy counter variable
            
    finally:
        file_handle.close()                 # Ensure file handle is closed securely
        
    assert isinstance(extracted_data, str), "Extracted data must be of type string" # Assertion 4: Validate return type (Rule #11)
    return extracted_data                   # Return final extracted byte string

def run_step4_harness():
    # Main orchestration function for Step 4 execution and logging
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Retrieve absolute directory path of script (Rule #11)
    output_filename = os.path.join(script_dir, "tail_step4_output.txt") # Define absolute path for log output (Rule #2, #4)
    sample_filename = os.path.join(script_dir, "test_sample_step4.txt") # Define absolute path for sample test file
    
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
        print "=== CODING CHALLENGE #141: STEP 4 INITIALIZED ===" # Trace statement start marker (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer to disk
        
        # Create a sample test file containing known byte content to verify byte extraction
        sample_file_handle = open(sample_filename, "wb") # Open sample test file for binary writing
        try:
            sample_content = "ABCDEFGHIJ1234567890KLMNOPQRST" # Define exact sample byte string (30 bytes)
            sample_file_handle.write(sample_content) # Write sample content to file
        finally:
            sample_file_handle.close()      # Ensure sample file handle is closed securely
            
        print "TRACE: Sample binary test file created with 30 bytes at %s" % sample_filename # Trace file creation step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        # Simulate command-line arguments requesting custom tail byte count of 12 bytes via -c flag
        simulated_args = ["tail.py", "-c", "12"] # Define simulated argument list with flag and value
        custom_bytes = parse_bytes_argument(simulated_args) # Parse custom byte count from arguments
        print "TRACE: Parsed custom byte count from arguments: %d" % custom_bytes # Trace parse step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        byte_results = extract_last_n_bytes(sample_filename, custom_bytes) # Extract custom last N bytes
        print "TRACE: Extracted last %d bytes successfully using custom argument" % len(byte_results) # Trace extraction step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        print "--- TAIL OUTPUT RESULTS (-c 12) ---" # Print header for tail output section
        sys.stdout.write(byte_results)      # Write extracted byte string directly to output stream
        print ""                            # Print newline separator
            
        print "=== STEP 4 EXECUTION COMPLETED SUCCESSFULLY ===" # Trace success completion marker (Rule #3)
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
    execution_result = run_step4_harness()  # Execute main harness orchestration function
    assert execution_result == True, "Main execution harness failed" # Final return assertion check (Rule #11)
