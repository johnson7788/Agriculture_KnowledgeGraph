#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2021/9/30 9:57 上午
# @File  : import_csv.py
# @Author: johnson
# @Desc  :

from neo4j import GraphDatabase
class NEO4JExample():

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def excute(self, database):
        with self.driver.session(database=database) as session:
            session.write_transaction(self._import_data_pedia1)
            session.write_transaction(self._import_data_pedia2)
            session.write_transaction(self._create_Hudong_index)
            session.write_transaction(self._import_data_new_node)
            session.write_transaction(self._create_node_index)
            session.write_transaction(self._import_relaion2)
            session.write_transaction(self._import_relaion1)
            session.write_transaction(self._import_attr_Hudong2Hudong)
            session.write_transaction(self._import_attr_Hudong2Newnode)
            session.write_transaction(self._import_attr_Newnode2Newnode)
            session.write_transaction(self._import_attr_Newnode2Hudong)
            session.write_transaction(self._import_static_weather)
            session.write_transaction(self._create_weather_index)
            session.write_transaction(self._import_weather_plant)
            session.write_transaction(self._import_city_weather)


    @staticmethod
    def _import_data_pedia1(tx):
        file = f"http://127.0.0.1:8080/hudong_pedia.csv"
        sql = """
        LOAD CSV WITH HEADERS  FROM "%s" AS line  
CREATE (p:HudongItem{title:line.title,image:line.image,detail:line.detail,url:line.url,openTypeList:line.openTypeList,baseInfoKeyList:line.baseInfoKeyList,baseInfoValueList:line.baseInfoValueList}) 
        """ % file
        result = tx.run(sql)
        print(result)

    @staticmethod
    def _import_data_pedia2(tx):
        file = f"http://127.0.0.1:8080/hudong_pedia2.csv"
        sql = """
        LOAD CSV WITH HEADERS  FROM "%s" AS line  
CREATE (p:HudongItem{title:line.title,image:line.image,detail:line.detail,url:line.url,openTypeList:line.openTypeList,baseInfoKeyList:line.baseInfoKeyList,baseInfoValueList:line.baseInfoValueList}) 
        """ % file
        result = tx.run(sql)
        print(result)

    @staticmethod
    def _create_Hudong_index(tx):
        sql = """
        CREATE CONSTRAINT ON (c:HudongItem) ASSERT c.title IS UNIQUE
        """
        result = tx.run(sql)
        print(result)

    @staticmethod
    def _import_data_new_node(tx):
        file = f"http://127.0.0.1:8080/wikidataSpider/wikidataProcessing/new_node.csv"
        sql = """
        LOAD CSV WITH HEADERS  FROM "%s" AS line  
CREATE (:NewNode { title: line.title }) 
        """ % file
        result = tx.run(sql)
        print(result)
    @staticmethod
    def _create_node_index(tx):
        sql = """
        CREATE CONSTRAINT ON (c:NewNode) ASSERT c.title IS UNIQUE
        """
        result = tx.run(sql)
        print(result)
    @staticmethod
    def _import_relaion2(tx):
        file = f"http://127.0.0.1:8080/wikidataSpider/wikidataProcessing/wikidata_relation2.csv"
        sql = """
        LOAD CSV WITH HEADERS  FROM "%s" AS line  
        MATCH (entity1:HudongItem{title:line.HudongItem}) , (entity2:NewNode{title:line.NewNode})
        CREATE (entity1)-[:RELATION { type: line.relation }]->(entity2) 
        """ % file
        result = tx.run(sql)
        print(result)

    @staticmethod
    def _import_relaion1(tx):
        file = f"http://127.0.0.1:8080/wikidataSpider/wikidataProcessing/wikidata_relation.csv"
        sql = """
        LOAD CSV WITH HEADERS  FROM "%s" AS line  
        MATCH (entity1:HudongItem{title:line.HudongItem1}) , (entity2:HudongItem{title:line.HudongItem2})
        CREATE (entity1)-[:RELATION { type: line.relation }]->(entity2)
        """ % file
        result = tx.run(sql)
        print(result)
    @staticmethod
    def _import_attr_Hudong2Hudong(tx):
        file = f"http://127.0.0.1:8080/attributes.csv"
        sql = """
        LOAD CSV WITH HEADERS  FROM "%s" AS line  
    MATCH (entity1:HudongItem{title:line.Entity}), (entity2:HudongItem{title:line.Attribute})
    CREATE (entity1)-[:RELATION { type: line.AttributeName }]->(entity2);
        """ % file
        result = tx.run(sql)
        print(result)
    @staticmethod
    def _import_attr_Hudong2Newnode(tx):
        file = f"http://127.0.0.1:8080/attributes.csv"
        sql = """
        LOAD CSV WITH HEADERS  FROM "%s" AS line  
        MATCH (entity1:HudongItem{title:line.Entity}), (entity2:NewNode{title:line.Attribute})
        CREATE (entity1)-[:RELATION { type: line.AttributeName }]->(entity2);
        """ % file
        result = tx.run(sql)
        print(result)
    @staticmethod
    def _import_attr_Newnode2Newnode(tx):
        file = f"http://127.0.0.1:8080/attributes.csv"
        sql = """
        LOAD CSV WITH HEADERS  FROM "%s" AS line  
        MATCH (entity1:NewNode{title:line.Entity}), (entity2:NewNode{title:line.Attribute})
        CREATE (entity1)-[:RELATION { type: line.AttributeName }]->(entity2);
        """ % file
        result = tx.run(sql)
        print(result)
    @staticmethod
    def _import_attr_Newnode2Hudong(tx):
        file = f"http://127.0.0.1:8080/attributes.csv"
        sql = """
        LOAD CSV WITH HEADERS  FROM "%s" AS line  
        MATCH (entity1:NewNode{title:line.Entity}), (entity2:HudongItem{title:line.Attribute})
        CREATE (entity1)-[:RELATION { type: line.AttributeName }]->(entity2)  
        """ % file
        result = tx.run(sql)
        print(result)
    @staticmethod
    def _import_static_weather(tx):
        file = f"http://127.0.0.1:8080/wikidataSpider/weatherData/static_weather_list.csv"
        sql = """
        LOAD CSV WITH HEADERS  FROM "%s" AS line  
        MERGE (:Weather { title: line.title }) 
        """ % file
        result = tx.run(sql)
        print(result)
    @staticmethod
    def _create_weather_index(tx):
        sql = """
        CREATE CONSTRAINT ON (c:Weather) ASSERT c.title IS UNIQUE
        """
        result = tx.run(sql)
        print(result)
    @staticmethod
    def _import_weather_plant(tx):
        file = f"http://127.0.0.1:8080/wikidataSpider/weatherData/weather_plant.csv"
        sql = """
        LOAD CSV WITH HEADERS  FROM "%s" AS line  
        MATCH (entity1:Weather{title:line.Weather}) , (entity2:HudongItem{title:line.Plant})
        CREATE (entity1)-[:Weather2Plant { type: line.relation }]->(entity2)
        """ % file
        result = tx.run(sql)
        print(result)
    @staticmethod
    def _import_city_weather(tx):
        file = f"http://127.0.0.1:8080/wikidataSpider/weatherData/city_weather.csv"
        sql = """
        LOAD CSV WITH HEADERS  FROM "%s" AS line  
        MATCH (city{title:line.city}) , (weather{title:line.weather})
        CREATE (city)-[:CityWeather { type: line.relation }]->(weather)
        """ % file
        result = tx.run(sql)
        print(result)
if __name__ == "__main__":
    greeter = NEO4JExample(uri="bolt://localhost:7687", user="neo4j", password="welcome")
    greeter.excute(database="agriculture")
    greeter.close()