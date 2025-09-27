# Images

### Set up envs and run

```shell
cp .env.example .env
docker compose up -d
```

### Docs

http://127.0.0.1:8000/api/docs/

### Upload an image to the server.
```shell
curl -X POST -F "file=@test_files/2.jpg" -F "title=I love this picture real 250 250 " -F "width=250" -F "height=250" http://localhost:8000/images/
```

### Get all images
```shell
curl http://localhost:8000/images/
```

### Filter images by title
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