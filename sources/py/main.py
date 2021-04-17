#######################################################
def main(fileContent):
	allLine = fileContent.split('\n')

	#筛选出与Magnetosome有关的部分
	allLineClean = []
	readable = False
	for line in allLine:
		if '>' in line:
			if 'Magnetosome' in line:
				allLineClean.append(line)
				readable = True
			elif readable:
				readable = False
		elif readable:
			allLineClean.append(line)

	#获取Magnetosome的行名、序号、蛋白名
	seqname = [] #行名
	seqname_tag = []#行名拆开后带有样本名的基因tag
	seqnumber = []#用于连续性比较的序号
	proname = []#蛋白名
	for line in allLineClean:
		if '>' in line:
			seqname.append(line)
			a = line.split()
			b = a[0]
			seqname_tag.append(b)
			c = b.split('_')
			seqnumber.append(int(c[1]))
			proindex = a.index('protein') + 1
			proname.append(a[proindex])

	#获取Mag序列
	allSeq = [] #所有Mag序列
	tmpSeq = ''
	for line in allLineClean:
		if '>' in line:
			if len(tmpSeq) > 0:
				allSeq.append(tmpSeq)
				tmpSeq = ''
		else:
			tmpSeq += line
	if tmpSeq != '':
		allSeq.append(tmpSeq)


	#获取连续基因
	MIN_LENGTH = 2 #序列被认为连续的最小长度
	MIN_DISTANCE = 2 #序列被认为断开的最小间隔

	maglist_tag = []
	templist = []
	seqname_tag_final = []#确定为磁小体蛋白的蛋白tag
	temp_seqname_tag_final = []#暂存的磁小体蛋白tag列表
	magpro_namelist = []#确定为磁小体蛋白的蛋白名列表
	temp_magpro_namelist = []#暂存的磁小体蛋白名列表
	magpro_seq = [] #确定为磁小体蛋白的序列
	temp_magpro_seq = [] #暂存的磁小体蛋白序列
	for index, i in enumerate(seqnumber):
		_len = len(templist)
		if _len == 0:
			templist.append(i)
			temp_seqname_tag_final.append(seqname_tag[index])
			temp_magpro_namelist.append(proname[index])
			temp_magpro_seq.append(allSeq[index])
		elif i - templist[-1] <= MIN_DISTANCE:
			templist.append(i)
			temp_seqname_tag_final.append(seqname_tag[index])
			temp_magpro_namelist.append(proname[index])
			temp_magpro_seq.append(allSeq[index])
		elif _len == 1:
			templist = [i]
			temp_seqname_tag_final =[seqname_tag[index]]
			temp_magpro_namelist = [proname[index]]
			temp_magpro_seq = [allSeq[index]]
		elif _len >= MIN_LENGTH: #每当出现断点，
			maglist_tag.append(templist) #更新maglist_tag
			seqname_tag_final.append(temp_seqname_tag_final)#更新磁小体基因tag
			magpro_namelist.append(temp_magpro_namelist)
			magpro_seq.append(temp_magpro_seq)
			templist = [i] #将templist清空
			temp_seqname_tag_final = [seqname_tag[index]]
			temp_magpro_namelist = [proname[index]]
			temp_magpro_seq = [allSeq[index]]
	if len(templist) >= MIN_LENGTH: #若循环结束后,templist中包含连续序列
		maglist_tag.append(templist)
		seqname_tag_final.append(temp_seqname_tag_final)
		magpro_namelist.append(temp_magpro_namelist)
		magpro_seq.append(temp_magpro_seq)

	print(maglist_tag)
	print(seqname_tag_final)
	print(magpro_namelist)
	#输出磁小体基因簇的长度/磁小体基因的个数
	magpro_number = 0
	for i in magpro_seq:
		magpro_number += len(i)
	print(magpro_number)
	# print(sum([len(i) for i in magpro_seq]))

	#把嵌套列表释放成一个列表
	tag = [i for j in seqname_tag_final for i in j]#磁小体基因的prokka注释标号
	name = [i for j in magpro_namelist for i in j]#磁小体基因的名称
	length = [len(i) for j in magpro_seq for i in j ]#磁小体基因的长度
	print(tag)
	print(name)
	print(length)
	
	for i in tag:
		locus_tag = i.split('>')[1]
		locus_tags.append(locus_tag)
	print(locus_tags)

	from browser import document, html
	dataArea = document['dataArea']
	for i in range(len(tag)):
		row = html.TR()
		row <= html.TD(i+1)
		row <= html.TD(tag[i])
		row <= html.TD(name[i])
		row <= html.TD(length[i])
		dataArea <= row

########################################################

from browser import window, document, bind

submitBtn = document['submitBtn']
fileContent = ''

@bind(submitBtn, 'click')
def read_file(ev):
	def getContent(event):
		fileContent = event.target.result
		main(fileContent)

	filename = document['fileUpload'].files[0]
	reader = window.FileReader.new()
	reader.readAsText(filename)
	reader.bind('load', getContent)

#####################################################
