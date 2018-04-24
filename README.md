# KeyValueStorage

Use a dictionary for storage, the input key as the key, and a self defined structure StorageNode as the value. For every StorageNode, it has two variables, __values stores the current values for the key, and __shortcuts stores the current value of __values and the time whenever the __values's value is changed, representing the history.

Core service file is key_value_storage.py, and build it into web service through server.py and client.py, which use flask and falsk_restful.
To run the web service, use "pip install -r requirements.txt" in shell in the located folder to install required packets.

some assumptions:
* because some operations take too short time to make differences in time, we make time a counter inside the storage rather than using timestamp
* keys are unique, all input keys with the same value refer to the same one in the storage
* diff(key, time1, time2) will return the values in the value set at time2 but not in the value set at time1.
* For all operations except put, if the key doesn't exist in the storage, return None.
* for invalid operations, like wrong type of arguments, or invalid value of arguments, the operation will not make the timer added
* for client, the passed value should be identified with the spcific name, or else it will be ignored

.... for put service, url shoud be **/[key]**, passed value should be **{'value': [value]}**, method should be **put**

.... for get service, url shoud be **/[key]**, passed value should be **{'time': [time]}** or None, method should be **get**

.... for diff service, url shoud be **/[key]**, passed value should be **{'time1': [time1], 'time2': [time2]}**, method should be **get**

.... for delete service, url shoud be **/[key]**, passed value should be **{'value': [value]}** or None, method should be **delete**


# Methods
**put(key, value)**

**get(key[, t])**

**diff(key, time1, time2)**

**delete(key[, value])**
