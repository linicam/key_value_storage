# KeyValueStorage

Use a dictionary for storage, the input key as the key, and a self defined structure StorageNode as the value. For every StorageNode, it has two variables, __values stores the current values for the key, and __shortcuts stores the current value of __values and the time whenever the __values's value is changed, representing the history.

Core service file is key_value_storage.py, and build it into web service through server.py and client.py, which use flask and falsk_restful.
To run the web service, use "pip install -r requirements.txt" in shell in the located folder to install required packets.

some assumptions:
* keys are unique, no duplicated username
* diff(key, time1, time2) will return the values in the value set at time2 but not in the value set at time1.
* For all operations except put, if the key doesn't exist in the storage, return None.