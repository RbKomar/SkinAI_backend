# Project Setup

## Prerequisites

- Python (3.7 or newer recommended)
- pip (Python package manager)
- Virtual environment (optional but recommended)

## Setting up the environment

1. (Optional) Create a virtual environment:
   ```
   python -m venv venv_name
   .\venv_name\Scripts\Activate  # On Windows
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. If you have additional packages installed that are not in `requirements.txt`, you can remove them using:
   ```powershell
   # Get the list of currently installed packages
   $installed = (pip freeze) -split "`n"
   
   # Get the list of required packages from requirements.txt
   $required = Get-Content requirements.txt
   
   # Identify packages that are installed but not required
   $to_uninstall = $installed | Where-Object { $_ -notin $required -and $_ -notmatch '^#|^-' }
   
   # Uninstall the unnecessary packages
   if ($to_uninstall) {
       pip uninstall -y $to_uninstall
   }
   
   # Install the required packages
   pip install -r requirements.txt

## Running the application

- Provide steps specific to your application.

## Testing

1. Run the tests:
   ```bash
   pytest
   ```

## Common PowerShell Commands

1. Activate a virtual environment:
   ```powershell
   .\venv_name\Scripts\Activate
   ```
   Deactivate with:
   ```powershell
   deactivate
   ```

2. List files in the current directory:
   ```powershell
   Get-ChildItem
   ```

3. Create a new directory:
   ```powershell
   New-Item -ItemType Directory -Name directory_name
   ```

4. Remove a directory:
   ```powershell
   Remove-Item directory_name -Recurse
   ```

5. Move files or directories:
   ```powershell
   Move-Item source destination
   ```

6. Delete a file:
   ```powershell
   Remove-Item file_name
   ```

