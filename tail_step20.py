# -*- coding: utf-8 -*-
"""
Coding Challenge #141: Step 20 - Advanced Extension 7: Comprehensive CLI Argument Parsing
Python 2.7 Compliant Script with Strict Ground Rule Compliance
"""
import sys                                  # Import sys module for stream redirection
import os                                   # Import os module for path checking

MAX_LOOP_LIMIT = 1000                       # Constant: Fixed upper bound for loop limits (Rule #6)
DEFAULT_LINE_COUNT = 5                      # Constant: Default fallback line count (Rule #7)

def parse_combined_arguments(arg_list):
    # Function to parse complex command-line argument lists into a structured configuration dictionary
    assert isinstance(arg_list, list), "Argument list must be a list"           # Assertion 1: Validate input type (Rule #9, #11)
    assert len(arg_list) < MAX_LOOP_LIMIT, "Argument list exceeds maximum bounds" # Assertion 2: Validate size bounds (Rule #9, #11)
    
    config_dict = {                         # Initialize configuration dictionary container (Rule #7, #10)
        "lines": DEFAULT_LINE_COUNT,        # Default line count option
        "sleep": 0.1,                       # Default sleep interval option
        "pattern": "",                      # Default grep filter pattern option
        "exclude": "",                      # Default exclusion pattern option
        "follow_name": False,               # Default name-tracking (-F) boolean flag
        "files": []                         # Default target file paths list container
    }
    
    arg_idx = 1                             # Initialize argument index starting past script name (Rule #10)
    total_args = len(arg_list)              # Calculate total number of arguments provided
    parse_counter = 0                       # Initialize parse loop counter variable (Rule #10)
    
    while arg_idx < total_args and parse_counter < MAX_LOOP_LIMIT: # Bounded loop execution (Rule #6)
        current_arg = arg_list[arg_idx]     # Retrieve current argument string item
        
        if current_arg == "-n" or current_arg == "--lines": # Check for line count flag
            assert arg_idx + 1 < total_args, "Missing value for lines argument flag" # Assertion check for value existence (Rule #9, #11)
            config_dict["lines"] = int(arg_list[arg_idx + 1]) # Parse and assign line count integer
            arg_idx += 2                    # Advance index past flag and value
        elif current_arg == "-s" or current_arg == "--sleep-interval": # Check for sleep interval flag
            assert arg_idx + 1 < total_args, "Missing value for sleep argument flag" # Assertion check for value existence (Rule #9, #11)
            config_dict["sleep"] = float(arg_list[arg_idx + 1]) # Parse and assign sleep interval float
            arg_idx += 2                    # Advance index past flag and value
        elif current_arg == "-e" or current_arg == "--grep": # Check for grep pattern flag
            assert arg_idx + 1 < total_args, "Missing value for pattern argument flag" # Assertion check for value existence (Rule #9, #11)
            config_dict["pattern"] = arg_list[arg_idx + 1] # Parse and assign pattern string
            arg_idx += 2                    # Advance index past flag and value
        elif current_arg == "-x" or current_arg == "--exclude": # Check for exclusion flag
            assert arg_idx + 1 < total_args, "Missing value for exclude argument flag" # Assertion check for value existence (Rule #9, #11)
            config_dict["exclude"] = arg_list[arg_idx + 1] # Parse and assign exclusion string
            arg_idx += 2                    # Advance index past flag and value
        elif current_arg == "-F":           # Check for follow-by-name flag
            config_dict["follow_name"] = True # Set follow-by-name boolean flag to True
            arg_idx += 1                    # Advance index past boolean flag
        else:
            config_dict["files"].append(current_arg) # Append positional argument to target files list
            arg_idx += 1                    # Advance index past positional file path
            
        parse_counter += 1                  # Increment parse loop counter variable
        
    assert isinstance(config_dict, dict), "Configuration result must be a dictionary" # Assertion 3: Validate return type (Rule #11)
    assert "files" in config_dict, "Configuration dictionary missing files key" # Assertion 4: Validate dictionary structure (Rule #9, #11)
    return config_dict                      # Return populated configuration dictionary

def validate_configuration(config_dict):
    # Function to validate parsed configuration option parameters and bounds
    assert isinstance(config_dict, dict), "Configuration parameter must be a dictionary" # Assertion 1: Validate input type (Rule #9, #11)
    assert "lines" in config_dict, "Config missing lines key"                   # Assertion 2: Validate structure (Rule #9, #11)
    
    assert config_dict["lines"] >= 0, "Line count cannot be negative"           # Assertion 3: Validate numeric bounds (Rule #9, #11)
    assert isinstance(config_dict["files"], list), "Files entry must be a list" # Assertion 4: Validate file list type (Rule #9, #11)
    return True                                 # Return validation success status

def run_step20_harness():
    # Main orchestration function for Step 20 execution and logging
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Retrieve absolute directory path of script (Rule #11)
    output_filename = os.path.join(script_dir, "tail_step20_output.txt") # Define absolute path for log output (Rule #2, #4)
    sample_filename = os.path.join(script_dir, "test_sample_step20.txt") # Define absolute path for sample test file
    
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
        print "=== CODING CHALLENGE #141: STEP 20 INITIALIZED (ADVANCED EXTENSION 7) ===" # Trace statement start marker (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer to disk
        
        # Simulate complex command-line invocation combining multiple flags and target file path
        simulated_cli_args = ["tail.py", "-n", "3", "-s", "0.2", "-e", "INFO", "-F", sample_filename] # Assemble simulated arguments list
        parsed_config = parse_combined_arguments(simulated_cli_args) # Parse combined argument list
        print "TRACE: Successfully parsed combined CLI argument flags" # Trace parsing step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        is_config_valid = validate_configuration(parsed_config) # Validate parsed configuration dictionary
        print "TRACE: Configuration validation status: %s" % str(is_config_valid) # Trace validation step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        assert is_config_valid == True, "Configuration validation check failed" # Assertion check on validation (Rule #9)
        
        print "--- PARSED CONFIGURATION SUMMARY ---" # Print header for summary section
        print "Lines Count (-n): %d" % parsed_config["lines"] # Print parsed lines count
        print "Sleep Interval (-s): %.1f" % parsed_config["sleep"] # Print parsed sleep interval
        print "Grep Pattern (-e): %s" % parsed_config["pattern"] # Print parsed grep pattern
        print "Exclude Pattern (-x): %s" % (parsed_config["exclude"] if parsed_config["exclude"] else "[None]") # Print parsed exclusion pattern
        print "Follow Name Flag (-F): %s" % str(parsed_config["follow_name"]) # Print parsed follow-by-name boolean flag
        print "Target Files: %s" % str(parsed_config["files"]) # Print target files list
            
        print "=== STEP 20 EXECUTION COMPLETED SUCCESSFULLY ===" # Trace success completion marker (Rule #3)
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
    execution_result = run_step20_harness() # Execute main harness orchestration function
    assert execution_result == True, "Main execution harness failed" # Final return assertion check (Rule #11)
