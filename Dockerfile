FROM python:3.7.4-alpine AS base

################# Multi-staging #################

# build all dependencies in the base image
FROM base AS builder

RUN mkdir /install
WORKDIR /install

COPY ./requirements.txt /requirements.txt

# update pip
RUN pip install --upgrade pip
# install python packages
RUN pip install --prefix="/install" -r /requirements.txt

# build our image from the first one

FROM base

# copy dependency folder in new image without cache
COPY --from=builder /install /usr/local/

COPY --from=builder /usr/lib/lib* /usr/lib/

# set working directory
WORKDIR /usr/src/app

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# add app
COPY . /usr/src/app

EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["main.py", "run", "-h", "0.0.0.0", "-p", "5000"]