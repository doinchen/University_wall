// index.js
// 获取应用实例
var ass = require('../../Node/code.js')

const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
      a:"text",
      b:"image",
      c:"video",

      list:[{
          hidden:false,
          user:{
              username:"杜宇琛",
          avatarurl:"../../images/logo.png",
          },
          
          type:"text",
          favor_count:"23",
          comment_count:"350",
          create_time:"2023-01-01",
          campus:"兴安校区",
          text:"你今天好吗？",
          type_text:[{asd:"你今天好吗？"}]
      },
      {
        hidden:false,
        user:{
            username:"杜宇琛",
        avatarurl:"../../images/logo.png",
        },
        type:"image",
        favor_count:"23",
        comment_count:"345",
        create_time:"2013-01-01",
        campus:"鹿泉校区",
        text:"你今天怎么样？",
        type_text:[
            // {asd:"../../images/1.webp"},
            // {asd:"../../images/1.webp"},
            {url:"../../images/1.webp"},
            {url:"../../images/1.webp"},
            {url:"../../images/1.webp"},
            {url:"../../images/1.webp"},
            {url:"../../images/1.webp"},
            {url:"../../images/1.webp"},
            {url:"../../images/1.webp"}
        ]
    },
    {
        hidden:false,
        user:{
            username:"杜宇琛",
        avatarurl:"../../images/logo.png",
        },
        type:"video",
        favor_count:"423",
        comment_count:"35",
        create_time:"2023-01-31",
        campus:"警安校区",
        text:"快看我拍的视频？",
        type_text:{video_url:"http://wxsnsdy.tc.qq.com/105/20210/snsdyvideodownload?filekey=30280201010421301f0201690402534804102ca905ce620b1241b726bc41dcff44e00204012882540400&bizid=1023&hy=SH&fileparam=302c020101042530230204136ffd93020457e3c4ff02024ef202031e8d7f02030f42400204045a320a0201000400",
        video_image:"../../images/2.webp"
    
    }
    
    }
        

      ]
    
  },
  nav:function(res){
    console.log(res.currentTarget.dataset.detail);
    let mess = res.currentTarget.dataset.detail
    wx.navigateTo({
        url: '/pages/detail/detail?time_TS=' + mess.time_TS + '&type_text=' + mess.user.type_text
    })
    
  },
  showInput() {
    this.setData({
      inputShowed: true,
    });
  },
  hideInput() {
    this.setData({
      inputVal: '',
      inputShowed: false,
    });
  },
  clearInput() {
    this.setData({
      inputVal: '',
    });
  },
  inputTyping(e) {
    this.setData({
      inputVal: e.detail.value,
    });
  },
  Getto:function(res){
    console.log(res.currentTarget.dataset.stu)
    wx.navigateTo({
        url: '/pages/us/us?time_TS=' + res.currentTarget.dataset.stu
    })



  },
  gotosearch:function(){
    wx.navigateTo({
        url: '/pages/search/search'
    })
      
  },


  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    wx.request({
        url: app.globalData.djangourl+'api/WX_index/',
        method:'GET',
        success:res=>{
            console.log(res);
            this.setData(
                {
                    list:res.data
                }
            )
        }
      })

      
    
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
    
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
      wx.request({
        url: app.globalData.djangourl+'api/WX_index/',
        method:'GET',
        success:res=>{
            console.log(res);
            this.setData(
                {
                    list:res.data
                }
            )
        }
      })
    
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {
    
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
    
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
    wx.request({
        url: app.globalData.djangourl+'api/WX_index/',
        method:'GET',
        success:res=>{
            console.log(res);
            this.setData(
                {
                    list:res.data
                }
            )
        }
      })
    
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
    
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {
    
  }
})