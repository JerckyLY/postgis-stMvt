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
      // fills 为source-layer名称
      query = "SELECT  ST_AsMVT( tile , 'fills' , 4096 , 'geom' ) tiles FROM ( SELECT  ST_AsMVTGeom( w.geom , ST_Transform(       ST_MakeEnvelope ( %s,%s,%s,%s,4326),3857),4096,256,true) AS geom FROM (SELECT  geom FROM public.china_point  ) w ) AS tile ;"
     
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
![image]('https://github.com/JerckyLY/postgis-stMvt/blob/master/image/2019-07-04_11-32-00.gif')
