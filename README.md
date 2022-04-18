[![Abcdspec-compliant](https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg)](https://github.com/brain-life/abcd-spec)
[![Run on Brainlife.io](https://img.shields.io/badge/Brainlife-brainlife.app.247-blue.svg)](https://doi.org/https://doi.org/10.25663/brainlife.app.247)

# Denoise SOS-reconstructed DWI data

This app will This app will denoise sum of squares reconstructed (SOS) dMRI data using tensorflow and pretrained model of SENSE reconstructed data. This uses a CNN to identify the increased noise from the SOS reconstruction by comparing the sequence to a SENSE reconstructed sequence from the same participant.

### Authors

- Brad Caron (bacaron@utexas.edu)
- Sophia Vinci-Booher (svinci@iu.edu)
- Hu Cheng (hucheng@iu.edu)

### Contributors

- Soichi Hayashi (shayashi@iu.edu)

### Funding Acknowledgement

brainlife.io is publicly funded and for the sustainability of the project it is helpful to Acknowledge the use of the platform. We kindly ask that you acknowledge the funding below in your publications and code reusing this code.

[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-1636893](https://img.shields.io/badge/NSF_BCS-1636893-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-ACI-1916518](https://img.shields.io/badge/NSF_ACI-1916518-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1916518)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://grantome.com/grant/NIH/R01-EB029272-01)

### Citations

We kindly ask that you cite the following articles when publishing papers and code using this code.

1. Avesani, P., McPherson, B., Hayashi, S. et al. The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services. Sci Data 6, 69 (2019). https://doi.org/10.1038/s41597-019-0073-y

#### MIT Copyright (c) 2020 brainlife.io The University of Texas at Austin and Indiana University

## Running the App

### On Brainlife.io

You can submit this App online at [https://doi.org/https://doi.org/10.25663/brainlife.app.247](https://doi.org/https://doi.org/10.25663/brainlife.app.247) via the 'Execute' tab.

### Running Locally (on your machine)

1. git clone this repo

2. Inside the cloned directory, create `config.json` with something like the following content with paths to your input files.

```json
{
	"dwi": "/input/dwi/dwi.nii.gz",
	"bvals": "/input/dwi/dwi.bvals",
	"bvecs": "/input/dwi/dwi.bvecs",
	"mask": "/input/brainmask/mask.nii.gz",
	"iters": 20000,
	"batch_size": 40000,
	"trainingSubj": "full_encode/subj1"
}
```

### Sample Datasets

You can download sample datasets from Brainlife using [Brainlife CLI](https://github.com/brain-life/cli).

```
npm install -g brainlife
bl login
mkdir input
bl dataset download
```

3. Launch the App by executing 'main'

```bash
./main
```

## Output

The main output of this App is a dwi datatype that has been denoised of the additional SOS-related noise.

#### Product.json

The secondary output of this app is `product.json`. This file allows web interfaces, DB and API calls on the results of the processing.

### Dependencies

This App only requires [singularity](https://www.sylabs.io/singularity/) to run. If you don't have singularity, you will need to install following dependencies.   

- tensorflow: https://www.tensorflow.org/
- python3: https://www.python.org/
- numpy: https://numpy.org/
- nibabel: https://nipy.org/nibabel/

#### MIT Copyright (c) 2020 brainlife.io The University of Texas at Austin and Indiana University
