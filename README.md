# seg4print 

This is a repository forked from [SynthSeg](https://github.com/BBillot/SynthSeg). We want to 3D print the brain regions for our scan. 

## Regular Workflow 

Please download the deep learning model [weights](https://mitprod-my.sharepoint.com/:u:/g/personal/bbillot_mit_edu/Ebqxo6YgUmBJkOML0m8NSXgBrhaHG7iqClFXRXPinS6FGw?e=DzKf1p) and paste the files to ./models folder.

We will only call CPUs in the regular workflow

## GPU Acceleration



Please download WSL2 in your Windows PowerShell by the following commands.

```powershell
wsl --version
wsl --install
wsl --update
```

Please download [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/) on Windows. 