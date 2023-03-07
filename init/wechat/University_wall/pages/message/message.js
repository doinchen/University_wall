var app = getApp();
var ass = require('../../Node/code.js')
Page({

    /**
     * 页面的初始数据
     */
    data: {
      stu:app.globalData.userlogin.student_number,
      stars:
      [
        {
          username:'sadfa',
          avatarurl:'../../images/logo.png',
          talkabout:'sadfad',
          stu:'210809039040'
        },
        {
          username:'sadfa',
          avatarurl:'../../images/logo.png',
          talkabout:'sadfad',
          stu:'210809037050'
        },
        {
          username:'sadfa',
          avatarurl:'../../images/logo.png',
          talkabout:'sadfad',
          stu:'210809039040'
        },        {
          username:'sadfa',
          avatarurl:'../../images/logo.png',
          talkabout:'sadfad',
          stu:'210809039040'
        },
        {
          username:'sadfa',
          avatarurl:'../../images/logo.png',
          talkabout:'sadfad',
          stu:'210809037050'
        },
        {
          username:'sadfa',
          avatarurl:'../../images/logo.png',
          talkabout:'sadfad',
          stu:'210809039040'
        },        {
          username:'sadfa',
          avatarurl:'../../images/logo.png',
          talkabout:'sadfad',
          stu:'210809039040'
        },
        {
          username:'sadfa',
          avatarurl:'../../images/logo.png',
          talkabout:'sadfad',
          stu:'210809037050'
        },
        {
          username:'sadfa',
          avatarurl:'../../images/logo.png',
          talkabout:'sadfad',
          stu:'210809039040'
        },        {
          username:'sadfa',
          avatarurl:'../../images/logo.png',
          talkabout:'sadfad',
          stu:'210809039040'
        },
        {
          username:'sadfa',
          avatarurl:'../../images/logo.png',
          talkabout:'sadfad',
          stu:'210809037050'
        },
        {
          username:'sadfa',
          avatarurl:'../../images/logo.png',
          talkabout:'sadfad',
          stu:'210809039040'
        },
      ],


    },
    onTextInput:function(res){
      //console.log(res.detail.value);
      this.setData({
        input:res.detail.value
      })
    },
    onSend:function(){
      let input = this.data.input
      let stu_num = this.data.stu_num
      console.log('asdfafa',app.globalData.userlogin.student_number);

      console.log(input);
      let con = {
          input:input,
          app_stu:stu_num.app_stu,
          user_stu:stu_num.user_stu,
          time:ass.formatDate(),
          type:'message'
        }
      wx.sendSocketMessage({

        data:JSON.stringify(con)
      })
      this.setData({
        talkabout:''
      })
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad(options) {
        this.setData({
            stu_num:options

        })
      
      let con = {
        stu:options.app_stu,
        type:'open' }
      wx.sendSocketMessage({
        data:JSON.stringify(con),
      })
      wx.request({
        url: app.globalData.djangourl+'api/room_messsage/',
        method:'POST',
        dataType: 'json',
        data:{
          "app_stu":options.app_stu,
          "user_stu":options.user_stu,
          "time":ass.formatDate()
          },
        success:res=>{ 
            console.log(res.data.list.length-1);
            this.setData({
                // Blogger:res.data.Blogger,
                // Fans:res.data.Fans,
                // favor_count:res.data.favor_count,
                // head:res.data.head[0],
                stars:res.data.list,
                toLast:'item'+(res.data.list.length-1)
            })
        }
        
    })






      console.log('mess',options);
      const windowInfo = wx.getWindowInfo()
      console.log(windowInfo.	windowWidth)
      console.log(windowInfo.	windowHeight)
      let height = 750/windowInfo.windowWidth*windowInfo.	windowHeight
      console.log(height);
      let height2 = height-60-75

      this.setData({
        height:height,
        height2:height2
      })
      wx.getSystemInfo({

        success(res) {
          console.log(res.windowHeight);
      
          // that.setData({
      
          //   windowHeightrpx: res.windowHeight / (res.windowWidth / 750)
      
          // })
      
        }
      
      })


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
        wx.onSocketMessage((result) => {
            console.log('showmessage',result);
            let ass = JSON.parse(result.data)
            console.log(ass[0].list);
            this.setData({
                stars:ass[0].list,
                toLast:'item'+(ass[0].list.length-1)
            })


        })

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