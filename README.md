# example_api

## Development

When developing locally:

First create a running local redis instance: `docker run -p 6379:6379 redislabs/redisearch:latest`

After creating the redis instance, you can also run the flask app locally:

```bash
cd api
source .env
export RUNNING_LOCALLY=True
flask run
```

## Deployment

After cloning the repo and installing Docker Compose, you can deploy both the redis data store instance as well as the flask API:

```bash
docker-compose build
docker-compose up
```

The API can be used by sending HTTP requests to the local instance as shown in the integration tests mentioned below.

## Testing

Unit tests for the flask API are done with pytest and do not test functionality related to redis. These tests can be run with `python -m pytest tests/test_unit.py` from the root directory.

Integration tests can be run a locally deployed redis instance by `python -m pytest tests/test_integration.py` after creating a running redis instance (see Development for example docker command). 

## CI / CD

Github action for each commit runs unit and integration tests

## Hygiene

Use black for formatting

## Design Discussion
- Why use Redis? Given the data types and the limited information, I wanted to use this as a learning opportunity and "kick the tires" so to speak on a new technology I hadn't worked with before.  After researching the RedisJSON API, I can see how it is a good in-memory solution for mimicking NoSQL data stores like MongoDB, similar to how SQLite works for production databases like PostGreSQL.  Also, from my brief research, it seems like a NoSQL solution would be more performant at scale with many insertions / deletions happening constantly.  On the other hand, if the goal is to optimize for reads, especially ordered reads, then SQL might be more effective with efficient indexing.
- Could ordered call list retrieval time complexity be improved by a different storage mechanism? If the amount of data stored became quite large and we wanted to improve the speed of call list retrieval, I could see using a compound key or field that reduces the need for multiple secondary indexes - for example 'firstname: helen, lastname: smith' could have a key like 'sortname: smith00000000helen00000000xf7ghxdd` where the lastname and firstname are interleaved with characters that wouldn't impact the sort and then a set of random characters are added a suffix to break ties.  I have not researched how production NoSQL solutions perform in this scenario - but it was interesting thought experiment.

## Development Notes
- Took a little over an hour to get the containers connected and working correctly based setup on a nice [post](https://levelup.gitconnected.com/implement-api-caching-with-redis-flask-and-docker-step-by-step-9139636cef24)
- Took another 2.5 hours to get the basic api structure and tests sketched out (lots of reading the docs)
- Some debugging and cleanup took about 30 minutes
- Networking issues took another hour as the docs are a bit opaque as to how to use redis within a docker network

