from flask import Flask,render_template,request,send_from_directory,redirect,url_for
import x8

app = Flask(__name__,template_folder='./templates')

@app.route('/')
def index():
	cookie=request.cookies
	name=cookie.get('name')
	pwd=cookie.get('pwd')
	if name==None:
		return render_template('index.html',word='🤖目前还未注册 or 登陆, 无法使用收藏功能!',data=x8.analysis_page(1),page=True,next_page=2,user=False)
	else:
		return render_template('index.html',word='🌈欢迎! %s'%name,data=x8.analysis_page(1),page=True,next_page=2,user=True)

@app.route('/video/<string:vid>')
def video(vid):
	cookie=request.cookies
	name=cookie.get('name')
	pwd=cookie.get('pwd')
	if name==None:
		return render_template('video.html',word='👽目前还未注册 or 登陆, 无法使用收藏功能!',data=x8.analysis_video(vid),vid=vid,user=False)
	else:
		return render_template('video.html',word='🎉欢迎! %s'%name,data=x8.analysis_page(1),vid=vid,user=True)

@app.route('/page/<string:page>')
def page(page):
	cookie=request.cookies
	name=cookie.get('name')
	pwd=cookie.get('pwd')
	if int(page)==1:
		if name==None:
			return render_template('index.html',word='👾目前还未注册 or 登陆, 无法使用收藏功能!',data=x8.analysis_page(1),page=True,next_page=2,user=False)
		else:
			return render_template('index.html',word='🔥欢迎! %s'%name,data=x8.analysis_page(1),page=True,next_page=2,user=True)
	else:
		if name==None:
			return render_template('index.html',word='👻目前还未注册 or 登陆, 无法使用收藏功能!',data=x8.analysis_page(page),page=False,next_page=int(page)+1,previous_page=int(page)-1,user=False)
		else:
			return render_template('index.html',word='⭐欢迎! %s'%name,data=x8.analysis_page(page),page=False,next_page=int(page)+1,previous_page=int(page)-1,user=True)
