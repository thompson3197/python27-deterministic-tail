# -*- coding: utf-8 -*-
"""
Coding Challenge #141: Step 0 - Environment & Input Verification Harness (Fixed Version)
Python 2.7 Compliant Script with Robust Version Validation & Absolute Paths
"""
import sys                                  # Import sys module for stream redirection
import os                                   # Import os module for path checking

MAX_LOOP_LIMIT = 100                        # Constant: Fixed upper bound for loop limits (Rule #6)
STATIC_BUFFER_SIZE = 1024                   # Constant: Static buffer size allocation (Rule #7)

def validate_environment(version_info):
    # Function to validate python runtime environment
    assert version_info is not None, "Version info cannot be None"              # Assertion 1 (Rule #9, #11)
    assert version_info[0] == 2, "Error: Python 2.x required"                   # Assertion 2 (Rule #9, #11)
    return True                                 # Return validation status

def verify_target_file(file_path):
    # Function to verify if target file exists and is readable
    assert isinstance(file_path, str), "File path must be a string"              # Assertion 1 (Rule #9, #11)
    assert len(file_path) > 0, "File path cannot be empty"                      # Assertion 2 (Rule #9, #11)
    
    file_exists = os.path.exists(file_path)     # Check if path exists in file system
    return file_exists                          # Return boolean existence status

def run_step0_harness():
    # Main orchestration function with absolute path alignment
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Get absolute directory of script (Rule #11)
    output_filename = os.path.join(script_dir, "tail_step0_output.txt")   # Absolute path for log file
    target_test_file = os.path.join(script_dir, "test_sample.txt")        # Absolute path for test file
    
    try:
        log_handle = open(output_filename, "w") # Open output file for static logging (Rule #7)
    except IOError, io_err:
        sys.stderr.write("FATAL: Could not open output file at %s: %s\n" % (output_filename, str(io_err)))
        return False                            # Return failure status
        
    original_stdout = sys.stdout                # Save original stdout stream
    original_stderr = sys.stderr                # Save original stderr stream
    
    sys.stdout = log_handle                     # Redirect standard output to file (Rule #2, #4)
    sys.stderr = log_handle                     # Redirect standard error to file (Rule #2, #4)
    
    try:
        print "=== CODING CHALLENGE #141: STEP 0 INITIALIZED ===" # Trace statement start (Rule #3)
        sys.stdout.flush()                      # Force immediate flush
        
        py_ver = sys.version_info               # Retrieve current python version object
        env_status = validate_environment(py_ver)# Validate runtime environment
        print "TRACE: Environment validation status: %s" % str(env_status) # Trace statement process (Rule #3)
        sys.stdout.flush()                      # Force flush output buffer
        assert env_status == True, "Environment validation failed"        # Assertion check (Rule #11)
        
        # Create a dummy test file statically using absolute path
        test_file_handle = open(target_test_file, "w") # Open test file for writing
        try:
            test_file_handle.write("Line 1: Alpha\n")  # Write test content line 1
            test_file_handle.write("Line 2: Bravo\n")  # Write test content line 2
            test_file_handle.write("Line 3: Charlie\n")# Write test content line 3
        finally:
            test_file_handle.close()            # Ensure test file handle is closed
            
        file_check = verify_target_file(target_test_file) # Verify target file accessibility
        print "TRACE: Target file verification status: %s" % str(file_check) # Trace process step (Rule #3)
        sys.stdout.flush()                      # Force flush output buffer
        assert file_check == True, "Target file verification failed"      # Assertion check (Rule #9, #11)
        
        # Bounded loop execution to verify static buffer initialization (Rule #6, #7)
        static_memory_array = [0] * STATIC_BUFFER_SIZE # Allocate static buffer array
        loop_counter = 0                        # Initialize loop counter variable (Rule #10)
        
        while loop_counter < 5 and loop_counter < MAX_LOOP_LIMIT: # Bounded loop with fixed limit (Rule #6)
            static_memory_array[loop_counter] = loop_counter * 10 # Populate array index
            print "TRACE: Static buffer index %d initialized with value %d" % (loop_counter, static_memory_array[loop_counter]) # Trace statement (Rule #3)
            sys.stdout.flush()                  # Force flush output buffer
            loop_counter += 1                   # Increment loop counter
            
        assert loop_counter == 5, "Loop counter did not complete expected iterations" # Assertion check (Rule #9)
        print "=== STEP 0 EXECUTION COMPLETED SUCCESSFULLY ===" # Trace statement output (Rule #3)
        sys.stdout.flush()                      # Force final flush
        return True                             # Return success status
        
    except Exception, err_inst:
        sys.stdout = original_stdout            # Restore stdout temporarily to print error
        sys.stderr = original_stderr
        print "CRITICAL ERROR: Exception caught during execution: %s" % str(err_inst)
        return False                            # Return failure status
        
    finally:
        sys.stdout = original_stdout            # Restore standard output stream
        sys.stderr = original_stderr            # Restore standard error stream
        log_handle.close()                      # Close log file handle safely

if __name__ == "__main__":
    execution_result = run_step0_harness()      # Invoke harness function
    assert execution_result == True, "Main execution harness failed" # Final return assertion (Rule #11)
