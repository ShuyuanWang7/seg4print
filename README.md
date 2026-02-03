# seg4print 

This is a repository forked from [SynthSeg](https://github.com/BBillot/SynthSeg). We want to 3D print the brain regions for our scan. 

## Regular Workflow 

Please download the deep learning model [weights](https://mitprod-my.sharepoint.com/:u:/g/personal/bbillot_mit_edu/Ebqxo6YgUmBJkOML0m8NSXgBrhaHG7iqClFXRXPinS6FGw?e=DzKf1p) and paste the files to ./models folder.

We will only call CPUs in the regular workflow to make this workflow as realizable as possible. 

## GPU Acceleration

(The GPU workflow is only verified on Windows so far.)
<br>
(We noticed that GPU mode only supports one CPU core to do the pre/post processing, and hence the workflow is slowed down. There will be an update as soon as we fixed it.)

Please download the deep learning model [weights](https://mitprod-my.sharepoint.com/:u:/g/personal/bbillot_mit_edu/Ebqxo6YgUmBJkOML0m8NSXgBrhaHG7iqClFXRXPinS6FGw?e=DzKf1p) and paste the files to ./models folder.

Please download WSL2 in your Windows PowerShell by the following commands. This will help you create a lightweight Ubuntu in your Windows system. 

```powershell
wsl --version
wsl --install
wsl --update
```

Please download [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/) on Windows. 