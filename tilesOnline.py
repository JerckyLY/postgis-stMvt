# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import shutil
import math
import psycopg2
import psycopg2.pool
import Util
from flask import Flask, render_template, make_response, jsonify
import time

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, 'cache')
Dbpool = psycopg2.pool.SimpleConnectionPool(
    1,
    500,
    dbname='scgs',
    user='scgs',
    host='192.168.1.107',
    password='scgs',
    port='5432')
#
# Dbpool = psycopg2.pool.SimpleConnectionPool(
#     1,
#     500,
#     dbname='CHINA',
#     user='postgres',
#     host='localhost',
#     password='admin',
#     port='5432')


def tile_ul(x, y, z):
    n = 2.0 ** z
    lon_deg = x / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
    lat_deg = math.degrees(lat_rad)
    return lon_deg, lat_deg


def get_tile(tableName, sourceLayer, z, x, y):
    print(tableName)
    print(sourceLayer)
    # 抽稀简化 提高查询速度
    # tolerance = listResolution[z]

    print('.............等级: %d' % z)
    # print(tolerance)
    lons = Util.getLon(x, z)
    lats = Util.getLat(y, z)

    lonmin = str(lons[0])
    lonmax = str(lons[1])

    # 保证求得的经纬度不是负数
    # latmin = str(-lats[0])
    # latmax = str(-lats[1])

    latmin = str(lats[1])
    latmax = str(lats[0])
    # minx = str(str(xmin)+' , ' + str(ymin) + ' , ' + str(xmax) + ' , '+str(ymax))
    minx = str(lonmin + ' , ' + latmin + ' , ' + lonmax + ' , ' + latmax)

    print(minx)

    tile = None
    conn = Dbpool.getconn()
    # cur = conn.cursor()
    if (conn):
        # query = "SELECT  ST_AsMVT( tile , 'fills' , 4096 , 'geom' ) tiles FROM ( SELECT  ST_AsMVTGeom( w.geom , ST_Transform( ST_MakeEnvelope ( %s,%s,%s,%s,4326),3857),4096,256,true) AS geom FROM (SELECT ST_Simplify(geom,%s) as geom FROM public.china_point  ) w ) AS tile ;"
        query = "SELECT  ST_AsMVT( tile , '" + sourceLayer + "' , 4096 , 'geoms' ) tiles FROM ( SELECT   ST_AsMVTGeom( w.geoms , ST_Transform( ST_MakeEnvelope ( %s,%s,%s,%s,4326),3857),4096,256,true) AS geoms ,w.* FROM (SELECT  ST_Transform(geom,3857) geoms , * FROM public." + tableName + "  ) w ) AS tile ;"
        cur = conn.cursor()
        cur.execute(query, (lonmin, latmin, lonmax, latmax))
        tile = bytearray(cur.fetchone()[0])
        cur.close()
        # Dbpool.closeall()
        Dbpool.putconn(conn, None, True)
    return tile


def getRoute(tableName, x1, y1, x2, y2):
    print('start:' + str(x1) + ' ' + str(y1))
    print('end:' + str(x2) + ' ' + str(y2))
    conn = Dbpool.getconn()
    data = None
    if (conn):
        query = "SELECT st_asgeojson ( ( ST_MakeLine (st_transform (route.geom,4490) ) ) )  FROM ( SELECT geom FROM pgr_fromAtoB ( '"+tableName+"', %s,  %s,  %s,  %s ) ORDER BY seq ) AS route"
        # query = "SELECT ST_AsGeoJSON(geom) as route FROM pgr_dijkstra('SELECT gid AS id, source::integer,target::integer,length::double precision AS cost FROM "+tableName+"',%s,%s,false,false ) as di join "+tableName+" pt on di.id2 = pt.gid"
        cur = conn.cursor()
        cur.execute(query, (x1, y1, x2, y2))
        data = cur.fetchall()
        cur.close()
        Dbpool.putconn(conn, None, True)
        # Dbpool.closeall()
    return data


@app.route('/route/<string:tableName>/<float:x1>/<float:y1>/<float:x2>/<float:y2>', methods=['GET'])
def pgroute(tableName='', x1=0.0, y1=0.0, x2=0.0, y2=0.0):
    resulte = getRoute(tableName, x1, y1, x2, y2)
    data = {
        'data': resulte
    }
    response = make_response(jsonify(data))
    response.headers['Content-Type'] = "application/json"
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Methods'] = "POST,GET"
    return response


@app.route('/test/<float:a>', methods=['GET'])
def test(a=0.0):
    data = {
        'data': a
    }
    response = make_response(jsonify(data))
    response.headers['Content-Type'] = "application/json"
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Methods'] = "POST,GET"
    return response


@app.route('/tiles/<string:tableName>/<string:sourceLayer>/<int:z>/<int:x>/<int:y>', methods=['GET'])
def tiles(tableName='', sourceLayer='', z=0, x=0, y=0):
    start_time = time.time()
    tile = get_tile(tableName, sourceLayer, z, x, y)
    response = make_response(tile)
    response.headers['Content-Type'] = "application/x-protobuf"
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Methods'] = "POST,GET"
    end_time = time.time()
    print(".........耗时: %d s" % (end_time - start_time))
    return response


if __name__ == "__main__":
    app.debug = True
    app.run()

