#!/usr/bin/python3
import sys
import random

FDIR = ''

def gen(user, id, hobby_id, comment1_cnt, comment0_cnt):
	#print(FDIR)
	#print(user[0])
	src_name = "./done/" + FDIR + "/" + FDIR + '_' + id + ".csv"
	print(src_name)
	random.seed(int(id))
	random.shuffle(user)
	#print(user[0])
	fil = open(src_name, 'w', encoding="gbk")
	fil.write("index	type	param	status\n")
	for idx, val in enumerate(user):
		if idx < comment1_cnt:
			typ = 1
		elif idx < comment0_cnt:
			typ = 0
		else:
			typ = 2

		fil.write("%d\tgive_five\t%s;%s;%s\t%d\n%d\tsleep\t5\t%d\n" % (idx + 1, val, id, hobby_id, typ, idx + 1, typ))
		#print(idx, val)
	fil.close()

def get_user():
	fil = open("users.csv")
	data = fil.readlines()[1:];
	fil.close()
	#print (data)
	user = list(map(lambda x: x.split('\t')[1], data))
	#print(user)
	return user
if __name__ == '__main__':
	user = get_user()
	FDIR = sys.argv[1]
	#print(FDIR)
	src_name = './doc/' + FDIR + '.csv'
	#print(src_name)
	fil = open(src_name, 'r', encoding="gbk")
	data = fil.readlines()[1:];
	fil.close()
	#print(data)
	for line in data:
		print(line)
		info = line.split(',')
		idx = info[0]
		hobby_id = info[1]
		id = info[2]
		comment_cnt = info[3]
		comment1_cnt = int(info[4])
		comment0_cnt = int(info[5])
		gen(user.copy(), id, hobby_id, comment1_cnt, comment0_cnt)