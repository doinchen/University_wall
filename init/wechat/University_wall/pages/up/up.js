// pages/up/up.js
var app = getApp();

var ass = require('../../Node/code.js')


function formatDate() {
    var date = new Date();
    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    var day = date.getDate();
    var hh = date.getHours();
    var mm = date.getMinutes();
    var ss = date.getSeconds();
    var arr = ['日', '一', '二', '三', '四', '五', '六'];
    var week = arr[date.getDay()];

    function add0(val) {
        return (val < 10 ? '0' + val : val);
    }
    month = add0(month);
    day = add0(day);
    hh = add0(hh);
    mm = add0(mm);
    ss = add0(ss);
    return year + '-' + month + '-' + day + ' ' + hh + ':' + mm + ':' + ss

}
Page({

    /**
     * 页面的初始数据
     */
    data: {
        schedule:0,
        imagelen:0,
        input_text:'',
        no_have_video:true,
        video:{},
        Url: [],
        type: "text",
        image_number: 0,
        type_t: "text",
        type_i: "image",
        type_v: "video",
        len: 140

    },
    radioChange(e) {
        console.log('radio发生change事件，携带value值为：', e.currentTarget.dataset.type);
        if (e.currentTarget.dataset.type == "text") {
            let type = "text"
            console.log(type);

            this.setData({
                type: type
            });
        }
        if (e.currentTarget.dataset.type == "image") {
            let type = "image"
            console.log(type);

            this.setData({
                type: type
            });
        }
        if (e.currentTarget.dataset.type == "video") {
            let type = "video"
            console.log(type);

            this.setData({
                type: type
            });
        }


        // const { radioItems } = this.data;
        // for (let i = 0, len = radioItems.length; i < len; ++i) {
        //   radioItems[i].checked = radioItems[i].value == e.detail.value;
        // }

        // this.setData({
        //   radioItems,
        // });
    },
    inputtext: function (e) {
        var str = e.detail.value;
        var len = 0;
        for (var i = 0; i < str.length; i++) {
            if (str.charCodeAt(i) > 127 || str.charCodeAt(i) == 94) {
                len += 2;
            } else {
                len++;
            }
        }
        // console.log(len);
        let a = 140 - len
        this.setData({
            len: a,
            str: str
        })
    },

    up_image: function () {
        wx.chooseImage({
            sizeType: ['original', 'compressed'],
            sourceType: ['album', 'camera'],
            count: 9,
            success: res => {
                //   console.log(res);
                // console.log(res.tempFiles.length);
                let a = this.data.Url.length
                let b = res.tempFiles.length + a
                if (b > 9) {
                    wx.showToast({
                        title: '图片最多九张',
                        icon: 'none'
                    })
                    return
                }
                let c = this.data.Url.concat(res.tempFiles)
                console.log(c);
                this.setData({
                    Url: c,
                    image_number: b
                })

            }
        })

    },
    close_image:function(res){
        console.log(res.currentTarget.dataset.id);
        let len = this.data.image_number
        console.log('前',len);
        let index = res.currentTarget.dataset.id
        let list = this.data.Url
        console.log('前',list);
        list.splice(index,1)
        len=len-1
        console.log('后',len);
        console.log('后',list);
        this.setData({
            Url: list,
            image_number: len
        })
        

    },
    up_video:function(){
        wx.chooseVideo({
            compressed:true,
            sourceType:['album', 'camera'],
            success:res=>{
                console.log(res.tempFilePath);
                console.log(res.thumbTempFilePath);
                let v = {
                    tempFilePath:res.tempFilePath,
                    thumbTempFilePath:res.thumbTempFilePath
                }
                console.log(v);
                this.setData({
                    no_have_video:false,
                    video:v
                })
            }
        })
        
    },
    video_image:function(){
        wx.chooseImage({
            count: 1,
            sizeType: ['original', 'compressed'],
            sourceType: ['album'],
            success:res=>{
                console.log(res.tempFilePaths[0]);
                let video = this.data.video
                console.log(video);
                video.thumbTempFilePath=res.tempFilePaths[0]
                console.log(video);
                this.setData({
                    video:video
                })
            }
        })
    },
    close_video:function(){
        this.setData({
            no_have_video:true,
            video:{}
        })

    },


    send_text: function () {
        var that = this
        console.log( 'text',this.data.str);
        console.log( 'text',this.data.Url[0]);
        console.log( 'text',this.data.video.tempFilePath);
        if(this.data.str== undefined || this.data.str==''){
            console.log('text为空');
            wx.showToast({
              title: '文本不能为空',
              icon:'none'
            })
        }else if(this.data.type == "image" && this.data.Url[0] == undefined){
            console.log('image为空');
            wx.showToast({
                title: '图片不能为空',
                icon:'none'
              })

        }else if(this.data.type == "video" && this.data.video.tempFilePath == undefined){

            wx.showToast({
                title: '视频不能为空',
                icon:'none'
              })

        }else{        
        console.log(this.data.len);
        var creat_tm = formatDate()
        let len = this.data.len
        if (this.data.len < 0) {
            wx.showToast({
                title: '字数超出',
                icon: 'none'
            })
        } else {

            wx.request({
                url: app.globalData.djangourl + 'api/Receive/',
                method: 'POST',
                data: {
                    username: app.globalData.userlogin.username,
                    student_number: app.globalData.userlogin.student_number,
                    avatarurl: app.globalData.userlogin.avatarurl,
                    campus: app.globalData.userlogin.campus,
                    department: app.globalData.userlogin.department,
                    profession: app.globalData.userlogin.profession,
                    create_time:creat_tm,
                    type: this.data.type,
                    text: this.data.str,
                    type_text: app.globalData.userlogin.student_number
                },
                success: res => {
                    console.log(res);
                    if (res.errMsg == 'request:ok') {
                        wx.showToast({
                            title: res.data.text,
                            icon: "none"
                        })
                        if(this.data.type == "text"){
                            that.setData({
                                schedule:100
                            })
                            
                                that.setData({
                                            input_text:'',
                                            schedule:0,
                    
                                            Url:[],
                                            video:{},
                                            image_number: 0,
                                            no_have_video:true,
                                        })
                                    wx.switchTab({
                                        url: '../index/index',
                                    })
                    
                            
        
                        }
                     

                    } else {
                        wx.showToast({
                            title: res.data.data[0].msg,
                            icon: "none"
                        })
                        console.log(res.data.data[0].msg);
                    }

                }
            })

        }
        if (this.data.type == "image") {
            let pathlist = this.data.Url
            // console.log(this.data.image_number);
            let imagelen = this.data.image_number
            
            ass.getAccessToken().then(function (res) {
                // console.log('前面',res.access_token);
                var qual = 0
                var baidu_time=0
                // console.log('pathlist',pathlist);

                for(let i =0;i<imagelen;i++){
                    
                    // console.log('path',pathlist[i].path);
                    ass.sendimg(pathlist[i].path,0,res.access_token).then(function (res) {
                    console.log('第',i,'次');
                    console.log('baidu',res);
                    if(res.data.conclusionType==1){
                        qual++
                        console.log('百度检查1：i=',i,'qual=',qual);
                    }
                    baidu_time=baidu_time+1
                    console.log('百度检查2：i=',i,'qual=',qual);
                    console.log(i,qual,imagelen,baidu_time);
                    if(baidu_time==imagelen){
                        console.log('检验完毕');
                        if(qual==imagelen){
                            console.log('通过检测');
                            var old_schedule = 0
                            for(let j = 0 ; j<imagelen;j++){
                                console.log('update',pathlist[j].path);
                                const uploadTask=wx.uploadFile({
                                    filePath: pathlist[j].path,
                                    name: app.globalData.userlogin.student_number+j,
                                    url: app.globalData.djangourl+'api/Upload_Pictures/',
                                    method: 'POST',
                                    formData: { // 传输一些需要的数据
                                        len:imagelen,
                                        name: app.globalData.userlogin.student_number+j,
                                        id: app.globalData.userlogin.student_number,
                                        time:creat_tm
                                    },
                                    success:res=>{
                                        console.log('asdfadsfas',res);
                                        for(let k =0;k<65535;k++){
                                            for(let l =0;l<65535;l++){

                                            }

                                        }
                                    }
                                })
                                uploadTask.onProgressUpdate((res) => {
                                    console.log('上传进度', res.progress)
                                    console.log('上一次',old_schedule);
                                    app.globalData.image_nine = app.globalData.image_nine+ res.progress - old_schedule
                                    if(res.progress == 100)
                                        old_schedule=0
                                    else{
                                        old_schedule = res.progress
                                    }
                                    
                                    console.log('进度全局',app.globalData.image_nine);
                                    console.log('已经上传的数据长度', res.totalBytesSent)
                                    console.log('预期需要上传的数据总长度', res.totalBytesExpectedToSend)
                                    console.log('总进度',100*imagelen);
                                    var image_n = app.globalData.image_nine/(100*imagelen)
                                  console.log('已经行进的进度',image_n);
                                  that.setData({
                                    schedule:image_n*100
                                  })
                                  if(image_n == 1){
                                    that.setData({
                                                input_text:'',
                                                schedule:0,
                        
                                                Url:[],
                                                video:{},
                                                image_number: 0,
                                                no_have_video:true,
                                            })
                                        wx.switchTab({
                                            url: '../index/index',
                                        })
                        
                                }



                                  })



                            }




                        }else{
                            console.log('存在违规图片');
                        }
                    }


                    })
                }
              

                // console.log("后面",app.globalData.access_token);
            
            })
            
        }else if(this.data.type == "video"){
            let video=this.data.video
            console.log(video);
            var old_schedule = 0
            for(let i = 0 ; i<=1 ;i++){
                if(i==0){
                    var video_path=this.data.video.tempFilePath
                }
                if(i==1){
                    var video_path=this.data.video.thumbTempFilePath

                }
                const uploadTask=wx.uploadFile({
                  filePath: video_path,
                  name:  app.globalData.userlogin.student_number,
                  url: app.globalData.djangourl+'api/Upload_Video/',
                  method: 'POST',
                  formData: { // 传输一些需要的数据
                      name: app.globalData.userlogin.student_number,
                      id: app.globalData.userlogin.student_number,
                      type:i,
                      time:creat_tm
                  },
                  success:res=>{
                      console.log(i,res);

                      
                  },
                  fail:e=>{
                      console.log('错误',e);
                  }
                })
                uploadTask.onProgressUpdate((res) => {
                    console.log('上传进度', res.progress)
                    console.log('上一次',old_schedule);
                    app.globalData.image_nine = app.globalData.image_nine+ res.progress - old_schedule
                    if(res.progress == 100)
                        old_schedule=0
                    else{
                        old_schedule = res.progress
                    }
                    
                    console.log('进度全局',app.globalData.image_nine);
                    console.log('已经上传的数据长度', res.totalBytesSent)
                    console.log('预期需要上传的数据总长度', res.totalBytesExpectedToSend)
                    console.log('总进度',100*2);
                    var image_n = app.globalData.image_nine/(100*2)
                  console.log('已经行进的进度',image_n);
                  that.setData({
                    schedule:image_n*100
                  })
                  if(image_n == 1){
                    that.setData({
                                input_text:'',
                                schedule:0,
        
                                Url:[],
                                video:{},
                                image_number: 0,
                                no_have_video:true,
                            })
                        wx.switchTab({
                            url: '../index/index',
                        })
        
                }



                  })
            }



        }
        if(this.data.schedule == 100){
            this.setData({
                        input_text:'',
                        schedule:0,

                        Url:[],
                        video:{},
                        image_number: 0,
                        no_have_video:true,
                    })
                wx.switchTab({
                    url: '../index/index',
                })

        }

        
      
    }

    },

    send_it: function () {
        console.log(this.data.str);
        console.log();

    },
    aaa: function () {
        console.log("sdfa");
    },




    /**
     * 生命周期函数--监听页面加载
     */
    onLoad(options) {


    },

    /**
     * 生命周期函数--监听页面初次渲染完成
     */
    onReady() {

    },

    /**
     * 生命周期函数--监听页面显示
     */
    onShow() {

    },

    /**
     * 生命周期函数--监听页面隐藏
     */
    onHide() {

    },

    /**
     * 生命周期函数--监听页面卸载
     */
    onUnload() {

    },

    /**
     * 页面相关事件处理函数--监听用户下拉动作
     */
    onPullDownRefresh() {

    },

    /**
     * 页面上拉触底事件的处理函数
     */
    onReachBottom() {

    },

    /**
     * 用户点击右上角分享
     */
    onShareAppMessage() {

    }
})