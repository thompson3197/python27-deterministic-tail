# -*- coding: utf-8 -*-
"""
Coding Challenge #141: Step 13 - Comprehensive Error Handling & Exit Status Codes
Python 2.7 Compliant Script with Strict Ground Rule Compliance
"""
import sys                                  # Import sys module for exit codes and streams
import os                                   # Import os module for path checking

MAX_LOOP_LIMIT = 1000                       # Constant: Fixed upper bound for loop limits (Rule #6)
EXIT_SUCCESS = 0                            # Constant: Exit code for successful execution (Rule #7)
EXIT_FILE_ERROR = 2                         # Constant: Exit code for file access errors (Rule #7)

def validate_exit_code(exit_code):
    # Function to validate integer exit code status range
    assert isinstance(exit_code, int), "Exit code must be an integer"         # Assertion 1: Validate input type (Rule #9, #11)
    assert exit_code >= 0 and exit_code <= 255, "Exit code must be between 0 and 255" # Assertion 2: Validate numeric range (Rule #9, #11)
    return True                                 # Return validation success status

def safe_open_target_file(file_path):
    # Function to securely open file with comprehensive error trapping and exit status mapping
    assert isinstance(file_path, str), "File path must be a string"              # Assertion 1: Validate input type (Rule #9, #11)
    assert len(file_path) > 0, "File path cannot be empty"                      # Assertion 2: Validate input length (Rule #9, #11)
    
    file_handle = None                      # Initialize file handle variable (Rule #7, #10)
    exit_status = EXIT_SUCCESS              # Initialize exit status code variable (Rule #10)
    
    try:
        if not os.path.exists(file_path):   # Check if file path exists before opening
            raise IOError(2, "No such file or directory: '%s'" % file_path) # Raise explicit file not found error
        file_handle = open(file_path, "r")  # Open target file for reading (Rule #11)
    except (IOError, OSError), err_obj:
        exit_status = EXIT_FILE_ERROR       # Map file error to non-zero exit status code
        sys.stderr.write("ERROR: Failed to open file '%s': %s\n" % (file_path, str(err_obj))) # Write error message to stderr stream
    
    assert isinstance(exit_status, int), "Exit status must evaluate to an integer" # Assertion 3: Validate return type (Rule #11)
    return (file_handle, exit_status)       # Return tuple containing file handle and exit code status

def run_step13_harness():
    # Main orchestration function for Step 13 execution and logging
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Retrieve absolute directory path of script (Rule #11)
    output_filename = os.path.join(script_dir, "tail_step13_output.txt") # Define absolute path for log output (Rule #2, #4)
    valid_filename = os.path.join(script_dir, "test_sample_step13.txt") # Define absolute path for valid test file
    missing_filename = os.path.join(script_dir, "non_existent_file.txt") # Define absolute path for missing test file
    
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
        print "=== CODING CHALLENGE #141: STEP 13 INITIALIZED ===" # Trace statement start marker (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer to disk
        
        # Create a valid sample test file
        valid_file_handle = open(valid_filename, "w") # Open valid sample file for writing
        try:
            valid_file_handle.write("Valid Test Content Line 1\n") # Write test line
        finally:
            valid_file_handle.close()       # Ensure valid file handle is closed securely
            
        print "TRACE: Valid sample test file created at %s" % valid_filename # Trace file creation step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        # Scenario 1: Test opening a valid file (Expect EXIT_SUCCESS)
        handle_v, status_v = safe_open_target_file(valid_filename) # Attempt to open valid file
        print "TRACE: Valid file open status code: %d" % status_v # Trace status code (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        if handle_v is not None:            # Check if file handle is valid
            handle_v.close()                # Close file handle securely
        assert status_v == EXIT_SUCCESS, "Valid file open expected success exit code" # Assertion check (Rule #9)
        
        # Scenario 2: Test opening a missing file (Expect EXIT_FILE_ERROR)
        handle_m, status_m = safe_open_target_file(missing_filename) # Attempt to open missing file
        print "TRACE: Missing file open status code: %d" % status_m # Trace status code (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        assert status_m == EXIT_FILE_ERROR, "Missing file open expected error exit code" # Assertion check (Rule #9)
        
        # Validate exit code helper function
        code_validation = validate_exit_code(status_m) # Validate exit code
        print "TRACE: Exit code validation status: %s" % str(code_validation) # Trace validation step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        assert code_validation == True, "Exit code validation failed" # Assertion check (Rule #9)
        
        print "--- ERROR HANDLING & EXIT CODES SUMMARY ---" # Print header for output section
        print "Success Exit Code: %d (Tested OK)" % status_v # Print success code result
        print "File Error Exit Code: %d (Tested OK)" % status_m # Print error code result
            
        print "=== STEP 13 EXECUTION COMPLETED SUCCESSFULLY ===" # Trace success completion marker (Rule #3)
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
    execution_result = run_step13_harness() # Execute main harness orchestration function
    assert execution_result == True, "Main execution harness failed" # Final return assertion check (Rule #11)
