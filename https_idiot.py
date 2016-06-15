#!/usr/bin/env python
#
# Super simple https webserver to serve
# static content.
# Supports python 2.7 and 3.
#
# YOU SHOULD ONLY USE THIS FOR DEVELOPING AND TESTING PURPOSES.
# DO NOT USE THIS FOR ANYTHING PRODUCTION LIKE.
# THE KEY FILE IS SHARED AND
# THE SERVER ONLY ALLOWS 1 SIMULTANOUS CONNECTION !
# 
# Create self signed certificate with openssl like:
#   openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes
#


import argparse
import os
from os.path import isfile, realpath, dirname, join as os_join

try:
    from http.server import HTTPServer, SimpleHTTPRequestHandler
    # we just assume python 3 here
    to_byte = bytes
except ImportError:
    from BaseHTTPServer import HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    to_byte = lambda a, *args: a
import ssl


_fallback_key = to_byte("""
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC6KFpldZJC63e/
of5iQjP+cY1trrw8ACqVwLKs4uMNEokzCNL1+rFBsvseDBHExqm4/5C7+NwbqzcP
sMI0CpdbAyjeKcBf4Kow6b++0PdlNX7mgLaBbR8yJJe8FyUoAH1+xvS2Os8A3Mgw
qecejdQIEeytlBjxFws+cDgkKqTNsIHXRclscztTnb4eQY0WaNAeY/nW3XUXEBvU
hxD7utyrTrj/1jilJPEzJdngs8CeLRsm+IUDhO2K+NBWi11IGGctcKI4bLKHgUJY
bqgsnHkMWLr6wDTUPqQiRvb++yatLjvdb5AZlI0JPoI3QghDGqqqUHur+vwMeCDf
iLgLt8Z9AgMBAAECggEAIoyIslnOqlLPJ6al8pB829UxPVD3qF8TiDV6M7HsF6oA
ApO5q2M6cIoKJvpwdce1ChuMPgaiuxPcpTHV6RiqHH8Kn6i6BlFI5MkNCBn6QDNc
eOUcegrJhmHaM1NMVw84O0YrdoKVloBjOvzdYwNJfbHt7g0VT/FJ6e2jzbqIWY/+
i+x11r6BFkdpLdEkcOunKkm508wEoV3k30csKRA1ePe9VCuNCDHY0l2pQBiiUrV5
6QGfZHiWb5yt5JELaams9VMHNgdm+XT/NiN8lF6s3g4fyjnc8IbjCic59O87HxLi
TFgHflywARmqD9bqNA8z3rQ4s/xOLLGqNkQe1ObWQQKBgQDfNDBfx/NOMGUROhqu
thNjO8uehNAWkKDTJ2oUMjDKwXpCGKIEHsB+6D6hgYMVd7njXlvruS/RYNLDaIhu
DlETZ5vmVt2/rajYORam8M3ukPEVaQFA5G6Hyys7sdkBFfEUs0viR26x06xeUogD
5YVVv4BHcN7Kx4Ii9LhCH302LQKBgQDVgquiG8oUetTWdIJrafNM5O8HE+GfqKr4
Koiy8qiDq8x1z4HNhi83ljjJf8DAIJUBzs87BFQ/wGzHwz6P8znKiyFFrW6ZQUXp
CR/APf2I7iJ3ksN0G4LVaNiA+bfrUzakOUP9f43NR8NIVkcuazwMyiVPsYXY5CVk
hmPVLtnTkQKBgEse/HzwBdI19X4DyUEt5H6MfG5gksxVZttKM6iSb9t9nJEsSzMJ
yo2rypB+z0hlYDnG4zcFv7M/XBAKWYh45w6Z2119tOozH1WOeTI8b4KwY4NqMNLP
TugDGAziQX/dC6OE6LBCjF3rOOMR8dcl42dFqX3h3gnvdbwgEvemM3UNAoGAUv53
Pw10UN+qSi6B38UQiSxYabTluE01IEBQYNcIgB5Q3N6rgzuMsRvYuSLKxyQjJ8+/
KB63rQxcfI49jHEsXroUVeRjoHkJ9trQF8dA/XArv7Ux+rkS82fM+N2ZC4WOMOn9
rtVdRpWFqGG5S6btcb9GH6NO9w9AJcJDnkOW8rECgYEAmS13CeSC0lWRvpvdUxAr
aDDw0Pwx6aNjJ0GgVc+RAw6jGL6WV8yiWUhPIJSgdYzYSW9BEpefmiBAjdxTYXqD
+DvKFDe8ZWH//CJiNPc/zOE1vFuJFXHKBo8KdY/5fYni9FszQBEH0YaIin4U9FCV
tAsGrkIIojaIG8tYzVYFyL4=
-----END PRIVATE KEY-----
-----BEGIN CERTIFICATE-----
MIIDFzCCAf+gAwIBAgIJANoJgHqHwljcMA0GCSqGSIb3DQEBCwUAMCIxCzAJBgNV
BAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMB4XDTE2MDYxNDE5MzA1MVoXDTE3
MDYxNDE5MzA1MVowIjELMAkGA1UEBhMCQVUxEzARBgNVBAgMClNvbWUtU3RhdGUw
ggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC6KFpldZJC63e/of5iQjP+
cY1trrw8ACqVwLKs4uMNEokzCNL1+rFBsvseDBHExqm4/5C7+NwbqzcPsMI0Cpdb
AyjeKcBf4Kow6b++0PdlNX7mgLaBbR8yJJe8FyUoAH1+xvS2Os8A3MgwqecejdQI
EeytlBjxFws+cDgkKqTNsIHXRclscztTnb4eQY0WaNAeY/nW3XUXEBvUhxD7utyr
Trj/1jilJPEzJdngs8CeLRsm+IUDhO2K+NBWi11IGGctcKI4bLKHgUJYbqgsnHkM
WLr6wDTUPqQiRvb++yatLjvdb5AZlI0JPoI3QghDGqqqUHur+vwMeCDfiLgLt8Z9
AgMBAAGjUDBOMB0GA1UdDgQWBBTcNfyjXKaGMCTG8iXTt3txhwQrcDAfBgNVHSME
GDAWgBTcNfyjXKaGMCTG8iXTt3txhwQrcDAMBgNVHRMEBTADAQH/MA0GCSqGSIb3
DQEBCwUAA4IBAQCXZoyJratwD2BPa5M5xPUyI+wnEysym/ces4XZctaI/a3MDAfF
ze0DyVFA0NmXavAEQX5EoB1MpCCqxlsPnRBMjcAhqEsiRw6xFLgiXbbdqO9tyZez
Cx4oumU4y9k6c+hICWrEe5ZnwSFIOOigypiL8mVjSWpTjbzLukcWErd5lKTjdk6F
vFeMjRmbVtVzWz1jTaggMqf34YN7Pg//S0qkPHJOItQY35eLv6STt02dxaa81dCo
iDS1qQ4Yk3LeSQewg/FbZUGlo+zf1wVNKqgCEQ2qj7QDbTzJCykBQ1wc6VOOGfbz
a+MHSy4jcC2im710HusdvBaFDK7qUzByF91j
-----END CERTIFICATE-----
""", 'ASCII')


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--key', help="""The keyfile to use.
    Need to contain the key AND the certificate formated as PEM.
    If not given we try the following until something exists.
    1. "server.pem" in the CWD.
    2. "server.pem" at the same location as this script.
    3. The fallback key included in this script (This is not safe at all)""", default="")
    parser.add_argument('-p', '--port', type=int, help="The port to use (Default 4443).", default=4443)
    parser.add_argument('-l', '--listen', help="""The address to listen to.
    Defaults to '127.0.0.1' which only allows connections from the same system.
    Set to '0.0.0.0' or '' to allow connections from everywhere or a specific ip/domain to restrict it.
    """, default="")
    args = parser.parse_args()

    
    # Search for the keyfile
    _is_temp_file = False
    if len(args.key) != 0:
        if not os.path.isfile(args.key):
            print("Keyfile '%s' not found." % args.key)
            exit(1)
        keyfile = args.key
    else:
        if os.path.isfile('server.pem'):
            keyfile = 'server.pem'
            os.path.join(a)
        elif isfile(os_join(dirname(realpath(__file__)), 'server.pem')):
            keyfile = os_join(dirname(realpath(__file__)), 'server.pem')
        else:
            # We need to create a temporary file for the key
            # as ssl.wrap_socket just pass the path.
            from tempfile import mkstemp
            fd, keyfile = mkstemp()
            offset = 0
            _len = len(_fallback_key)
            while offset < _len:
                offset += os.write(fd, _fallback_key[offset:])
            os.close(fd)
            _is_temp_file = True
        
    print('Using keyfile "%s"' % keyfile)
    print('START LISTENING ON https://%s:%i\n' % ('localhost', args.port))
    
    httpd = HTTPServer((args.listen, args.port), SimpleHTTPRequestHandler)
    httpd.socket = ssl.wrap_socket (httpd.socket, certfile=keyfile, server_side=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Going down.")
        if _is_temp_file:
            os.remove(keyfile)
