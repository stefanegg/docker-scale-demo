# docker-scale-demo
Simple web server that returns container name, docker host name and a random string

## Usage

### Build
```bash
docker build -t scale-demo .
```

### Run
```bash
docker run -d -p 8080:8080 -e host=$(hostname) scale-demo
```
