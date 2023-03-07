// pages/detail/detail.js
var app = getApp();
var ass = require('../../Node/code.js')
Page({

  /**
   * 页面的初始数据
   */
  data: {
    FABL:"关注",
    FABLbt:"primary",

    userstu:app.globalData.userlogin.student_number,
    fill_detail_favor:"",
    comment: true,
    show_url: '../../images/1.webp',
    id: '0',
    send_message: true,
    a: "text",
    b: "image",
    c: "video",
    type: "video",

    list: {
      hidden: false,
      user: {
        username: "杜宇琛",
        avatarurl: "../../images/logo.png",
      },

      type: "text",
      favor_count: "23",
      comment_count: "350",
      create_time: "2023-01-01",
      campus: "兴安校区",
      text: "你今天好吗？",
      type_text: [{
        asd: "你今天好吗？"
      }]
    },
    type_text1: [{
        url: '../../images/2.webp'
      },
      {
        url: '../../images/2.webp'
      },
      {
        url: '../../images/1.webp'
      },
      {
        url: '../../images/2.webp'
      },
      {
        url: '../../images/2.webp'
      },
      {
        url: '../../images/2.webp'
      },
      {
        url: '../../images/2.webp'
      },
      {
        url: '../../images/2.webp'
      },
      {
        url: '../../images/2.webp'
      },
    ]
  },
  mess_close:function(){
    this.setData({
      send_message: true
    })

  },
  send_fa: function (res) {
    //console.log(res.currentTarget.dataset);
    
    this.setData({
      root_id: res.currentTarget.dataset.root_id,
      re_user: res.currentTarget.dataset.re_user,
      depth: parseInt(res.currentTarget.dataset.depth) + 1,
      send_message: false
    })
  },
  send_son: function () {
    let cont_mess = this.data.cont_mess
    let detail = this.data.detail
    //console.log(ass.formatDate());
    let news_TS = detail.create_time.time03
    let news_ustu = detail.user.type_text
    let content_text = cont_mess
    let user = app.globalData.userlogin.student_number
    let create_time = ass.formatDate()
    let root_id = this.data.root_id
    let re_user = this.re_user
    let depth = this.data.depth
    let con = {
      "news_TS" : detail.create_time.time03,
      "news_ustu": detail.user.type_text,
      "content_text" : cont_mess,
      "user" : app.globalData.userlogin.student_number,
      "create_time" : ass.formatDate(),
      "root_id" : this.data.root_id,
      "re_user": this.data.re_user,
      "depth" : String(this.data.depth),
      "type":"comment"

    }
    //console.log('提交前',con);

    //console.log(JSON.stringify(con))
    // let ll = JSON.stringify(con)
    // console.log(JSON.parse(ll));
  
    wx.sendSocketMessage({
      data: JSON.stringify(con),
  })
    this.setData({
      send_message: true
    })
  },
  send_con: function (res) {
    // console.log(res.detail.value);
    this.setData({
      cont_mess: res.detail.value
    })
  },
  choose: function (res) {
    //console.log(res.currentTarget.dataset.url);
    this.setData({
      id: res.currentTarget.dataset.index,
      show_url: res.currentTarget.dataset.url
    })
  },
  choose_comment: function (res) {
    //console.log(res.currentTarget.dataset);
    let text = res.currentTarget.dataset
    //console.log(text.id);
    let detail = this.data.detail
    wx.request({
      url: app.globalData.djangourl+'api/SecondComment/',
      method:'POST',
      dataType: 'json',
      data:{
        "news_TS" : detail.create_time.time03,
        "news_ustu": detail.user.type_text,
        "user_check" : app.globalData.userlogin.student_number,
        "time_TS":text.ts,
        //"id":String(text.id),
        "user":text.rootuser,
        "id":text.id,
      },
      success:res=>{
        //console.log(res.data);
        this.setData({
          comment_back_head:res.data.data[0],
          comment_back_list:res.data.datalist,
        })

      }

    })
    
    this.setData({
      comment: false
    })
  },
  close_choose: function () {
    this.setData({
      comment: true
    })

  },

  detail_favor:function(res){
    let cont_mess = this.data.cont_mess
    let detail = this.data.detail
    //console.log(ass.formatDate());
    let con = {
      "news_TS" : detail.create_time.time03,
      "news_ustu": detail.user.type_text,
      "user" : app.globalData.userlogin.student_number,
      "create_time" : ass.formatDate(),

    }
    //console.log('提交前',con);

    //console.log(JSON.stringify(con))
    // let ll = JSON.stringify(con)
    // console.log(JSON.parse(ll));
  
    wx.request({
      url: app.globalData.djangourl+'api/Detail_favor/',
      method:'POST',
      dataType: 'json',
      data: con,
      //data: JSON.stringify(con),
      success:res=>{
        console.log('点赞返回',res);
        this.setData({
          detail: res.data.data[0],
          //commentlist: res.data.comment
        })
        if (res.data.fill_detail_favor=='0'){
          this.setData({
            fill_detail_favor:""
          })
        }else{
          this.setData({
            fill_detail_favor:"_fill"
          })

        }
        
      }

  })
  },

  comment_fover:function(res){
    console.log(res.currentTarget.dataset);
    let detail = this.data.detail
    let comment_mess = res.currentTarget.dataset

    let con = {
      "news_TS" : detail.create_time.time03,
      "news_ustu": detail.user.type_text,
      "user" : app.globalData.userlogin.student_number,
      "comment_id":comment_mess.comment_id,
      "depth": comment_mess.depth,
      "create_time" : ass.formatDate(),

    }

    wx.request({
      url: app.globalData.djangourl+'api/Comment_fover/',
      method:'POST',
      dataType: 'json',
      data:con,
      //data: JSON.stringify(con),
      success:res=>{
        console.log('点赞返回',res.data.sedcomment);
        for (let index = 0; index <res.data.comment.length; index++) {
          if(res.data.comment[index].id==comment_mess.comment_id){
            this.setData({
              comment_back_head:res.data.comment[index]
            })
          }     
        }


        this.setData({
          comment_back_list:res.data.sedcomment,
          commentlist: res.data.comment
        })
        //this.setData({
          
          //comment_back_list:res.data.datalist,
        //})



        
      }

  })

  },
  Fans_Blogger:function(res){
      console.log(res.currentTarget.dataset);
      let FB = res.currentTarget.dataset
      let con = {
        app_stu:FB.app_stu,
        user_stu: FB.user_stu

      }
      wx.request({
        url: app.globalData.djangourl+'api/Fans_Blogger/',
        method:'POST',
        dataType: 'json',
        data:con,
        success:res=>{
            console.log(res.data.FABL);
            if(res.data.FABL=="0"){
                this.setData({
                    FABLbt:"primary",
                    FABL:"关注"
                })
            }else{
                this.setData({
                    FABLbt:"warn",
                    FABL:"已关注"
                })
            }
        }
      })

  },






  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    console.log(options);
    console.log(app.globalData.userlogin.student_number);
    let dict = {
      time_TS:options.time_TS,
      type_text:options.type_text,
      create_time:ass.formatDate(),
      student_number:app.globalData.userlogin.student_number}
    console.log(dict);
    wx.request({
      url: app.globalData.djangourl + 'api/WX_detail/',
      method: 'POST',
      data: dict,
      success: res => {
        console.log(res.data.FABL);
        if(res.data.FABL=="0"){
            this.setData({
                FABLbt:"primary",
                FABL:"关注"
            })
        }else{
            this.setData({
                FABLbt:"warn",
                FABL:"已关注"
            })
        }


        this.setData({
          detail: res.data.data[0],
          commentlist: res.data.comment
        })
        if (res.data.data[0].type == 'image') {
          this.setData({
            show_url: res.data.data[0].type_text[0].url

          })
        }
        if (res.data.fill_detail_favor=='0'){
          this.setData({
            fill_detail_favor:""
          })
        }else{
          this.setData({
            fill_detail_favor:"_fill"
          })

        }


      }

    })
    let that = this
    wx.onSocketMessage(function (res) {
      //console.log(JSON.parse(res.data));
      that.setData({
        commentlist:JSON.parse(res.data)
      })
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
    let that = this
    wx.onSocketMessage(function (res) {
      let ass = JSON.parse(res.data)
      console.log(ass[1].list);
      if(ass[0].aaa=='1'){
        that.setData({
          commentlist:ass[1].list,
        })

      }else{
      that.setData({
        
        comment_back_list:ass[1].list,

      })
      }


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
    console.log();

  }
})