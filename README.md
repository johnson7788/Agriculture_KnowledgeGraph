# 测试

## 项目配置

**0.安装基本环境：**

确保安装好python3和Neo4j（任意版本）
 
安装一系列pip依赖： cd至项目根目录，运行 sudo pip3 install -r requirement.txt

**1.导入数据：**
import_csv.py
以上步骤是导入爬取到的关系


**2.下载词向量模型：（如果只是为了运行项目，步骤2可以不做，预测结果已经离线处理好了）**
 
~~http://s3-us-west-1.amazonaws.com/fasttext-vectors/wiki.zh.zip  
  将wiki.zh.bin放入 KNN_predict 目录 。~~


**3.修改Neo4j用户**

进入demo/Model/neo_models.py,修改第9行的neo4j账号密码，改成你自己的

**4.启动服务**

进入demo目录，然后运行脚本：

```
sudo sh django_server_start.sh
```

这样就成功的启动了django。我们进入8000端口主页面，输入文本，即可看到以下命名实体和分词的结果（确保django和neo4j都处于开启状态）

----------------------
###  (update 2018.11.11)
添加了农业知识问答
![](https://raw.githubusercontent.com/CrisJk/SomePicture/master/blog_picture/1541921074856.jpg)

###  (update 2018.10.26) 
- 修改部分配置信息
- 关系查询中，添加了2个实体间的最短路查询，从而挖掘出实体之间一些奇怪的隐含关系

![image](https://i.loli.net/2018/10/27/5bd3bf6ce4472.jpg)

### 农业实体识别+实体分类


![image](https://raw.githubusercontent.com/qq547276542/blog_image/master/agri/2.png)

点击实体的超链接，可以跳转到词条页面（词云采用了词向量技术）：

![image](https://raw.githubusercontent.com/qq547276542/blog_image/master/agri/3.png)

### 实体查询

实体查询部分，我们能够搜索出与某一实体相关的实体，以及它们之间的关系：
![image](https://raw.githubusercontent.com/CrisJk/SomePicture/master/blog_picture/entitySearch.png)

![](https://raw.githubusercontent.com/CrisJk/SomePicture/master/blog_picture/entitySearch2.png)

### 关系查询

关系查询即查询三元组关系entity1-[relation]->entity2 , 分为如下几种情况:

* 指定第一个实体entity1
* 指定第二个实体entity2
* 指定第一个实体entity1和关系relation
* 指定关系relation和第二个实体entity2
* 指定第一个实体entity1和第二个实体entity2
* 指定第一个实体entity1和第二个实体entity2以及关系relation

下图所示，是指定关系relation和第二个实体entity2的查询结果

![](https://raw.githubusercontent.com/CrisJk/SomePicture/master/blog_picture/relationSearch.png)



![](https://raw.githubusercontent.com/CrisJk/SomePicture/master/blog_picture/relationSearch2.png)

### 知识的树形结构

农业知识概览部分，我们能够列出某一农业分类下的词条列表，这些概念以树形结构组织在一起：

![image](https://raw.githubusercontent.com/qq547276542/blog_image/master/agri/6.png)

农业分类的树形图：

![image](https://raw.githubusercontent.com/qq547276542/blog_image/master/agri/5.png)

### 训练集标注

我们还制作了训练集的手动标注页面，每次会随机的跳出一个未标注过的词条。链接：http://localhost:8000/tagging-get , 手动标注的结果会追加到/label_data/labels.txt文件末尾：

我们将这部分做成了小工具，可复用：https://github.com/qq547276542/LabelMarker

![image](https://raw.githubusercontent.com/qq547276542/blog_image/master/agri/4.png)

(update 2018.04.07)  同样的，我们制作了标注关系提取训练集的工具，如下图所示

![](https://raw.githubusercontent.com/CrisJk/SomePicture/master/blog_picture/tagging.JPG)

如果Statement的标签是对的，点击True按钮；否则选择一个关系，或者输入其它关系。若当前句子无法判断，则点击Change One按钮换一条数据。

说明:　Statement是/wikidataSpider/TrainDataBaseOnWiki/finalData中train_data.txt中的数据，我们将它转化成json,导入到mongoDB中。标注好的数据同样存在MongoDB中另一个Collection中。关于Mongo的使用方法可以参考官方tutorial，或者利用这篇文章简单了解一下[MongoDB](http://crisjk.site/2018/04/04/MongoDB-Tutorial/) 

我们在MongoDB中使用两个Collections，一个是train_data，即未经人工标注的数据；另一个是test_data，即人工标注好的数据。

![](https://raw.githubusercontent.com/CrisJk/crisjk.github.io/master/resource/pictures/Agriculture-KnowledgeGraph-Data-README/mongo.png)



**使用方法**: 启动neo4j,mongodb之后，进入demo目录，启动django服务，进入127.0.0.1:8000/tagging即可使用




## 思路

### 命名实体识别:

使用thulac工具进行分词，词性标注，命名实体识别（仅人名，地名，机构名） 
为了识别农业领域特定实体，我们需要： 

1. 分词，词性标注，命名实体识别 
2. 以识别为命名实体（person，location，organzation）的，若实体库没有，可以标注出来 
3. 对于非命名实体部分，采用一定的词组合和词性规则，在O(n)时间扫描所有分词，过滤掉不可能为农业实体的部分（例如动词肯定不是农业实体） 
4. 对于剩余词及词组合，匹配知识库中以分好类的实体。如果没有匹配到实体，或者匹配到的实体属于0类（即非实体），则将其过滤掉。 
5. 实体的分类算法见下文。


### 实体分类：

#### 特征提取：

![image](https://raw.githubusercontent.com/qq547276542/blog_image/master/agri/1.png)


#### 分类器：KNN算法

- 无需表示成向量，比较相似度即可
- K值通过网格搜索得到

#### 定义两个页面的相似度sim(p1,p2)：

- 
  title之间的词向量的余弦相似度(利用fasttext计算的词向量能够避免out of vocabulary)
- 2组openType之间的词向量的余弦相似度的平均值
- 相同的baseInfoKey的IDF值之和（因为‘中文名’这种属性贡献应该比较小）
- 相同baseInfoKey下baseInfoValue相同的个数
- 预测一个页面时，由于KNN要将该页面和训练集中所有页面进行比较，因此每次预测的复杂度是O(n)，n为训练集规模。在这个过程中，我们可以统计各个分相似度的IDF值，均值，方差，标准差，然后对4个相似度进行标准化:**(x-均值)/方差**
- 上面四个部分的相似度的加权和为最终的两个页面的相似度，权值由向量weight控制，通过10折叠交叉验证+网格搜索得到


### Labels：（命名实体的分类）

| Label | NE Tags                                  | Example                                  |
| ----- | ---------------------------------------- | ---------------------------------------- |
| 0     | Invalid（不合法）                             | “色调”，“文化”，“景观”，“条件”，“A”，“234年”（不是具体的实体，或一些脏数据） |
| 1     | Person（人物，职位）                            | “袁隆平”，“副市长”                         |
| 2     | Location（地点，区域）                          | “福建省”，“三明市”，“大明湖”                        |
| 3     | Organization（机构，会议）                      | “华东师范大学”，“上海市农业委员会”                      |
| 4     | Political economy（政治经济名词）                | “惠农补贴”，“基本建设投资”                          |
| 5     | Animal（动物学名词，包括畜牧类，爬行类，鸟类，鱼类，等）          | “绵羊”，“淡水鱼”，“麻雀”                          |
| 6     | Plant（植物学名词，包括水果，蔬菜，谷物，草药，菌类，植物器官，其他植物）  | “苹果”，“小麦”，“生菜”                           |
| 7     | Chemicals（化学名词，包括肥料，农药，杀菌剂，其它化学品，术语等）    | “氮”，“氮肥”，“硝酸盐”，“吸湿剂”                     |
| 8     | Climate（气候，季节）                           | “夏天”，“干旱”                                |
| 9     | Food items（动植物产品）                        | “奶酪”，“牛奶”，“羊毛”，“面粉”                      |
| 10    | Diseases（动植物疾病）                          | “褐腐病”，“晚疫病”                              |
| 11    | Natural Disaster（自然灾害）                   | “地震”，“洪水”，“饥荒”                           |
| 12    | Nutrients（营养素，包括脂肪，矿物质，维生素，碳水化合物等）       | “维生素A”，"钙"                               |
| 13    | Biochemistry（生物学名词，包括基因相关，人体部位，组织器官，细胞，细菌，术语） | “染色体”，“血红蛋白”，“肾脏”，“大肠杆菌”                 |
| 14    | Agricultural implements（农机具，一般指机械或物理设施）  | “收割机”，“渔网”                               |
| 15    | Technology(农业相关术语，技术和措施)                 | “延后栽培"，“卫生防疫”，“扦插”                       |
| 16    | other（除上面类别之外的其它名词实体，可以与农业无关但必须是实体）      | “加速度"，“cpu”，“计算机”，“爱鸟周”，“人民币”，“《本草纲目》”，“花岗岩” |


### 关系抽取

使用远程监督方法构建数据集，利用tensorflow训练PCNN模型
详情见： [relationExtraction](https://github.com/qq547276542/Agriculture_KnowledgeGraph/tree/master/relationExtraction)
