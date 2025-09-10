import os
import shutil

def remove_egg_info_recursively(root="."):
    """
    Recursively remove all directories ending with `.egg-info` starting from `root`.
    """
    for dirpath, dirnames, _ in os.walk(root):
        # Make a copy of dirnames because we may modify it while iterating
        for dirname in dirnames[:]:
            if dirname.endswith(".egg-info"):
                full_path = os.path.join(dirpath, dirname)
                print(f"Removing {full_path}/ ...")
                shutil.rmtree(full_path)
                # remove from dirnames so os.walk doesn't descend into it
                dirnames.remove(dirname)

def remove_pycache(root_folder):
    for root, dirs, files in os.walk(root_folder):
        for d in dirs:
            if d == "__pycache__":
                cache_path = os.path.join(root, d)
                try:
                    shutil.rmtree(cache_path)
                    print(f"[REMOVED] {cache_path}")
                except Exception as e:
                    print(f"[ERROR]   {cache_path} -> {e}")

def clean_build_dirs():
    """
    Remove build artifact directories if they exist:
    - dist/
    - any *.egg-info directory
    """
    # Always check 'dist'
    if os.path.exists("dist"):
        print("Removing dist/ ...")
        shutil.rmtree("dist")
    else:
        print("dist/ not found, skipping.")
        
    # Always check '.pytest_cache'
    if os.path.exists(".pytest_cache"):
        print("Removing dist/ ...")
        shutil.rmtree(".pytest_cache")
    else:
        print(".pytest_cache/ not found, skipping.")    
    

    remove_egg_info_recursively()
    
    folder_to_clean = "."   # current folder, change if needed
    remove_pycache(folder_to_clean)


if __name__ == "__main__":
    clean_build_dirs()


'''
deactivate

# Create environment (called .venv here)
python -m venv .venv

# Activate it
# On Linux/macOS:
source .venv/bin/activate

# On Windows (PowerShell):
.venv\Scripts\Activate.ps1


pip install virtualenv
virtualenv myenv
source myenv/bin/activate   # Linux/macOS
myenv\Scripts\activate      # Windows



conda create -n hijridatetimeenv python=3.8.2
#                                                                                                                                                                                  
# To activate this environment, use     
# conda init                                                                                                                                           
#                                                                                                                                                                                  
#     $ conda activate hijridatetimeenv
#
# To deactivate an active environment, use
#
#     $ conda deactivate

# python -m build

# twine upload --repository testpypi dist/*


# Make a small commit (even just updating a comment)
git add .
git config --global --add safe.directory E:/GitHub/hijri-datetime
git add .
git commit -m "Bump version for new release"

# Rebuild - this will create a version like 0.0.1.dev1+g1234567
python -m build

git tag v0.2.0
git push origin v0.2.0
python -m build
twine upload dist/*

# 5. Install development dependencies
pip install -e ".[dev]"

# 6. Set up pre-commit hooks
pre-commit install

# 7. Run initial tests
pytest

# 8. Build the package
python -m build

# 9. Check the package
twine check dist/*



'''
