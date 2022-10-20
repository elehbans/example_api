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

TODO: Github action for each commit runs unit and integration tests

## Hygiene

TODO: Use black for formatting

## Design Discussion
- Why use Redis? Given the data types and the limited information, I wanted to use this as a learning opportunity and "kick the tires" so to speak on a new technology I hadn't worked with before.  After researching the RedisJSON API, I thought it may serve as a good in-memory solution for mimicking NoSQL data stores like MongoDB, similar to how SQLite works for production databases like PostGreSQL.  Also, from my brief research, it seems like a NoSQL solution would be more performant than a SQL solution at scale with many insertions / deletions happening constantly.  On the other hand, if the goal is to optimize for reads, especially ordered reads, then SQL might be more effective with efficient indexing.
- What are the drawbacks of redis in this scenario?  At this time, the `redisearch-py` client doesn't support multiple "sort_by" statements.  This means that in order to use the client to pull a sorted call list and not sort within the API, we would need to use a compound key: An example 'firstname: helen, lastname: smith' could have a key like 'sortname: smith00000000helen00000000xf7ghxdd` where the lastname and firstname are interleaved with characters that wouldn't impact the sort and then a set of random characters are added a suffix to break ties.  I have not researched how production NoSQL solutions perform in this scenario - but it was interesting thought experiment.  Given that the querying functionality of redis may not be equivalent to something like MongoDB, I think that using a dockerized true NoSQL DB would be a better choice than in-memory solution for development.

## Development Notes - An Honest Appraisal
- Took a little over an hour to get the containers connected and working correctly based setup on a nice [post](https://levelup.gitconnected.com/implement-api-caching-with-redis-flask-and-docker-step-by-step-9139636cef24)
- Took another 2 hours to get the basic api structure and tests sketched out (lots of reading the docs)
- Some debugging and cleanup took about 30 minutes
- Networking issues took another hour as the docs are a bit opaque as to how to use redis within a docker network with flask (most examples have it as a standalone container, not part of a container network)
- Although the ULIDs are a nice touch with redis-om and I thought they would work well, for testing it adds a bit of annoying wrinkle - requiring creating Contacts with the redis client directly prior to calling the API client. Also the EmbeddedJsonModels are also given primary keys, which seems unnecessary and makes the formatting of the return objects a pain.
- After a number of hours trying to understand why the `Migrator().run()` command is not actually migrating the schema over to the redis instance to enable indexing / searching to capture the "home" string in phone numbers, I am throwing in the towel. Lesson learned that I would need to spend more time with Redis and the `redis_om` package to understand their API to determine whether it is worth using or whether it would be easier to just use pydantic for validation, generate UUIDs separately and then use the `redis-py` base package for querying.
- What would have to be done to get this to full functionality? Get the migrations working, add a helper function to format the output of the redis queries to json without the primary keys.
- What functionality is working? The docker network can be spun up and the flask service will respond to some calls, however the `GET /contacts` and the `GET /contacts/contact-list` routes do not work as expected because of the `Migrator()` issue - i.e. querying is not possible since the indexes are not migrated.

