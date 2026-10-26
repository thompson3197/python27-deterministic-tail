# -*- coding: utf-8 -*-
"""
Coding Challenge #141: Step 10 - Sleep Interval Handling (-s / --sleep-interval)
Python 2.7 Compliant Script with Strict Ground Rule Compliance
"""
import sys                                  # Import sys module for stream redirection
import os                                   # Import os module for path checking
import time                                 # Import time module for interval sleeping

MAX_LOOP_LIMIT = 1000                       # Constant: Fixed upper bound for loop limits (Rule #6)
DEFAULT_SLEEP_INTERVAL = 0.1                # Constant: Default fallback sleep interval in seconds (Rule #7)

def parse_sleep_interval(arg_list):
    # Function to parse custom sleep interval from argument list simulating -s / --sleep-interval flags
    assert isinstance(arg_list, list), "Argument list must be a list"           # Assertion 1: Validate input type (Rule #9, #11)
    assert len(arg_list) < MAX_LOOP_LIMIT, "Argument list exceeds maximum bounds" # Assertion 2: Validate size bounds (Rule #9, #11)
    
    parsed_interval = DEFAULT_SLEEP_INTERVAL # Initialize parsed interval with default value (Rule #10)
    arg_idx = 0                             # Initialize argument iteration index variable (Rule #10)
    
    while arg_idx < len(arg_list) and arg_idx < MAX_LOOP_LIMIT: # Bounded loop execution (Rule #6)
        current_arg = arg_list[arg_idx]     # Retrieve current argument string from list
        if current_arg == "-s" or current_arg == "--sleep-interval": # Check for sleep interval flag identifier
            assert arg_idx + 1 < len(arg_list), "Missing value following sleep interval flag" # Assertion check for flag value existence (Rule #9, #11)
            value_arg = arg_list[arg_idx + 1] # Retrieve value argument following the flag
            parsed_interval = float(value_arg) # Convert value string to float sleep interval
            break                           # Exit loop once flag and value are processed
        arg_idx += 1                        # Increment argument iteration index variable
        
    assert isinstance(parsed_interval, (int, float)), "Parsed interval must be numeric" # Assertion 3: Validate return type (Rule #11)
    assert parsed_interval > 0.0, "Parsed interval must be greater than zero"   # Assertion 4: Validate numeric range (Rule #9, #11)
    return parsed_interval                  # Return validated sleep interval float

def simulate_interval_polling(sleep_duration, test_cycles):
    # Function to execute bounded polling simulation utilizing the specified sleep interval
    assert isinstance(sleep_duration, (int, float)), "Sleep duration must be numeric" # Assertion 1: Validate input type (Rule #9, #11)
    assert isinstance(test_cycles, int), "Test cycles must be an integer"       # Assertion 2: Validate input type (Rule #9, #11)
    assert sleep_duration > 0.0, "Sleep duration must be greater than zero"     # Assertion 3: Validate numeric bounds (Rule #9, #11)
    
    timing_log_list = []                    # Initialize timing log container list (Rule #7, #10)
    cycle_idx = 0                           # Initialize cycle iteration index variable (Rule #10)
    
    while cycle_idx < test_cycles and cycle_idx < MAX_LOOP_LIMIT: # Bounded loop execution (Rule #6)
        start_timestamp = time.time()       # Record start timestamp prior to sleep
        time.sleep(sleep_duration)          # Pause execution for the configured sleep interval duration
        end_timestamp = time.time()         # Record end timestamp following sleep pause
        elapsed_time = end_timestamp - start_timestamp # Calculate actual elapsed pause duration
        
        log_entry = "Cycle %d: Slept for %.4f seconds" % (cycle_idx + 1, elapsed_time) # Format log entry string
        timing_log_list.append(log_entry)   # Append log entry to list container
        cycle_idx += 1                      # Increment cycle iteration index variable
        
    assert len(timing_log_list) == test_cycles, "Timing log length must match cycle count" # Assertion 4: Validate list size (Rule #9)
    assert isinstance(timing_log_list, list), "Timing log must be a list"       # Assertion 5: Validate return type (Rule #11)
    return timing_log_list                  # Return completed timing log list

def run_step10_harness():
    # Main orchestration function for Step 10 execution and logging
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Retrieve absolute directory path of script (Rule #11)
    output_filename = os.path.join(script_dir, "tail_step10_output.txt") # Define absolute path for log output (Rule #2, #4)
    
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
        print "=== CODING CHALLENGE #141: STEP 10 INITIALIZED ===" # Trace statement start marker (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer to disk
        
        # Simulate command-line arguments requesting custom sleep interval of 0.05 seconds via -s flag
        simulated_args = ["tail.py", "-s", "0.05"] # Define simulated argument list with flag and value
        parsed_interval = parse_sleep_interval(simulated_args) # Parse custom sleep interval from arguments
        print "TRACE: Parsed sleep interval from arguments: %.2f seconds" % parsed_interval # Trace parse step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        simulation_cycles = 3               # Define number of test cycles to simulate
        polling_results = simulate_interval_polling(parsed_interval, simulation_cycles) # Execute interval polling simulation
        print "TRACE: Successfully completed %d interval polling cycles" % len(polling_results) # Trace simulation step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        print "--- SLEEP INTERVAL OUTPUT RESULTS (-s 0.05) ---" # Print header for output section
        print_idx = 0                       # Initialize print iteration index (Rule #10)
        while print_idx < len(polling_results) and print_idx < MAX_LOOP_LIMIT: # Bounded loop for printing results (Rule #6)
            sys.stdout.write(polling_results[print_idx] + "\n") # Write each timing log entry directly to output stream
            print_idx += 1                  # Increment print iteration index variable
            
        print "=== STEP 10 EXECUTION COMPLETED SUCCESSFULLY ===" # Trace success completion marker (Rule #3)
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
    execution_result = run_step10_harness() # Execute main harness orchestration function
    assert execution_result == True, "Main execution harness failed" # Final return assertion check (Rule #11)
