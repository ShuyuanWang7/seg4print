# seg4print 

This is a repository forked from [SynthSeg](https://github.com/BBillot/SynthSeg). We want to 3D print the brain regions for our scan. 


# GPU 
## Preparation

Please download the deep learning model [weights](https://mitprod-my.sharepoint.com/personal/bbillot_mit_edu/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fbbillot%5Fmit%5Fedu%2FDocuments%2FSynthSeg%5Fmodels%2Ezip&parent=%2Fpersonal%2Fbbillot%5Fmit%5Fedu%2FDocuments&ga=1) and paste them to ./models folder.

Please download WSL2 in your Windows PowerShell by the following commands.

```powershell
wsl --version
wsl --install
wsl --update
```

Please download [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/) on Windows. 