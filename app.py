from flask import Flask,render_template,request,send_from_directory,redirect,make_response
import x8
import json

app = Flask(__name__,template_folder='./templates')

# 添加用户
def add_user(name,pwd):
	with open('.user.json','r')as file:
		old_data=json.loads(file.read())
	old_data.append({'name':name,'pwd':pwd,'star':[]})
	with open('.user.json','w')as file:
		file.write(json.dumps(old_data,ensure_ascii=False))

# 检查新/老用户, 密码是否正确
def check_user(name,pwd):
	with open('.user.json','r')as file:
		data=json.loads(file.read())
	for u in data:
		if u['name']==name:
			if u['pwd']==pwd:
				return 'old'
			else:
				return 'pwd'
	return 'new'

# 为用户收藏视频
def like_video(name,vid):
	vdata=x8.analysis_video(vid)
	vdata['vid']=vid
	with open('.user.json','r')as file:
		data=json.loads(file.read())
	for u in data:
		if u['name']==name:
			u['star'].append(vdata)
	with open('.user.json','w')as file:
		file.write(json.dumps(data,ensure_ascii=False))

# 为用户取消收藏视频
def hate_video(name,vid):
	vdata=x8.analysis_video(vid)
	vdata['vid']=vid
	with open('.user.json','r')as file:
		data=json.loads(file.read())
	for u in data:
		if u['name']==name:
			try:
				u['star'].remove(vdata)
			except ValueError:
				return False
	with open('.user.json','w')as file:
		file.write(json.dumps(data,ensure_ascii=False))
	return True

# 获取用户的收藏列表
def get_star(name):
	with open('.user.json','r')as file:
		data=json.loads(file.read())
	for u in data:
		if u['name']==name:
			return u['star']

# 获取网站信息
def get_realtime():
	with open('.user.json','r')as file:
		data=json.loads(file.read())
	user_num=len(data)
	video=[]
	for u in data:
		video.append(len(u['star']))
	return {'user_num':user_num,'video_num':sum(video)}

# index页面
@app.route('/')
def index():
	cookie=request.cookies
	name=cookie.get('name')
	pwd=cookie.get('pwd')
	info=get_realtime()
	if name==None:
		return render_template('index.html',word='🤖 目前还未注册 or 登陆, 无法使用收藏功能!',page_word='首页',data=x8.analysis_page(1),page=True,next_page=2,user=False,user_num=info['user_num'],video_num=info['video_num'])
	else:
		return render_template('index.html',word='🌈 欢迎! %s'%name,page_word='首页',data=x8.analysis_page(1),page=True,next_page=2,user=True,user_num=info['user_num'],video_num=info['video_num'])

# 视频页面
@app.route('/video/<string:vid>')
def video(vid):
	cookie=request.cookies
	name=cookie.get('name')
	pwd=cookie.get('pwd')
	info=get_realtime()
	if name==None:
		return render_template('video.html',word='👽 目前还未注册 or 登陆, 无法使用收藏功能!',data=x8.analysis_video(vid),vid=vid,user=False,user_num=info['user_num'],video_num=info['video_num'])
	else:
		return render_template('video.html',word='🎉 欢迎! %s'%name,data=x8.analysis_video(vid),vid=vid,user=True,user_num=info['user_num'],video_num=info['video_num'])

# 页面
@app.route('/page/<string:page>')
def page(page):
	cookie=request.cookies
	name=cookie.get('name')
	pwd=cookie.get('pwd')
	info=get_realtime()
	if int(page)==1:
		if name==None:
			return render_template('index.html',word='👾 目前还未注册 or 登陆, 无法使用收藏功能!',data=x8.analysis_page(1),page=True,next_page=2,page_word='首页',user=False,user_num=info['user_num'],video_num=info['video_num'])
		else:
			return render_template('index.html',word='🔥 欢迎! %s'%name,data=x8.analysis_page(1),page=True,next_page=2,page_word='首页',user=True,user_num=info['user_num'],video_num=info['video_num'])
	else:
		if name==None:
			return render_template('index.html',word='👻 目前还未注册 or 登陆, 无法使用收藏功能!',data=x8.analysis_page(page),page=False,next_page=int(page)+1,previous_page=int(page)-1,page_word='第%s页'%page,user=False,user_num=info['user_num'],video_num=info['video_num'])
		else:
			return render_template('index.html',word='⭐ 欢迎! %s'%name,data=x8.analysis_page(page),page=False,next_page=int(page)+1,previous_page=int(page)-1,page_word='第%s页'%page,user=True,user_num=info['user_num'],video_num=info['video_num'])

# 登陆页面
@app.route('/login',methods=['POST','GET'])
def login():
	info=get_realtime()
	if request.method=='POST':
		name=request.form['name']
		pwd=request.form['pwd']
		truth=check_user(name,pwd)
		if truth=='new':
			add_user(name,pwd)
		elif truth=='old':
			pass
		else:
			return render_template('login.html',word='💔 密码错误或此用户名已被注册!',login=True,user_num=info['user_num'],video_num=info['video_num'])
		response=make_response(redirect('/'))
		response.set_cookie('name',name,max_age=2419200)
		response.set_cookie('pwd',pwd,max_age=2419200)
		return response
	else:
		return render_template('login.html',word='🤔 起一个什么名字好呢...',login=True,user_num=info['user_num'],video_num=info['video_num'])

# 收藏页面
@app.route('/star')
def star():
	cookie=request.cookies
	name=cookie.get('name')
	pwd=cookie.get('pwd')
	info=get_realtime()
	if name==None:
		return render_template('login.html',word=' 🤖目前还未注册 or 登陆, 无法使用收藏功能!',user_num=info['user_num'],video_num=info['video_num'])
	else:
		data=get_star(name)
		return render_template('star.html',word='🌈 %s的收藏 (共%s个) :'%(name,len(data)),data=data,user=True,user_num=info['user_num'],video_num=info['video_num'])

# 收藏视频的动作
@app.route('/like/<string:vid>')
def like(vid):
	cookie=request.cookies
	name=cookie.get('name')
	pwd=cookie.get('pwd')
	info=get_realtime()
	if name==None:
		return render_template('login.html',word='🤖 目前还未注册 or 登陆, 无法使用收藏功能!',user_num=info['user_num'],video_num=info['video_num'])
	else:
		like_video(name,vid)
		return '<meta http-equiv=\"refresh\" content=\"1; url=%s\"><p>收藏成功, 正在返回视频页面...</p>'%'/video/%s'%vid

# 取消收藏视频的动作
@app.route('/hate/<string:vid>')
def hate(vid):
	cookie=request.cookies
	name=cookie.get('name')
	pwd=cookie.get('pwd')
	info=get_realtime()
	if name==None:
		return render_template('login.html',word='🤖 目前还未注册 or 登陆, 无法使用取消收藏功能!',user_num=info['user_num'],video_num=info['video_num'])
	else:
		if hate_video(name,vid)==False:
			return '<meta http-equiv=\"refresh\" content=\"1; url=%s\"><p>没收藏怎么取消收藏, 正在返回视频页面...</p>'%'/video/%s'%vid
		else:
			return '<meta http-equiv=\"refresh\" content=\"1; url=%s\"><p>取消收藏成功, 正在返回视频页面...</p>'%'/video/%s'%vid

# 关于页面
@app.route('/about')
def about():
	cookie=request.cookies
	name=cookie.get('name')
	if name==None:
		name='无名绅士'
	info=get_realtime()
	return render_template('about.html',word='🎉 欢迎不知道来自哪里的%s!'%name,user_num=info['user_num'],video_num=info['video_num'])

# 退出登陆
@app.route('/logout')
def logout():
	response = make_response(redirect('/'))
	response.set_cookie('name', '', expires=0)
	return response