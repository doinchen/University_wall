var app = getApp();
var ass = require('../../Node/code.js')
Page({

  /**
   * 页面的初始数据
   */
  data: {

    assd:[{
        asdfasdf:1,
        pass:{
            asd:'sfasd',
            asd:'sfasd',
            asd:'sfasd',
        }
    },{
        asdfasdf:1,
        pass:{
            asd:'sfasd',
            asd:'sfasd',
            asd:'sfasd',
        }
    }

    ],    
    list:[{
        id:"1",
        selected:false,
        hidden:false,
        username:"杜宇琛",
        avaterUrl:"../../images/logo.png",
        type:"text",
        good:"23",
        message:"350",
        date:"2023-01-01",
        where:"兴安校区",
        text:"你今天好吗？",
        Url:[{asd:"你今天好吗？"}]
    },
    {
      id:"2",
      selected:false,
      hidden:false,
      username:"杜宇琛",
      avaterUrl:"../../images/logo.png",
      type:"image",
      good:"23",
      message:"345",
      date:"2013-01-01",
      where:"鹿泉校区",
      text:"你今天怎么样？",
      Url:[
          // {asd:"../../images/1.webp"},
          // {asd:"../../images/1.webp"},
          {asd:"../../images/1.webp"},
          {asd:"../../images/1.webp"},
          {asd:"../../images/1.webp"},
          {asd:"../../images/1.webp"},
          {asd:"../../images/1.webp"},
          {asd:"../../images/1.webp"},
          {asd:"../../images/1.webp"}
      ]
  },
  {
      id:"3",
      selected:false,
      hidden:false,
      username:"杜宇琛",
      avaterUrl:"../../images/logo.png",
      type:"video",
      good:"423",
      message:"35",
      date:"2023-01-31",
      where:"警安校区",
      text:"快看我拍的视频？",
      Url:[{asd:"http://wxsnsdy.tc.qq.com/105/20210/snsdyvideodownload?filekey=30280201010421301f0201690402534804102ca905ce620b1241b726bc41dcff44e00204012882540400&bizid=1023&hy=SH&fileparam=302c020101042530230204136ffd93020457e3c4ff02024ef202031e8d7f02030f42400204045a320a0201000400"}]
  
  }
      

    ],
      oldid:"-1",
    a:"text",
    b:"image",
    c:"video",
    


    
  },
  chick:function(e){
    let con
      console.log(e.currentTarget.dataset);

      console.log(this.data.assd);
      if(e.currentTarget.dataset.type == "once"){
        con = {
            "type": e.currentTarget.dataset.type ,
            "stu":e.currentTarget.dataset.stu
        }
      }else if(e.currentTarget.dataset.type == "all"){
        con = {
            "type": e.currentTarget.dataset.type ,
            "stu":app.globalData.userlogin.student_number,
        }
      }
      wx.request({ 
        url:app.globalData.djangourl+'api/blog_once/',
        method:'POST',
        dataType: 'json',
        data:con,
        success:res=>{
            console.log(res.data); 
            this.setData({
            //     blog_list:res.data.blog_list,
                 list:res.data.list
            })
        }

      })
      let oldid=e.currentTarget.dataset.index
      this.setData({oldid:oldid})
  },
  bloger_one:function(res){
    console.log(res.currentTarget.dataset);


  },
  nav:function(res){
    console.log(res.currentTarget.dataset.detail);
    let mess = res.currentTarget.dataset.detail
    wx.navigateTo({
        url: '/pages/detail/detail?time_TS=' + mess.time_TS + '&type_text=' + mess.user.type_text
    })
    
  },
  Getto:function(res){
    console.log(res.currentTarget.dataset.stu)
    wx.navigateTo({
        url: '/pages/us/us?time_TS=' + res.currentTarget.dataset.stu
    })



  },


  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
      console.log(this.data.assd);
      wx.request({ 
        url:app.globalData.djangourl+'api/Active/',
        method:'POST',
        dataType: 'json',
        data:{
            userstu:app.globalData.userlogin.student_number
        },
        success:res=>{
            console.log(res.data.blog_list); 

            this.setData({
                blog_list:res.data.blog_list,
                list:res.data.list,
                code:res.data.reses
            })
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
        url:app.globalData.djangourl+'api/Active/',
        method:'POST',
        dataType: 'json',
        data:{
            userstu:app.globalData.userlogin.student_number
        },
        success:res=>{
            console.log(res.data.blog_list); 

            this.setData({
                blog_list:res.data.blog_list,
                list:res.data.list,
                code:res.data.reses
            })
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