# LSLMS

`pip install xfact-lm`

##

Large Scale Language Model Service

```
from xfact_lslms.client.lslms_client import LSMSClient

client = LSMSClient(username="", password="", model_name="")


print(client.call("Tell me about X", generate_kwargs={"max_length": 50}))                          
```