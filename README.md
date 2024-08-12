# dnd-spells-backend
 Backend for the dnd-spells I'm making

# Deployment
Deploy using github by forking with [these instructions](https://vercel.com/docs/deployments/git/vercel-for-github)

# Env variables needed
* Necessary
  * Used to connect to store spell list, make it by registering [here](https://www.mongodb.com/cloud/atlas/register) and following these instructions [here](https://www.mongodb.com/docs/atlas/tutorial/create-new-cluster/#navigate-to-the-database-deployments-page-for-your-project-2)
    * MONGO_HOST_URL
    * MONGO_DB_NAME
    * MONGO_USERNAME
    * MONGO_PASSWORD
  * Used for Django, generate secret key by these methods if you dont want to download django: [here](https://stackoverflow.com/questions/41298963/is-there-a-function-for-generating-settings-secret-key-in-django)
    * DJANGO_SECRET_KEY
    * DJANGO_DEBUG
  * Used to allow frontend to connect
    * FRONTEND_URLS
* Unnecessary
  * Used to for admin privileges, make one using vercel (make one with `python manage.py createsuperuser`)
    * POSTGRES_URL
    * POSTGRES_PRISMA_URL
    * POSTGRES_URL_NON_POOLING
    * POSTGRES_USER
    * POSTGRES_HOST
    * POSTGRES_PASSWORD
    * POSTGRES_DATABASE
    * POSTGRES_PORT
  * Used to store images for spells, follow the ways to do it [here](`https://testdriven.io/blog/storing-django-static-and-media-files-on-amazon-s3/`)
    * AWS_S3_ACCESS_KEY_ID
    * AWS_S3_SECRET_ACCESS_KEY
    * AWS_STORAGE_BUCKET_NAME
    * AWS_S3_REGION_NAME
