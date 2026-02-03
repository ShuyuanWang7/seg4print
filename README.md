# seg4print 

This is a repository forked from [SynthSeg](https://github.com/BBillot/SynthSeg). We, the [Edden et al.](https://www.gabamrs.com/) at Hopkins, want to 3D print the well-segmented brain regions for our scans. 

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

Please download [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/) on Windows. This helps you get an isolated environment to run the tensorflow-based code. Then launch your PowerShell and activate your WSL2 by

```powershell
wsl
```

Then go to your local address to this repository and create a new Docker image using our configuration. You can customize `name:tag` for your image and remember to keep it consistent in the following commands. 

```powershell
cd your/address/to/seg4print
docker build -t name:tag .
```

After a successful installment of your image, we will launch a container for that. Remember your ```seg4print``` folder should always be the workspace for the container, so always go to the address first. 

```powershell
cd your/address/to/seg4print
docker run --gpus all -it --rm -v "${PWD}:/workspace" -w /workspace name:tag bash
```

Inside your container, now run the model. 

```powershell
python ./scripts/commands/SynthSeg_predict.py --i ./input.nii --o ./output.nii --fast --crop 160 192 160
```

If you get a slow processing, here are someways to help you monitor the device.
<br>

GPU
```powershell
nvidia-smi -l 1
```

CPU
```powershell
htop
```