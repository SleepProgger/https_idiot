# https_idiot
Super simple https server in python (python 2 and 3 compatible). for developing / testing

**THIS SCRIPT SHOULD NOT BE USED AS PRODUCTION SERVER**  
If you supply no certificate via the `--key` parameter it will use a SHARED hardcoded certificate.  
Additionally it only allows one concurrent connection.  

*Basically the only reason to use this is if you want to load/inject local CSS or Javascript files in a website loaded via https without them getting blocked by your browser because of `Mixed Active Content`*  



Usage
-----
For the simplest case just drop the `https_idiot.py` into the folder you want to use as webroot and double click it (depending on your OS and settings and if you have python installed *doh*) it should start the webserver on port `4443`.  
Just navigate to 'https://localhost:4443' and add an exception for the certificate.  
Use `ctr+c` to stop the server.

The web root is always the current directory.  

    usage: https_idiot.py [-h] [-k KEY] [-p PORT]
    
    optional arguments:
      -h, --help            show this help message and exit
      -k KEY, --key KEY     The keyfile to use. Need to contain the key AND the
                            certificate formated as PEM. If not given we try the
                            following till something exists. 1. "server.pem" in
                            the CWD. 2. "server.pem" at the same location as this
                            script. 3. The fallback key included in this script
                            (This is not safe at all)
      -p PORT, --port PORT  The port to use (Default 4443).


