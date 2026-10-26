# -*- coding: utf-8 -*-
"""
Coding Challenge #141: Step 9 - File Descriptor Tracking vs. Name Tracking (-F)
Python 2.7 Compliant Script with Strict Ground Rule Compliance
"""
import sys                                  # Import sys module for stream redirection
import os                                   # Import os module for file status and path checking
import time                                 # Import time module for polling intervals

MAX_LOOP_LIMIT = 1000                       # Constant: Fixed upper bound for loop limits (Rule #6)
DEFAULT_RETRY_CYCLES = 3                    # Constant: Default number of simulation cycles (Rule #7)

def validate_descriptor_parameters(file_path, retry_cycles):
    # Function to validate name tracking and retry parameters
    assert isinstance(file_path, str), "File path must be a string"              # Assertion 1: Validate input type (Rule #9, #11)
    assert isinstance(retry_cycles, int), "Retry cycles must be an integer"       # Assertion 2: Validate input type (Rule #9, #11)
    assert retry_cycles >= 1, "Retry cycles must be at least 1"                   # Assertion 3: Validate numeric bounds (Rule #9, #11)
    return True                                 # Return validation success status

def simulate_rotation_and_name_tracking(file_path, retry_cycles):
    # Function to simulate file rotation handling and name-based re-opening (-F behavior)
    assert isinstance(file_path, str), "File path must be a string"              # Assertion 1: Validate input type (Rule #9, #11)
    assert isinstance(retry_cycles, int), "Retry cycles must be an integer"       # Assertion 2: Validate input type (Rule #9, #11)
    
    tracked_output_list = []                # Initialize output container list (Rule #7, #10)
    cycle_idx = 0                           # Initialize cycle iteration index variable (Rule #10)
    
    while cycle_idx < retry_cycles and cycle_idx < MAX_LOOP_LIMIT: # Bounded loop execution (Rule #6)
        time.sleep(0.1)                     # Pause briefly to simulate polling delay
        
        if os.path.exists(file_path):       # Check if target file currently exists on disk
            file_handle = open(file_path, "r") # Open existing file for reading (Rule #11)
            try:
                file_content = file_handle.read() # Read content from active file handle
                if len(file_content) > 0:   # Check if content was retrieved successfully
                    tracked_output_list.append("Cycle %d Read: %s" % (cycle_idx + 1, file_content.strip())) # Append read result
            finally:
                file_handle.close()         # Ensure file handle is closed securely
        else:
            tracked_output_list.append("Cycle %d: File missing or rotated" % (cycle_idx + 1)) # Log rotation event
            
        # Simulate file recreation / rotation on cycle 2
        if cycle_idx == 1:                  # Check if iteration matches rotation simulation trigger
            rotation_handle = open(file_path, "w") # Open file to truncate and recreate with new content
            try:
                rotation_handle.write("Rotated File Content\n") # Write new content post-rotation
            finally:
                rotation_handle.close()     # Ensure rotation file handle is closed securely
                
        cycle_idx += 1                      # Increment cycle iteration index variable
        
    assert len(tracked_output_list) <= retry_cycles * 2, "Output list exceeds expected bounds" # Assertion 3: Validate size bounds (Rule #9)
    assert isinstance(tracked_output_list, list), "Output must be a list"      # Assertion 4: Validate return type (Rule #11)
    return tracked_output_list              # Return list of tracked output events

def run_step9_harness():
    # Main orchestration function for Step 9 execution and logging
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Retrieve absolute directory path of script (Rule #11)
    output_filename = os.path.join(script_dir, "tail_step9_output.txt") # Define absolute path for log output (Rule #2, #4)
    sample_filename = os.path.join(script_dir, "test_sample_step9.txt") # Define absolute path for sample test file
    
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
        print "=== CODING CHALLENGE #141: STEP 9 INITIALIZED ===" # Trace statement start marker (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer to disk
        
        # Create initial test file
        init_handle = open(sample_filename, "w") # Open sample file for initial writing
        try:
            init_handle.write("Initial Pre-Rotation Content\n") # Write initial content
        finally:
            init_handle.close()             # Ensure initial file handle is closed securely
            
        print "TRACE: Initial sample test file created at %s" % sample_filename # Trace file creation step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        param_validation = validate_descriptor_parameters(sample_filename, DEFAULT_RETRY_CYCLES) # Validate parameters
        print "TRACE: Descriptor parameter validation status: %s" % str(param_validation) # Trace validation step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        assert param_validation == True, "Descriptor parameter validation failed" # Assertion check on validation (Rule #9)
        
        tracking_results = simulate_rotation_and_name_tracking(sample_filename, DEFAULT_RETRY_CYCLES) # Execute name-tracking simulation
        print "TRACE: Successfully simulated name tracking across %d cycles" % len(tracking_results) # Trace simulation step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        print "--- NAME TRACKING OUTPUT RESULTS (-F) ---" # Print header for output section
        print_idx = 0                       # Initialize print iteration index (Rule #10)
        while print_idx < len(tracking_results) and print_idx < MAX_LOOP_LIMIT: # Bounded loop for printing results (Rule #6)
            sys.stdout.write(tracking_results[print_idx] + "\n") # Write each tracked event directly to output stream
            print_idx += 1                  # Increment print iteration index variable
            
        print "=== STEP 9 EXECUTION COMPLETED SUCCESSFULLY ===" # Trace success completion marker (Rule #3)
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
    execution_result = run_step9_harness()  # Execute main harness orchestration function
    assert execution_result == True, "Main execution harness failed" # Final return assertion check (Rule #11)
