First you need to have access to llama3 models, to do so, simply request the access on huggingface, it takes hours to days to be granted access, then you follow the instructions given in huggingface on how to set up an authentification key on your profile.
Download the llama3 8b model ( approximately 5gb)
Preferably have anaconda installed on your PC
Copy the folder to your directory
After these steps are followed, open anaconda prompt and make sure you have a virtual environment where you install the required libraries mentioned in the file requirements.txt, install them and then do "ollama start" without the quotes, this will start the llama3 model, open another anaconda prompt, change to the WebApp folder directory and type python app.py. You will be given a url, paste it on your browser and you will be able to do queries and ask questions. 
# Create the database
first run populate_database.py to load and split the docs then create the database and populate it 
# Embedding 
the get_embedding_function sets up an embedding model for text data.
#  Prompt_template and Ollama behaviour management
in the file query_data.py we will set a prompt_template that the model would follow to treat the embedded data as we want it to


##### the model that was used is llama3"# amayaAG" 
