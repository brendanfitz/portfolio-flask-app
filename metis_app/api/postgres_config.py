from os import environ

cc = {
    'host': environ['blog_postgres_host'],
    'dbname': environ['blog_postgres_dbname'],
    'user': environ['blog_postgres_user'],
    'password': environ['blog_postgres_password'],
}