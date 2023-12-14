#Mansoorali Amiri
import os
import comet_ml

def get_comet_model(model_name, model_path, download=1, workspace="morph-e", model_version=None):
    # Read the COMET_API_KEY from the system environment
    comet_api_key = os.getenv('COMET_KEY')
    if not comet_api_key:
        raise ValueError("COMET_API_KEY is not set in the environment")

    # Initialize the Comet API
    comet_api = comet_ml.API(api_key=comet_api_key)

    # Download the model
    if download:
        details = comet_api.download_registry_model(workspace, model_name, model_version, output_path=model_path)
    else:
        details = comet_api.get_registry_model_details(workspace, model_name, model_version)
    
    # Extract the file name from the details
    file_name = details['versions'][0]['assets'][0]['fileName']

    # Store the model details (optional, depending on your requirement)
    # ... (store the details as needed)

    return file_name
