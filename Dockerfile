FROM 677125173008.dkr.ecr.ca-central-1.amazonaws.com/cope:req

# copy project
COPY . /app/

# port where the Django app runs
EXPOSE 80
EXPOSE 8000

# Use docker-compose to run the Django app