# -*- coding: utf-8 -*-
import MeCab
text = u'袋を開けた瞬間香る、バターの香りが食欲をそそります。 口に入れると、じゃがいもとバターの味の見事なバッティング。 とても、美味しいポテトチップスです 残念なのは、他のポテトチップスが一袋60gなのに対して この商品は58gと僅かに、せこい企業努力が見えて取れます。 2014/2/15注文→翌日到着。2014/2/13製造→14/6/13賞味期限 の物が届きました。注文時のご参考になれば幸いです。 期間限定商品です。アマゾンの値段も値頃なので買いやすい商品だと思います。'
nouns, verbs, adjs, advs = [], [], [], []
nounswords, verbswords, adjswords, advswords = [], [], [], []
nounspoint, verbspoint, adjspoint, advspoint = [], [], [], []

def analyze(hinsi, words, point):
	#品詞分解したwordと辞書のwordが一致するかチェック
	global score, number
	for i in hinsi:
		cnt=0
		for j in words:
			if i == j:
				print j, point[cnt]
				score+=float(point[cnt])
				number+=1
			cnt+=1

if __name__ == "__main__":
	#単語感情極性対応表を読み込む
	f = open('pn_ja.dic.txt', 'r')
	for line in f:
		line = line.rstrip()
		x = line.split(':')
		if abs(float(x[3]))>0:	#ポイントの調整
			if x[2] == '名詞':
				nounswords.append(x[0])
				nounspoint.append(x[3])
			if x[2] == '動詞':
				verbswords.append(x[0])
				verbspoint.append(x[3])
			if x[2] == '形容詞':
				adjswords.append(x[0])
				adjspoint.append(x[3])
			if x[2] == '副詞':
				advswords.append(x[0])
				advspoint.append(x[3])
	f.close()

	#mecabで文章を品詞分解する
	tagger = MeCab.Tagger('-Ochasen')
	node = tagger.parseToNode(text.encode('utf-8'))
	while node:
		if node.feature.split(",")[0] == '名詞':
			nouns.append(node.surface)
		if node.feature.split(",")[0] == '動詞':
			verbs.append(node.surface)
		if node.feature.split(",")[0] == '形容詞':
			adjs.append(node.surface)
		if node.feature.split(",")[0] == '副詞':
			advs.append(node.surface)
		node = node.next

	#辞書を使って感情分析する
	score=number=0
	analyze(nouns,nounswords,nounspoint)
	analyze(verbs,verbswords,verbspoint)
	analyze(adjs,adjswords,adjspoint)
	analyze(advs,advswords,advspoint)
	print score/number
