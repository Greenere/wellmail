#coding=utf-8

#收信模块

#Lower level email retrieving module
#Written by Haoyang Li

import os
import email.mime.multipart
import email.message
import imaplib
import base64

def getEmailIMAP4(fmail,password,maildir='INBOX',new=True,seen=False):
    """
    :param fmail: 收件账户
    :param password: 收件账户密码
    :param maildir: 收取文件夹(默认为'INBOX'，即收件箱)
    :param new: 是否只获取未读邮件（默认为是）
    :param seen: 是否告诉服务器已经读取邮件（默认为否）
    :return messagelist: 邮件列表
    """
    mail_host='imap.'+fmail.split('@')[-1]
    search_flag='unseen' if new else 'all'
    #连接IMAP4服务器，登陆账户，选择收取邮件的邮件夹（默认为收件箱），取出可以收取的邮件标识列表
    imapObj=imaplib.IMAP4_SSL(mail_host)
    imapObj.login(fmail,password)
    imapObj.select(maildir)
    type,seq=imapObj.search(None,search_flag)
    messagelist=[]
    for num in seq[0].split():
        #根据标识列表seq[0]中的标识，依次收取各个邮件
        try:
            type,data=imapObj.fetch(num,'(RFC822)')#.HEADER
            message=email.message_from_bytes(data[0][1])
            messagelist.append(message)
            if seen:
                imapObj.store(num,'+FLAGS','\\Seen')
            #解析收取到的邮件
            psd=parseEmail(message)
            #保存收取到的邮件
            filestate=saveParsedEmail(psd,username=fmail)
            #更新邮件列表文件
            filename=psd['date']
            for s in ['[','\\',':','*','?','<','>','|',']']:
                filename=filename.replace(s,"")
            saveFileList(username=fmail,filename=filename)
            #print(filestate)
        except:
            pass
    #关闭连接
    imapObj.close()
    imapObj.logout()
    #返回未解析的邮件列表
    return messagelist

def deleteEmailIMAP4(fmail,password,dpsd=None,maildir='INBOX'):
    """
    :param fmail: 账户
    :param password: 密码
    :param dpsd: 要删除的邮件字典
    :param maildir: 要删除的邮件文件夹（默认为收件箱）
    :return bool:是否成功删除
    """
    mail_host = 'imap.' + fmail.split('@')[-1]
    search_flag = 'all'
    #连接IMAP4服务器，登陆账户，选择收件箱
    imapObj = imaplib.IMAP4_SSL(mail_host)
    imapObj.login(fmail, password)
    imapObj.select(maildir)
    #搜索可以收取的邮件标识列表
    type, seq = imapObj.search(None, search_flag)
    delstate=False
    for num in seq[0].split():
        #针对每个邮件收取其邮件头，比对时间戳进行删除
        #对于无时间戳的邮件，比对发件人和主题进行删除（几乎不会出现）
        try:
            type, data = imapObj.fetch(num, '(RFC822.HEADER)')
            message = email.message_from_bytes(data[0][1])
            psd=parseEmail(message)
            match1=False
            match2=False
            if dpsd['date']==psd['date']:
                match1=True
            if dpsd['from']==psd['from'] and dpsd['subject']==psd['subject']:
                match2=True
            if match1:
                imapObj.store(num, '+FLAGS', '\\Deleted')
                delstate=True
                return delstate
            else:
                if match2:
                    if dpsd==psd:
                        imapObj.store(num, '+FLAGS', '\\Deleted')
                        delstate = True
                        return delstate
        except:
            #出现问题表示在线删除失败，可能是在线的邮件已经在别处进行了删除操作
            return False
    return delstate


def parseEmail(message,flag='Empty'):
    """
    :param message: 结构化邮件
    :param flag: 本地邮件状态标志（默认为"Empty'）
    :return parsedict: 邮件完整内容(包含主题、正文、发件人、收件人、附件)
    """
    parsedict={}
    #解析主题，发件人，收件人
    for key in ['subject','from','to']:
        parsedict[key]=''
        try:
            header=email.header.decode_header(message[key])
            for hd in header:
                if hd[-1]:
                    parsedict[key]+=hd[0].decode(hd[-1])
                else:
                    parsedict[key]+=hd[0].decode('utf8')
            if parsedict[key] is None:
                parsedict[key]='-'
            if parsedict[key]=='':
                parsedict[key]='-'
        except:
            parsedict[key]=str(message[key])
    #解析时间
    parsedict['date'] = message['date']
    if parsedict['date'] is None:
        parsedict['date']= '-'
    #解析编码信息
    parsedict['charset']=message['charset'] if message['charset'] else 'utf8'
    #解析有效载荷（一般是正文）
    try:
        parsepayload=parsePayload(message)
        parsedict['payload']=parsepayload
    except:
        parsedict['payload']=None
    #解析附件
    try:
        parsefile=parseFile(message)
        parsedict['file']=parsefile
    except:
        parsedict['file']={'filename':[],'filedata':[]}
    parsedict['flag']=flag
    return parsedict

def parseFile(message):
    """
    :param message: 结构化邮件
    :return parsefile: 附件内容(为一字典)
    """
    parsefile={}
    parsefile['filename']=[]
    parsefile['filedata']=[]
    for msg in message.walk():
        #获取附件名
        filename=msg.get_filename()
        if filename:
            #解析附件名
            header=email.header.Header(filename)
            dh=email.header.decode_header(header)
            filename=dh[0][0]
            if filename.find(b'=?') != -1 and filename.find(b'?=') != -1:
                try:
                    fsplit=filename.split(b'?')
                    fcode=fsplit[1]
                    fname=fsplit[-2]
                    filename=base64.decodebytes(fname).decode(fcode.decode())
                except:
                    pass
            if dh[0][-1]:
                try:
                    filename=filename.decode(dh[0][-1])
                except:
                    pass
            #获取附件数据
            filedata=msg.get_payload(decode=True)
            fns = filename.split('.')
            if fns[-1] == fns[-2]:
                filename = ''
                fns.pop(-1)
                for n in range(0,len(fns)):
                    filename += fns[n]
                    if n<len(fns)-1:
                        filename+='.'
            #添加附件名和附件数据到附件字典
            parsefile['filename'].append(filename)
            parsefile['filedata'].append(filedata)
    return parsefile

def parsePayload(message):
    """
    :param message: 结构化邮件
    :return parsepayload: 邮件正文(为一字典)
    """
    trim=False
    parsepayload={}
    #获取有效载荷列表，如果是单载荷简单邮件则将其转换成列表
    payloadlist = message.get_payload()
    if type(payloadlist) != type([]):
        payloadlist=[message]
    #记录载荷数目
    parsepayload['num'] = len(payloadlist)
    for num in range(0, parsepayload['num']):
        if parsepayload['num'] > 1:
            #多载荷时依次解析载荷，若载荷为文件则content为None
            if payloadlist[num].is_multipart():
                content = payloadlist[num].get_payload()
            else:
                content = payloadlist[num].get_payload(decode=True)
        else:
            #单载荷时获取该载荷
            content =payloadlist[0].get_payload(decode=True)
        #如果载荷不是文件则进行进一步处理
        if content:
            try:
                 #尝试进一步解析载荷（防止多重嵌套）
                 if type(content) is type([]):
                     trim=True
                     content=content[-1].get_payload(decode=True)
            except:
                 pass
            try:
                #尝试采用默认编码解码载荷，否则采用国标码
                content=content.decode()
            except:
                try:
                    content=content.decode('gbk')
                except:
                    try:
                        content=content.decode()
                    except:
                        pass
                    
            #将载荷加入邮件字典
            parsepayload['content' + str(num)] = str(content)
        if trim==True:
            parsepayload['content1']=parsepayload['content0']
    return parsepayload

def saveParsedEmail(parsedict,filepath=os.getcwd(),filename=None,username='well'):
    """
    :param parsedict: 邮件解析结果(为一字典)
    :param filepath: 邮件存储路径(默认为当前工作路径）
    :param filename: 邮件存储名称
    :param username: 用户名
    :return filestate: 邮件存储结果
    """
    filepath=filepath+'\\user\\user_maildata'+'\\'+username
    filestate =''
    #将邮件以字典的格式写入一个文件以方便读取，文件名为时间戳去除非法字符
    try:
        if filename:
            fp=open(filepath+'\\'+filename,'w',encoding='utf8')
        else:
            filename=parsedict['date']
            for s in ['[','\\',':','*','?','<','>','|',']']:
                filename=filename.replace(s,"")
            fp=open(filepath+'\\'+filename+'.wellmail','w',encoding='utf8')
        fp.write(str(parsedict))
        filestate+='邮件正文成功写入文件\n'
        fp.close()
        filestate+='邮件：《'+parsedict['subject']+'》完整写入文件'+filename+'\n'
    except:
        filestate+='邮件：《'+parsedict['subject']+'》未能完整写入文件'+filename+'\n'
    #print(filestate)
    #有附件时保存附件
    if parsedict['file']['filename'] != []:
        fpstate='有附件'+str(parsedict['file']['filename'])+'\n'
        #print(fpstate)
        try:
            fc=0
            for fn in parsedict['file']['filename']:
                fd=parsedict['file']['filedata'][fc]
                fsd=saveParsedFile(fn,fd,filepath)
                fc+=1
                #print(fsd)
            fpstate+='附件'+str(parsedict['file']['filename'])+'保存成功\n'
        except:
            fpstate+='附件保存失败\n'
    else:
        fpstate='没有附件\n'
    filestate+=fpstate
    #print(fpstate)
    return filestate

def saveParsedFile(psfname,psfdata,filepath,filename=None):
    """
    :param psfname: 附件名称列表
    :param psfdata: 附件数据列表
    :param filepath: 存储路径
    :param filename: 存储名称
    :return filestate: 附件存储结果
    """
    #保存附件
    try:
        #print(filepath,filename)
        if filename:
            try:
                fp=open(filepath,'wb')
                #print(filepath)
            except:
                filepath = filepath + '\\' + filename
                fp = open(filepath, 'wb')
                #print(filepath)
            svname=filename
        else:
            try:
                fp=open(filepath,'wb')
                #print(filepath)
            except:
                filepath = filepath + '\\' + psfname
                fp = open(filepath, 'wb')
                #print(filepath)
            svname=psfname
        #print(svname)
        #print('fileopen')
        fp.write(psfdata)
        #print('filewrite')
        fp.close()
        filestate='文件:'+psfname+'已经成功保存为'+svname
    except:
        filestate='文件:'+psfname+'保存失败'
    return filestate

def saveFileList(filepath=os.getcwd(),username='well',filename=None):
    #保存邮件列表
    #首先尝试添加，否则直接将该文件夹中的文件名写入邮件列表文件
    filepath=filepath+'\\user\\user_maildata'+'\\'+username
    if os.path.exists(filepath+'\\'+'wellmaillist.welllist'):
        #print('exists')
        if filename:
            fp=open(filepath+'\\'+'wellmaillist.welllist','r')
            text=fp.read()
            fp.close()
            text=text+filename+'.wellmail\n'
            fp = open(filepath + '\\' + 'wellmaillist.welllist', 'w')
            fp.write(text)
            fp.close()
        return
    os.system('dir /b '+filepath+' > '+filepath+'\\wellmaillist.welllist')

def readWellmailDir(filepath=os.getcwd(),username='well'):
    """
    :param filepath:文件路径（默认为当前工作路径)
    :param username: 用户名（默认为well）
    :return psdlist:该文件夹中的邮件字典列表
    """
    try:
        #根据邮件列表文件读取用户邮件夹中的邮件
        filepath=filepath+'\\user\\user_maildata'+'\\'+username
        try:
            fp=open(filepath+'\\'+'wellmaillist.welllist','r')
        except:
            os.system('dir /b ' + filepath + '\\' + username + ' > ' + filepath + '\\' + username + '\\wellmaillist.txt')
            fp = open(filepath + '\\' + 'wellmaillist.welllist', 'r')
        filelist=fp.read()
        fp.close()
        filelist=filelist.split('\n')
        readstate='文件列表已经读取\n'
        psdlist=[]
        for wellmail in filelist:
            psd=readWellmailFile(filepath,wellmail)
            if type(psd)==type({}):
                psdlist.append(psd)
            readstate+='已经读取文件'+wellmail+'\n'
        return psdlist
    except:
        return []

def readWelllist(filepath=os.getcwd(),username='well'):
    """
    :param filepath: 文件路径（默认为当前工作路径）
    :param username: 用户名（默认为well)
    :return filelist: 文件名称列表
    """
    #读取邮件列表
    try:
        saveFileList(filepath,username)
        filepath=filepath+'\\user\\user_maildata'+'\\'+username
        try:
            fp=open(filepath+'\\'+'wellmaillist.welllist','r')
        except:
            os.system('dir /b ' + filepath + '\\' + username + ' > ' + filepath + '\\' + username + '\\wellmaillist.txt')
            fp = open(filepath + '\\' + 'wellmaillist.welllist', 'r')
        filelist=fp.read()
        fp.close()
        filelist=filelist.split('\n')
        tempfilelist=filelist.copy()
        for file in filelist:
            if file.split('.')[-1]!='wellmail':
                tempfilelist.remove(file)
        readstate='文件列表已经读取\n'
        filelist=tempfilelist
        return filelist
    except:
        readstate='文件列表读取失败\n'
        return []

def readWellmailFile(filepath,filename):
    """
    :param filepath: 文件路径
    :param filename: 文件名
    :return parsedict: 从文件中解析出的邮件字典
    """
    #读取邮寄
    if filename.split('.')[-1]!='wellmail':
        return '文件格式有误（应为wellmail文件）'
    try:
        fp=open(filepath+'\\'+filename,'r',encoding='utf8')
        lines=fp.read()
        fp.close()
        #因为邮件以字典的形式保存，直接用eval语句便可读取
        parsedict=eval(lines)
        return parsedict
    except:
        return '文件'+filename+'不存在或读取出错\n'

if __name__ == '__main__':
    fmail='lihaoyangsohu@sohu.com'
    password=''
    msg_list=getEmailIMAP4(fmail,password,new=True)
    psdl=[]
    for msg in msg_list:
        psdl.append(parseEmail(msg))
    for msg in msg_list:
        filestate=saveParsedEmail(parseEmail(msg),username='well_test')
        saveFileList(username='well_test')
    psdlist=readWellmailDir(username='well_test')
    for psd in psdlist:
       print(psd['date'])

"""
parseDict结构：
parsedict-['subject'字符串, 'from'字符串, 'to'字符串, 'date'字符串, 'charset'字符串, 'payload'字典, 'file'字典,'flag'邮件状态标志]
payload-['num'数字, 'content0'数据, 'content1'数据]
file-['filename'字符串列表, 'filedata'二进制数据列表]
wellmail文件直接保存字典内容部分
同时在相应文件夹中生成wellmaillist.welllist文件，保存wellmail文件列表
读取时通过wellmaillist.txt文件读取所有文件，再次生成字典
"""
