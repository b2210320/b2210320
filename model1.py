import pandas as pd
from pysummarization.tokenizabledoc.mecab_tokenizer import MeCabTokenizer

from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor
from pysummarization.nlp_base import NlpBase
from pysummarization.similarityfilter.tfidf_cosine import TfIdfCosine
from pysummarization.tokenizabledoc.simple_tokenizer import SimpleTokenizer

def summary(text):
    #print('txtファイル(UTF-8）を指定してください')
    #uploaded = files.upload()
    #
    # for fn in uploaded.keys():
    #   print('User uploaded file "{name}" with length {length} bytes'.format(name=fn, length=len(uploaded[fn])))

    #  #@title 類似性フィルターカットオフ設定（Defalt = 0.25） { run: "auto" }
    similarity_limit = 0.25 #@param {type:"slider", min:0.05, max:0.5, step:0.05}

    # if len(uploaded.keys()) != 1:
    #     print("アップロードは１ファイルにのみ限ります")
    # else:
    #     target = list(uploaded.keys())[0]

    # with open(target) as f:
    #     contents = f.readlines()

    document = ''.join(text).replace(' ', '').replace(' ', '')


    # print(u'[原文書]')
    # print(document)

    # # 自動要約のオブジェクト
    auto_abstractor = AutoAbstractor()
    # # トークナイザー設定（MeCab使用）
    auto_abstractor.tokenizable_doc = MeCabTokenizer()
    # # 区切り文字設定
    auto_abstractor.delimiter_list = ["。", "\n"]
    # # 抽象化&フィルタリングオブジェクト
    abstractable_doc = TopNRankAbstractor()
    # # 文書要約
    result_dict1 = auto_abstractor.summarize(document, abstractable_doc)

    print(u'[要約結果]')
    # # 出力
    for sentence in result_dict1["summarize_result"]:
        print(sentence)

    # NLPオブジェクト
    nlp_base = NlpBase()
    # トークナイザー設定（MeCab使用）
    nlp_base.tokenizable_doc = MeCabTokenizer()
    # 類似性フィルター
    similarity_filter = TfIdfCosine()
    # NLPオブジェクト設定
    similarity_filter.nlp_base = nlp_base
    # 類似性limit：limit超える文は切り捨て
    similarity_filter.similarity_limit = similarity_limit

    # 自動要約のオブジェクト
    auto_abstractor = AutoAbstractor()
    # トークナイザー設定（MeCab使用）
    auto_abstractor.tokenizable_doc = MeCabTokenizer()
    # 区切り文字設定
    auto_abstractor.delimiter_list = ["。", "\n"]
    # 抽象化&フィルタリングオブジェクト
    abstractable_doc = TopNRankAbstractor()
    # 文書要約（similarity_filter機能追加）
    result_dict2 = auto_abstractor.summarize(document, abstractable_doc, similarity_filter)

    print(u'[要約結果：Similarity Filter機能]')
    # 出力
    for sentence in result_dict2["summarize_result"]:
        print(sentence)

    doc0 = ''.join(s for s in document)
    doc1 = result_dict1["summarize_result"]
    doc2 = result_dict2["summarize_result"]
    doc1 = ''.join(s for s in doc1)
    doc2 = ''.join(s for s in doc2)
    lst1 = ["原文書","要約文書","要約文書:SF"]
    lst2 = [doc0,doc1,doc2]
    df = pd.DataFrame(list(zip(lst1,lst2)), columns = ['Class.','Content'])
    df = df.replace( '\n', '', regex=True)
    return df.iloc[1,1]
    #print(df)

    #with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.colheader_justify','light', 'display.width', 2000, 'display.max_colwidth', 500):
        # df = df.stack().str.lstrip().unstack()
        # df = df.style.set_properties(**{'text-align': 'left'})


        
            