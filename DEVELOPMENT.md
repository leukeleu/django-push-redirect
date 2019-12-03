# Setup

This is a `docker-compose` project, download and install 
[Docker Desktop](https://www.docker.com/products/docker-desktop)
to run this.


## Certificates

In order to use HTTP/2 a certificate is required.

[`minica`](https://github.com/jsha/minica) is a excellent tool
to generate a root CA certificate and a certificate for `localhost`

```shell script
minica -domains localhost
```

Then add the generated root CA file to the OS/browsers trust store
and move the certificates for `localhost` to `./conf/certs`.

The expected file names for the certificates are `cert.pem` and `cert.key`.


## Run the project

Once the certificates have been set up, run nginx and Django using:

```shell script
docker-compose up -d
```

Visiting the following urls in a modern browser should show the 
difference between "normal" redirects and HTTP/2 Server Push redirects:

* <http://localhost/hello/world> redirects to <http://localhost/hello/world/>
* <https://localhost/hello/world> redirects to and pushes <https://localhost/hello/world/>


## Linting/Formatting

This project uses `black`, `isort` and `flake8` to enforce a consistent
code style.

Run the next set of commands to apply fixes and perform linting:

```shell script
docker-compose exec django isort
docker-compose exec django black .
docker-compose exec django flake8
```


## Testing/Coverage

To run the unit tests run:
 
```shell script
docker-compose exec django python -W module ./manage.py test
```

To generate a coverage report run:
 
```shell script
docker-compose exec django coverage run ./manage.py test
docker-compose exec django coverage report
docker-compose exec django coverage html
```

The coverage report can be found in `./htmlcov`.
