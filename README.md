# Reproducibility Engineering

Author: Vibhash Kumar Singh

Email: singh13@uni-passau.de

## Reproduction package for JSONSchemaDiscovery

This site contains the reproduction package for the JSONSchemaDiscovery tool mentioned in the paper `An Approach for Schema Extraction of JSON and Extended JSON Document Collections`. 

## Using the package

To use the package, from the package directory run `docker-compose up -d`. This will start two containers, one for the `JSONSchemaDiscovery` tool and the other one for the Mongodb which the tool uses to read and write data. The tool's interface can be accessed on `localhost:4200`

To access the JSONSchemaDiscovery tool container, first, we need to get the container ID. To retrieve the container ID, use the command, `docker ps`. This will list all the running containers with their container IDs.

Use the following command to access the container by replacing `<container_ID>` with the correct container ID.

`docker exec -it <container_ID> bash`

## Running smoke.sh
`smoke.sh` is preset in the root of the container and can be run from both inside or outside the container. To run it from outside the container use the following command
`docker exec -it <container_ID> sh /smoke.sh`

## Generating report
The `Makefile` can be used to generate the report. The `Makefile` is present in the root of the container. Run `make report` from the root to build the report. This will generate `report.pdf` inside the `report` folder which is also present in the root. Use `make clean` to clean all the report build files. 

To copy the report.pdf from the container to the current directory in the host, use the following command:

`docker cp <container_ID>:/report/main.pdf .`
