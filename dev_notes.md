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

C:\ProgramData\anaconda3
C:\ProgramData\anaconda3\Scripts
C:\ProgramData\anaconda3\Library\bin

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

Alright, now we’ve uncovered two issues at once:

1. ✅ Execution policy was fixed (`RemoteSigned` now allowed).
2. ❌ But your **profile file doesn’t exist at the path PowerShell is looking for**, so when you run `. $PROFILE`, it bombs out.

Let’s fix this cleanly:

---

### 🔧 Step 1: Create the missing profile file

Run:

```powershell
if (!(Test-Path -Path $PROFILE)) { New-Item -Type File -Path $PROFILE -Force }
```

That will create:
`C:\Users\m\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1`

---

### 🔧 Step 2: Edit the profile

Open it:

```powershell
notepad $PROFILE
```

Paste this inside (minimal, no auto-base activation):

```powershell
# >>> conda initialize >>>
& "C:\ProgramData\anaconda3\shell\condabin\conda-hook.ps1"
# <<< conda initialize <<<
```

⚠️ Double-check that your Anaconda path really is `C:\ProgramData\anaconda3` (from your logs, it is).

---

### 🔧 Step 3: Reload

Run:

```powershell
. $PROFILE
```

Then test:

```powershell
conda activate hijridatetimeenv
```


'''
