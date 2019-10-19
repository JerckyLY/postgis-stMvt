# postgis-stMvt
python 后台连接postgis 返回矢量切片
# 使用
 - 在tileOline.py中配置自己的postgis连接参数
   ```
     Dbpool = psycopg2.pool.SimpleConnectionPool(
        1,
        100,
        dbname='GISMVT',
        user='postgres',
        host='localhost',
        password='admin',
        port='5432')
   ```
  - 重要的查询语句
   ```
      // 传 source-layer 和 tableName参数动态获取
      query = "SELECT  ST_AsMVT( tile , '" + sourceLayer + "' , 4096 , 'geoms' ) tiles FROM ( SELECT   ST_AsMVTGeom( w.geoms , ST_Transform( ST_MakeEnvelope ( %s,%s,%s,%s,4326),3857),4096,256,true) AS geoms ,w.* FROM (SELECT  ST_Transform(geom,3857) geoms , * FROM public." + tableName + "  ) w ) AS tile ;"
     
   ```
  - mapbox前端加载代码
   ```
     this.map.addLayer({
                    "id":"PostGIS",
                    "type":"circle",
                    "source":{
                        "type":"vector",
                        "tiles":[window.origin+"/mapserver/tiles/{z}/{x}/{y}"],
                    },"source-layer":"fills",
                    "paint":{
                        "circle-opacity":1,
                        "circle-radius":2,
                        "circle-color":"#00f"
                    },
                    "layout":{
                        "visibility":"none"
                    }
                });
   ```
   
# 结果 
![image](https://github.com/JerckyLY/postgis-stMvt/blob/master/image/postgis01.png)   
![image](https://github.com/JerckyLY/postgis-stMvt/blob/master/image/2019-07-04_11-32-00.gif)
