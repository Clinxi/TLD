# TLD项目后端使用及部署说明



## 运行后端
```py
mvn spring-boot:run
```
## Java测试案例
```shell
curl -X POST http://10.214.211.207:8080/api/detect -H "Content-Type: application/json" -d '{"detectOriginalPhotoList":[{"originalPhotoAddress":"address1","originalPhotoName":"name1"}],"projectStandardList":[{"startingMileage":0.0,"endingMileage":10.0,"standardSteelBarSpacing":5.0,"standardThickness":2.0}]}'

curl -X POST http://10.214.211.207:8080/api/detect \
  -H "Content-Type: multipart/form-data" \
  -F 'entities=[{"originalPhotoAddress":"path/to/photo1.jpg","originalPhotoName":"photo1.jpg"},{"originalPhotoAddress":"path/to/photo2.jpg","originalPhotoName":"photo2.jpg"}]' \
  -F 'entities1=[{"startingMileage":0.0,"endingMileage":10.0,"standardSteelBarSpacing":0.0,"standardThickness":15.0},{"startingMileage":10.0,"endingMileage":20.0,"standardSteelBarSpacing":0.5,"standardThickness":20.0}]'


curl -X POST http://10.214.211.207:8080/api/detect \
  -H "Content-Type: multipart/form-data" \
  -F 'entities=[{"originalPhotoAddress":"path/to/photo1.jpg","originalPhotoName":"photo1.jpg"},{"originalPhotoAddress":"path/to/photo2.jpg","originalPhotoName":"photo2.jpg"}]' \
  -F 'entities1=[{"startingMileage":0.0,"endingMileage":10.0,"standardSteelBarSpacing":0.0,"standardThickness":15.0},{"startingMileage":10.0,"endingMileage":20.0,"standardSteelBarSpacing":0.5,"standardThickness":20.0}]'

curl -X POST http://10.214.211.209:8080/api/detect \
     -H "Content-Type: application/json" \
     -d @data.json


```

## python测试案例
```shell
python test.py '[{"originalPhotoAddress":"path/to/photo1.jpg","originalPhotoName":"photo1.jpg"},{"originalPhotoAddress":"path/to/photo2.jpg","originalPhotoName":"photo2.jpg"}]' '[{"startingMileage":0.0,"endingMileage":10.0,"standardSteelBarSpacing":0.0,"standardThickness":15.0},{"startingMileage":10.0,"endingMileage":20.0,"standardSteelBarSpacing":0.5,"standardThickness":20.0}]'
```