First you need to have access to Llama3 models, to do so, simply request the access on huggingface, it takes hours to days to be granted access, then you follow the instructions given in huggingface on how to set up an authentification key on your profile.

Download the Llama3 8b model ( at least 4-5gb)

Preferably have anaconda installed on your PC (at least 8gb of RAM and a decent cpu)

Copy the folder to your directory

Go to Webapp subfolder, open app.py and edit line 28 to your actual directory of query_data.py
Go to populate_database.py and edit line 12 to your actual directory of DATA_PATH which is the "data" folder

After these steps are followed, open anaconda prompt and make sure you have a virtual environment created and started where you install the required libraries mentioned in the file requirements.txt, this is to avoid issues in your python installation, install them and then do "ollama start" without the quotes, this will start the Llama3 model, open another anaconda prompt, cd to the WebApp folder directory and type "python app.py", You will be given a url, paste it on your browser and you will be able to do queries and ask questions. 

# Create the database
first run populate_database.py to load and split the docs then create the database and populate it 
# Embedding 
the get_embedding_function sets up an embedding model for text data.
# Prompt_template and Ollama behaviour management
in the file query_data.py is set a prompt_template that the model would follow to treat the embedded data the way we want it to

##### the model that was used is Llama3"# amayaAG"
