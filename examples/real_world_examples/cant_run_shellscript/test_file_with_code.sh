#!/usr/bin/env b‬ash

# It contains various characters and strings to test the functionality of the script.
# This script contains a Zero Width Space (​) and other special characters that change 
# the script behavior. The scanning process should be able to detect and remove these characters,
# ensuring that the output is clean and free of any unwanted characters, bringing the
# shell script execution to a expected behavior.

function bad_function {
    # This function have intentionally the behavior changed with a "ghost" character to
    # demonstrate one of the issues that can occur when special characters are present in a script.

    # The presence of this character can cause the script to behave unexpectedly.
    # For example, the following line should print "Hello, World!" but may not work as expected.
    local var=‬"Hello, World!"

    echo "$var" || return 1

    loca‬l v‬ar2=‬"This is a test string with a Zero Width Space (​) character."

    # The presence of this character can cause the script to behave unexpectedly.
    # For example, the following line should print "This is a test string with a Zero Width Space (​) character."

    echo "$var2" || return 1
}

bad_function