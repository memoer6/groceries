
# Load environment variables
export POSTGRES_CONTAINER_NAME=postgres-db

 
# Stop current container if it's running
if [ "$(docker ps -a | grep $POSTGRES_CONTAINER_NAME)" ]; then
  docker stop $POSTGRES_CONTAINER_NAME && docker rm $POSTGRES_CONTAINER_NAME  # -> docker rm -f $NAME
fi  

docker run -d \
    --name postgres-db \
    --env-file ../../.env \
    -v /home/eduardo/coding/groceries/database/postgres/init:/docker-entrypoint-initdb.d \
    -p 5432:5432 \
    postgres

# To build custom image using Dockerfile
#docker build -t my-postgres-img .

# The default postgres user and database are created in the entrypoint with initdb.

# POSTGRES_PASSWORD: This environment variable sets the superuser password for PostgreSQL. The default
# superuser is defined by the POSTGRES_USER environment variable.

# POSTGRES_USER: This variable will create the specified user with superuser power and a database with the
# same name. If it is not specified, then the default user of postgres will be used.

# POSTGRES_HOST_AUTH_METHOD: This optional variable can be used to control the auth-method for host connections
# for all databases, all users, and all addresses. If unspecified then md5 password authentication is used.
# The method scram-sha-256 performs SCRAM-SHA-256 authentication. It is a challenge-response scheme that
# prevents password sniffing on untrusted connections and supports storing passwords on the server in a 
# cryptographically hashed form that is thought to be secure. The method md5 uses a custom less secure
# challenge-response mechanism. It prevents password sniffing and avoids storing passwords on the server in
# plain text but provides no protection if an attacker manages to steal the password hash from the server. 
# Also, the MD5 hash algorithm is nowadays no longer considered secure against determined attacks.  
# The method password sends the password in clear-text and is therefore vulnerable to password “sniffing”
# attacks. It should always be avoided if possible. If the connection is protected by SSL encryption then
# password can be used safely, though. (Though SSL certificate authentication might be a better choice if 
# one is depending on using SSL)

# POSTGRES_DB: This optional environment variable can be used to define a different name for the default
# database that is created when the image is first started. If it is not specified, then the value of 
# POSTGRES_USER will be used

# Initialization scripts: If you would like to do additional initialization in an image derived from this
# one, add one or more *.sql, *.sql.gz, or *.sh scripts under /docker-entrypoint-initdb.d (creating the
# directory if necessary). After the entrypoint calls initdb to create the default postgres user and 
# database, it will run any *.sql files, run any executable *.sh scripts, and source any non-executable
# *.sh scripts found in that directory to do further initialization before starting the service.
# Warning: scripts in /docker-entrypoint-initdb.d are only run if you start the container with a data directory 
# that is empty; any pre-existing database will be left untouched on container startup.



