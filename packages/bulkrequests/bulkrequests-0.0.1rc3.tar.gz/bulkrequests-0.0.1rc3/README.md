# dcache bulkrequests client

## Install
To install the package the user has to clone the repository with `git clone`. Then access the directory and execute `pip install -e .` For test purposes the user can create a virtual environment as explained below.


### Virtual Environment
The user has to create a `conda environment` with pip

`conda create -n test-dc pip`


## Authentication
With bulkrequests the user can interact with dCache using it own credentials in different ways.
The `user` (username), `pwd` (password) and `url` (endpoint), can be passed by cli, through the `--config`
option or storing the information in the `$HOME/.dcacheclientrc` file. Also an `oidc account` can be used.
For more information type `bulkrequests -h`


## Setup
The config file has this format with an `oidc-agent-account`

```
[DEFAULT]
url=https://endpoint.io:4521
oidc-agent-account=dcache-client
ca-directory=/etc/ssl/certs
no-check-certificate=False
```

The config file has this format using `user` and `pwd`

```
[DEFAULT]
user=john
pass=doe
url=https://endpoint.io:4525
no-check-certificate=True
```

The config file can be divided in many sections to use different profiles. The default values are taken
from the DEFAULT section and overwritten later if other profile is used.
```
[DEFAULT]
user=john
pass=doe
url=https://endpoint.io:4525
no-check-certificate=False

[SITE1]
oidc-agent-account=dcache-client
url=https://other-endpoint.io:7549
no-check-certificate=True
```

Also all this parameters can be set by environment variables; the variables names are:
```
BULKREQUESTS_USER
BULKREQUESTS_PWD
BULKREQUESTS_URL
BULKREQUESTS_OIDC_AGENT_ACC
BULKREQUESTS_PROFILE
BULKREQUESTS_CERTIFICATE
BULKREQUESTS_PRIVATE_KEY
BULKREQUESTS_X509_PROXY
BULKREQUESTS_CA_CERTIFICATE
BULKREQUESTS_CA_DIRECTORY
BULKREQUESTS_NO_CHECK_CERT
```

All this parameters can also be passed through the cli options.


## Options
The options are the following

`-h`, `--help` show help dialog.

`-u`, `--user` username to be used in dCache login.

`-p`, `--pwd` password to be used in dCache login.

`-f`, `--file` a plain text file to be readed by `bulkrequests` where dCache path are stored.

`--profile` bulkrequestsrc file can be divided to access differents sites.

`-j [N=1]`, `--threads=[N]` allows N jobs at once. By default uses N=1.

`--url` dCache endpoint url.

`--get-locality` returns the actual **locality** of the file passed by `--file` argument or the one contained into the last argument (it must be a valid dCache path). It has no effect over directories.

`--get-qos`  returns the actual **qos** of the file passed by `--file` argument or the one contained into the last argument (it must be a valid dCache path). It has no effect over directories.

`--set-qos` takes a qos as argument and sets it to the file passed by `--file` argument or the one contained into the last argument (it must be a valid dCache path). It has no effect over directories.

`-c`, `--config`can be used to pass an alternative config file with authentication information.

`--oidc-agent-account` takes an oidc account.

`--certificate` CA certificate to verify peer against.

`--x509-proxy` Client X509 proxy file.

`--private_key` Private key file.

`--ca-certificate` CA certificate to verify peer against.

`--ca-directory` takes a CA certificate directory to be used.

`--no-check-certificate` does not check a certificate.

`--size` prints the size of the query in bytes

`--human` prints the size of the query in a human-readable format

`-r`, `--recursive` when a directory is passed, this options enables to navigate it.

`-q`, `--quiet` disables progress output, only shows a summary at the end.

`-d`, `--debug` show debug information.


### Examples

###### get `/tape/file1.h5` file locality (path in dCache) using username and password
`bulkrequests -u user -p pass --url https://yourendpoint.io:port --get-locality /tape/file1.h5`

###### get the qos of all files in `files.txt` and subdirectories using an oidc account
`bulkrequests --oidc-agent-account oidc_account --url https://yourendpoint.io:port -f files.txt --get-qos --recursive`

###### get the locality of `/tape` (dCache path) content directory
`bulkrequests -u user -p pass --url https://yourendpoint.io:port --get-locality --recursive /tape`

###### set `tape` qos to all files contained in files.txt using mynewconfig config file in quiet manner
`bulkrequests --url https://yourendpoint.io:port -f files.txt --set-qos tape --recursive --quiet --config mynewconfig`

###### get the qos and size (in bytes) of all files in `files.txt` and subdirectories using an oidc account
`bulkrequests --oidc-agent-account oidc_account --url https://yourendpoint.io:port -f files.txt --get-qos --recursive --size`

###### get the locality and size (in human readable format) of all files in `/tape` directory and subdirectories using an oidc account
`bulkrequests --oidc-agent-account oidc_account --url https://yourendpoint.io:port --get-qos --recursive --size --human /tape`


### Installing bulkrequests and oidc-agent in a conda environment

#### create a conda environment with `pip` and `oidc-agent`

`conda create -n bulk pip oidc-agent -c conda-forge`

`conda activate bulk`

#### start oidc-agent

``eval `oidc-agent` ``

#### create an oidc-agent-account named with a browser

`oidc-gen -m --iss=https://idp.pic.es/auth/realms/PIC --client-id=dcache-view --client-secret=8c61284e-9653-4309-acca-8b82b38f8d08 --scope="openid profile" --no-webserver --redirect-uri=http://localhost:8080 dcache-client`

This command will open a browser where the client has to sign up with LDAP credentials. After the login, the account should be created and loaded, ready to use.

#### create an oidc-agent-account named *without* a browser

`oidc-gen -m --iss=https://idp.pic.es/auth/realms/PIC --client-id=dcache-view --client-secret=8c61284e-9653-4309-acca-8b82b38f8d08 --scope="openid profile" --no-webserver --redirect-uri=http://localhost:8080 dcache-client`

This command will create a link. This link should be copied and introduced into a web browser. Then the user has to sign up. Once signed up, the browser produces a new link, it should be copied.
Finally the user has to execute the next command

`oidc-gen --codeExchange='url' `

Where *url* is the url generated in the previous step.


dCache bulkrequests management developed by PIC and IATE

Its based on [dcacheclient](https://github.com/neicnordic/dcacheclient)

This code tries to manage bulk requests awaiting for the [implementation](https://docs.google.com/document/d/14sdrRmJts5JYBFKSvedKCxT1tcrWtWchR-PJhxdunT8/edit?usp=sharing "implementation") in dCache v7.0

This project has received funding from the European Union’s Horizon 2020 Research and Innovation Programme under the Marie Skłodowska-Curie grant agreement No 734374”
