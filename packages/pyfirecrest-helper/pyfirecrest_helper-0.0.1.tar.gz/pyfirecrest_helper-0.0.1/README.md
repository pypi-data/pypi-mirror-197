# Introduction 
Helper for using CSCS's [pyfireCREST](https://github.com/eth-cscs/pyfirecrest)


**Under construction!**

Quick start

python3 -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org pyfirecrest_helper
- You need a client id and a client secret to use the API. These can be obtained from CSCS here: https://oidc-dashboard-prod.cscs.ch/ This can be put in a file called `secrets.json` file that will look something like this (replace the client_id and client_secret with the information you have obtained from the CSCS site):
```
{
    "client_id" : "firecrest-jgustavs-mycomputer",
    "client_secret": "qpfKkEaHCwwmeC0vmysecretforfirecrest",
    "token_uri" : "https://auth.cscs.ch/auth/realms/firecrest-clients/protocol/openid-connect/token"
}
```
## give the location of your certs 
export REQUESTS_CA_BUNDLE=/usr/local/share/ca-certificates/BIT_Proxy_Root_CA_01.crt
pyfirecrest_helper --list -a daint -t /store/2go/go30/JAG_test/
pyfirecrest_helper --download -a daint -s /store/2go/go30/JAG_test/20211212_121543.jpg
pyfirecrest_helper --upload -a daint -s ./requirements.txt -t /store/2go/go30/JAG_test/


Installing:

Getting Started with script

- Have python 3 installed on your system. If not installed please go here: https://www.python.org/downloads
    - py -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --upgrade pip
    - py -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org pipx pyenv
    - py -m venv testing_fireCREST_JAG
    - .\env\Scripts\activate
- Clone this repository: `git clone https://juliagustavsenagroscope@dev.azure.com/juliagustavsenagroscope/Allegra_Pilot/_git/pyfirecrest_helper`
s
-  py setup.py install
- You need a client id and a client secret to use the API. These can be obtained from CSCS here: https://oidc-dashboard-prod.cscs.ch/ This can be put in a file called `secrets.json` file that will look something like this (replace the client_id and client_secret with the information you have obtained from the CSCS site):
```
{
    "client_id" : "firecrest-jgustavs-mycomputer",
    "client_secret": "qpfKkEaHCwwmeC0vmysecretforfirecrest",
    "token_uri" : "https://auth.cscs.ch/auth/realms/firecrest-clients/protocol/openid-connect/token"
}
```
The secrets.json file should live in the same directory as the source code.

Helpful installation  if issues with requests,etc. 
export REQUESTS_CA_BUNDLE=/usr/local/share/ca-certificates/BIT_Proxy_Root_CA_01.crt
equivalent on windows?

- Deactivate the virtual env with `deactivate`




# Examples

python3 pyfirecrest_helper.py --list -a daint -t /store/2go/go30/JAG_test/

python3 pyfirecrest_helper.py --download -a daint -s /store/2go/go30/JAG_test/20211212_121543.jpg

python3 pyfirecrest_helper.py --upload -a daint -s ./requirements.txt -t /store/2go/go30/JAG_test/




## Windows testing
py -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org pipx pyenv certifi
py -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org certifi
py -c "import certifi ; print(certifi.where())"
#C:\Users\F80862788\AppData\Local\Programs\Python\Python311\Lib\site-packages\certifi\cacert.pem

## or try to get it to trust the certificaters
py -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org pip_system_certs
## then try...isntalling