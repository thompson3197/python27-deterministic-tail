# -*- coding: utf-8 -*-
"""
Coding Challenge #141: Step 6 - Quiet Mode (-q) and Verbose Mode (-v)
Python 2.7 Compliant Script with Strict Ground Rule Compliance
"""
import sys                                  # Import sys module for stream redirection
import os                                   # Import os module for path checking

MAX_LOOP_LIMIT = 1000                       # Constant: Fixed upper bound for loop limits (Rule #6)
DEFAULT_LINE_COUNT = 3                      # Constant: Default fallback line count per file (Rule #7)

def parse_verbosity_flags(arg_list):
    # Function to parse quiet or verbose flags from argument list
    assert isinstance(arg_list, list), "Argument list must be a list"           # Assertion 1: Validate input type (Rule #9, #11)
    assert len(arg_list) < MAX_LOOP_LIMIT, "Argument list exceeds maximum bounds" # Assertion 2: Validate size bounds (Rule #9, #11)
    
    verbosity_mode = "default"              # Initialize verbosity mode string (Rule #10)
    arg_idx = 0                             # Initialize argument iteration index variable (Rule #10)
    
    while arg_idx < len(arg_list) and arg_idx < MAX_LOOP_LIMIT: # Bounded loop execution (Rule #6)
        current_arg = arg_list[arg_idx]     # Retrieve current argument string from list
        if current_arg == "-q" or current_arg == "--quiet": # Check for quiet flag identifier
            verbosity_mode = "quiet"        # Set mode to quiet suppression
            break                           # Exit loop once flag is processed
        elif current_arg == "-v" or current_arg == "--verbose": # Check for verbose flag identifier
            verbosity_mode = "verbose"      # Set mode to verbose forced headers
            break                           # Exit loop once flag is processed
        arg_idx += 1                        # Increment argument iteration index variable
        
    assert isinstance(verbosity_mode, str), "Verbosity mode must evaluate to a string" # Assertion 3: Validate return type (Rule #11)
    assert verbosity_mode in ["default", "quiet", "verbose"], "Invalid verbosity mode state" # Assertion 4: Validate state bounds (Rule #9, #11)
    return verbosity_mode                   # Return validated verbosity mode string

def determine_header_visibility(file_count, verbosity_mode):
    # Function to determine whether file headers should be displayed based on file count and flags
    assert isinstance(file_count, int), "File count must be an integer"          # Assertion 1: Validate input type (Rule #9, #11)
    assert isinstance(verbosity_mode, str), "Verbosity mode must be a string"   # Assertion 2: Validate input type (Rule #9, #11)
    
    show_header = False                     # Initialize header visibility boolean flag (Rule #10)
    
    if verbosity_mode == "quiet":           # Check if quiet mode flag is active
        show_header = False                 # Quiet mode suppresses headers completely
    elif verbosity_mode == "verbose":       # Check if verbose mode flag is active
        show_header = True                  # Verbose mode forces headers on
    else:
        if file_count > 1:                  # Default mode shows headers only for multiple files
            show_header = True              # Enable headers for multiple files
        else:
            show_header = False             # Disable headers for single file
            
    assert isinstance(show_header, bool), "Header visibility must evaluate to a boolean" # Assertion 3: Validate return type (Rule #11)
    assert file_count >= 1, "File count must be at least 1"                     # Assertion 4: Validate numeric range (Rule #9, #11)
    return show_header                      # Return validated header visibility boolean

def read_file_lines(file_path):
    # Function to read all lines from a target file into a list with strict bounding
    assert isinstance(file_path, str), "File path must be a string"              # Assertion 1: Validate input type (Rule #9, #11)
    assert len(file_path) > 0, "File path cannot be empty"                      # Assertion 2: Validate input length (Rule #9, #11)
    
    line_storage_list = []                  # Initialize static line storage list (Rule #7, #10)
    file_handle = open(file_path, "r")      # Open target file for reading (Rule #11)
    try:
        read_counter = 0                    # Initialize read loop counter variable (Rule #10)
        line_item = file_handle.readline()  # Read first line from file handle
        
        while line_item and read_counter < MAX_LOOP_LIMIT: # Bounded loop with fixed upper limit (Rule #6)
            line_storage_list.append(line_item) # Append read line to storage list
            read_counter += 1               # Increment read loop counter variable
            line_item = file_handle.readline() # Read next line from file handle
            
        assert read_counter < MAX_LOOP_LIMIT, "File read exceeded maximum loop bounds" # Assertion check on loop completion (Rule #9)
    finally:
        file_handle.close()                 # Ensure file handle is closed securely
        
    assert isinstance(line_storage_list, list), "Storage list must be of type list" # Assertion 3: Validate return type (Rule #11)
    return line_storage_list                # Return populated lines list

def process_tail_with_verbosity(file_paths_list, target_lines_count, verbosity_mode):
    # Function to process files and format output incorporating quiet/verbose rules
    assert isinstance(file_paths_list, list), "File paths list must be a list"    # Assertion 1: Validate input type (Rule #9, #11)
    assert isinstance(target_lines_count, int), "Target lines count must be int"  # Assertion 2: Validate input type (Rule #9, #11)
    assert isinstance(verbosity_mode, str), "Verbosity mode must be a string"   # Assertion 3: Validate input type (Rule #9, #11)
    
    formatted_output_list = []              # Initialize formatted output container list (Rule #7, #10)
    total_files = len(file_paths_list)      # Calculate total number of files to process
    show_headers = determine_header_visibility(total_files, verbosity_mode) # Determine header rule
    
    file_idx = 0                            # Initialize file iteration index variable (Rule #10)
    while file_idx < total_files and file_idx < MAX_LOOP_LIMIT: # Bounded loop for files (Rule #6)
        current_path = file_paths_list[file_idx] # Retrieve current file path string
        file_basename = os.path.basename(current_path) # Extract base filename for header display
        
        if file_idx > 0 and show_headers:   # Check if preceding file output requires separator spacing
            formatted_output_list.append("\n") # Append blank line separator between files
            
        if show_headers:                    # Check if headers are enabled for this run
            header_string = "==> %s <==\n" % file_basename # Format standard tail header string
            formatted_output_list.append(header_string) # Append header string to output list
            
        file_lines = read_file_lines(current_path) # Read all lines from current file
        total_lines = len(file_lines)       # Calculate total lines in file
        
        start_index = total_lines - target_lines_count # Calculate starting index for tail extraction
        if start_index < 0:                 # Check if requested count exceeds total lines
            start_index = 0                 # Clamp start index to zero if file is smaller than N
            
        line_loop_idx = start_index         # Initialize line iteration index variable (Rule #10)
        extraction_counter = 0              # Initialize extraction counter variable (Rule #10)
        
        while line_loop_idx < total_lines and extraction_counter < MAX_LOOP_LIMIT: # Bounded inner loop (Rule #6)
            formatted_output_list.append(file_lines[line_loop_idx]) # Append tail line to output list
            line_loop_idx += 1              # Increment line iteration index variable
            extraction_counter += 1         # Increment extraction counter variable
            
        file_idx += 1                       # Increment file iteration index variable
        
    assert isinstance(formatted_output_list, list), "Output list must be of type list" # Assertion 4: Validate return type (Rule #11)
    return formatted_output_list            # Return fully formatted output list

def run_step6_harness():
    # Main orchestration function for Step 6 execution and logging
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Retrieve absolute directory path of script (Rule #11)
    output_filename = os.path.join(script_dir, "tail_step6_output.txt") # Define absolute path for log output (Rule #2, #4)
    file_single_path = os.path.join(script_dir, "test_sample_single.txt") # Define absolute path for single test file
    
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
        print "=== CODING CHALLENGE #141: STEP 6 INITIALIZED ===" # Trace statement start marker (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer to disk
        
        # Create single sample test file containing 5 lines
        file_single_handle = open(file_single_path, "w") # Open single sample file for writing
        try:
            write_idx = 1                   # Initialize write index for single file (Rule #10)
            while write_idx <= 5 and write_idx < MAX_LOOP_LIMIT: # Bounded loop for single file (Rule #6)
                file_single_handle.write("Single File Line %d\n" % write_idx) # Write line to single file
                write_idx += 1              # Increment write index variable
        finally:
            file_single_handle.close()      # Ensure single file handle is closed securely
            
        print "TRACE: Created single sample file successfully" # Trace creation step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        # Simulate command-line arguments requesting verbose mode (-v) on a single file
        simulated_args = ["tail.py", "-v", "test_sample_single.txt"] # Define simulated argument list with verbose flag
        parsed_verbosity = parse_verbosity_flags(simulated_args) # Parse verbosity mode from arguments
        print "TRACE: Parsed verbosity mode from arguments: %s" % parsed_verbosity # Trace parse step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        target_files_list = [file_single_path] # Assemble single file list
        verbose_results = process_tail_with_verbosity(target_files_list, DEFAULT_LINE_COUNT, parsed_verbosity) # Process with verbose mode
        print "TRACE: Processed tail with verbosity successfully (%d output lines generated)" % len(verbose_results) # Trace processing step (Rule #3)
        sys.stdout.flush()                  # Force flush output buffer
        
        print "--- VERBOSE TAIL OUTPUT RESULTS (-v single file) ---" # Print header for output section
        print_idx = 0                       # Initialize print iteration index (Rule #10)
        while print_idx < len(verbose_results) and print_idx < MAX_LOOP_LIMIT: # Bounded loop for printing results (Rule #6)
            sys.stdout.write(verbose_results[print_idx]) # Write each formatted item directly to output stream
            print_idx += 1                  # Increment print iteration index variable
            
        print "=== STEP 6 EXECUTION COMPLETED SUCCESSFULLY ===" # Trace success completion marker (Rule #3)
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
    execution_result = run_step6_harness()  # Execute main harness orchestration function
    assert execution_result == True, "Main execution harness failed" # Final return assertion check (Rule #11)
