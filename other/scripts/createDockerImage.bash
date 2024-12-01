# build

cd src/defend/container

# Erase prior if existing
docker image inspect myapp >/dev/null 2>&1 && docker rmi myapp -f

# Build
docker build -t myapp .
