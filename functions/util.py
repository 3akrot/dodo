import os
def is_within_dir(working_directory, directory):
    wd_absloute_path = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(wd_absloute_path, directory))
    valid_working_dir = (
        os.path.commonpath([wd_absloute_path, target_dir]) == wd_absloute_path
    )
    return valid_working_dir