### Initial Setup

#### Prerequisites:
Make sure you have docker and docker-compose working on your system.  
Useful links:  
[Install Docker on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)  
[Install Docker compose](https://docs.docker.com/compose/install/other/)  
[How to Install Docker and Docker Compose on Linux](https://www.howtogeek.com/devops/how-to-install-docker-and-docker-compose-on-linux/)  

1. Clone the project
`git clone ....`

2. Change directories  
`cd rates-api`

3. Build the Postgres docker image.  
`docker build -t rates-db ./db_setup/.`  

4. Build the Python API docker image.  
`docker build -t rates-api .`  

5. Run the application using docker-compose
`docker-compose up --build` 

6. Application is now accessible on `localhost:5000/`  
NB: It's important that you use the same names for the images as they will be used in the docker compose setup.

7. To stop: Spam Ctrl+c in terminal and do `docker-compose down`

### Usage:
`curl "http://localhost:5000/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main"
`

Sample result:  
```
[
    {
        "average_price": "1112",
        "day": "2016-01-01"
    },
    {
        "average_price": "1112",
        "day": "2016-01-02"
    },
    {
        "average_price": "null",
        "day": "2016-01-04"
    },
    {
        "average_price": "1142",
        "day": "2016-01-05"
    },
    {
        "average_price": "1142",
        "day": "2016-01-06"
    },
    {
        "average_price": "1137",
        "day": "2016-01-07"
    },
    {
        "average_price": "1124",
        "day": "2016-01-08"
    },
    {
        "average_price": "1124",
        "day": "2016-01-09"
    },
    {
        "average_price": "1124",
        "day": "2016-01-10"
    }
]
```


