# Images


### Upload an image to the server.
```shell
curl -X POST -F "file=@test_files/1.png" -F "title=This is water png 100 100" -F "width=100" -F "height=100" http://localhost:8000/images/
```

### Get all images
```shell
curl http://localhost:8000/images/
```

#### Filter images by title
```shell
curl http://localhost:8000/images/?title__icontains=water
```

### Get image with id
```shell
curl http://localhost:8000/images/1/
```

### Use pagination
```shell
curl http://localhost:8000/images/?offset=1&limit=5
```