## Steps to run in dev mode:

Requirements: Docker running in your machine

Nice to haves: > Python3.13, vscode/vscodium

`make setup`

This will:

- Create a .env file in your working directory

- Start a PostgreSQL service

- Expose a Flask API app in port 5000

- Launch worker service to asynchronously fetch external data

### Useful commands

1. `make env` Create the default dev .env file (see env.example.txt)

2. `make up` Start services (postgreSQL, flask and workers)

3. `make down` Stop services

4. `make migrate` Apply migrations. Excute if this is your first time using the app.

5. `make migrations` If there is any change in the model dir

6. `make test` TDD the heck out of it

Check `make help` to get +info

## Design Choices and Implementation Details

#### Problem-Solution Fit

The solution is designed to provide a robust, scalable API with asynchronous processing for external data. Using Docker ensures consistent development environments and ease of deployment. The architecture separates concerns clearly between API, workers, and database services.

#### Adherence to API Spec

The API follows the provided OpenAPI specification. Input validation, response formatting, and error handling are aligned with the spec.

#### Software Architecture

DDD-ish design. Not really a huge fan of it, I sometimes think it is an overkill, but I tried doing something halfway-through readable.

Asynchronous Workers: Dedicated background worker fetch and process external data without blocking the API.

#### Efficiency

- Docker ensures isolated, reproducible environments.
- SQLAlchemy ORM for optimized DB interactions.
- Asynchronous worker isolation for external data retrieval.

## Going the Extra Mile 🚀

#### Scalability

In case we needed to handle large datasets (e.g., thousands of plans with hundreds of zones each), the architecture can be extended with a RabbitMQ (or similar) queue system:

- <b>Retrieval Service:</b> Fetches raw XML or data from the provider.

- <b>Parsing Service:</b> Processes each XML and transforms it into domain entities, then adds them to a processing pool.

- <b>Pool Manager / DB Service:</b> Manages the pool and inserts or updates the database efficiently

This approach decouples the stages of data ingestion, allowing horizontal scaling for each service independently. In case any service is down, it is not blocking the rest, and can be handle easily.

#### High Traffic

To support 5k–10k requests per second:

- <b>Caching Layer:</b> Use Redis or Memcached to cache frequently accessed data and reduce database load.

- <b>Rate Limiting:</b> Implement rate limiting to prevent abuse and protect system resources

- <b>Increase workers:</b> Increase concurrency by adding more worker processes or threads in Gunicorn (or any other wsgi), allowing the Flask app to handle more simultaneous requests.

#### Optimization Strategies

- <b>Database Indexing:</b> Ensure proper indexing for frequently queried fields to speed up read operations, in this case start_at and end_at. I would have to review if it is better to save the whole column as DateTime and deserialize it or keep it as it is.

- <b>Connection Pooling:</b> Use SQLAlchemy connection pooling to manage DB connections efficiently. (reuse connections instead of creating them on demand)

- <b>Profiling & Monitoring:</b> Regularly profile endpoints and worker processes to identify bottlenecks like Grafana.

- <b>Lazy Loading / Pagination:</b> For endpoints returning large datasets, implement pagination or lazy loading to reduce memory usage and response time.

## Side Notes

The provided requirements may suggest the use of a non-SQL database; however, I believe this is not necessary. Given the nature of the data—particularly the reliance on date-based queries—an SQL database can be a more efficient and practical choice, offering strong performance and straightforward query capabilities.

In a production-ready setup, I would also include a `docker-compose.prod.yml` file to run the Flask application using Gunicorn with a configurable number of worker processes, ensuring better performance and scalability.

For even more optimization: Compress responses (gzip / brotli)
