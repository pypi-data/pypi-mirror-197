#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : es
# @Time         : 2023/3/14 上午10:38
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from whoosh import scoring
from whoosh.fields import *
from whoosh.filedb.filestore import FileStorage

from jieba.analyse import ChineseAnalyzer

# ME
from meutils.pipe import *


class ES(object):

    def __init__(self, indexdir, indexname='MAIN'):
        Path(indexdir).mkdir(parents=True, exist_ok=True)

        self.storage = FileStorage(indexdir)
        self.indexname = indexname

        self.ix = None
        self.searcher = None
        if self.storage.index_exists(indexname=indexname):
            self.ix = self.storage.open_index(indexname)
            self.searcher = self.ix.searcher()

    def create_index(self, df, schema, procs=4, limitmb=1024 * 2):
        self.ix = self.storage.create_index(schema, indexname=self.indexname)
        writer = self.ix.writer(procs=procs, multisegment=True, limitmb=limitmb)
        for fields in tqdm(df.to_dict('r'), 'Create Index'):
            writer.add_document(**fields)
        writer.commit()
        self.searcher = self.ix.searcher()

    def find(self, defaultfield, querystring, limit=1, return_fields=True, **kwargs):
        """

        @param defaultfield:
        @param querystring:
        @param limit:
        @param kwargs:
        @return:
        """
        assert self.ix is not None, 'please specify index !!!'

        hits = self.searcher.find(defaultfield, querystring, limit=limit, **kwargs)
        if return_fields:
            return hits | xmap_(lambda x: x.fields())
        else:
            return hits


if __name__ == '__main__':
    df = pd.DataFrame([{'id': '1', 'text': '周杰伦'}])
    schema = Schema(
        id=ID(stored=True),
        text=TEXT(stored=True, analyzer=ChineseAnalyzer(cachesize=-1))  # 无界缓存加速
    )

    es = ES('index')
    es.create_index(df, schema)
    print(es.find('text', '周杰伦'))
