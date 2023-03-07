// pages/us/us.js
var ass = require('../../Node/code.js')

const app = getApp()
Page({

    /**
     * 页面的初始数据
     */
    data: {
        userstu:app.globalData.userlogin.student_number,
        navtype:'all',
        a:"text",
        b:"image",
        c:"video",

    },
    click:function(res){
        console.log(res.currentTarget.dataset.type);
        wx.request({
          url: app.globalData.djangourl+'api/type_click/',
          method:'POST',
          dataType: 'json',
          data:{
              "stu":this.data.stu,
              "type":res.currentTarget.dataset.type
        },
          success:res=>{
              console.log(res.data);
              this.setData({
                list:res.data.list,
              })
              
            }
        })
        
        this.setData({
            navtype:res.currentTarget.dataset.type

        })
    },
    Fans_Blogger:function(res){
        console.log(res.currentTarget);
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
                    FABLEbtye:"primary",
                      FABLE:"关注"
                  })
              }else{
                  this.setData({
                    FABLEbtye:"warn",
                      FABLE:"已关注"
                  })
              }
          }
        })
  
    },
    getinto:function(){
        wx.navigateTo({
            url: '/pages/personal/personal'
          })

    },
    gotomess:function(res){
      console.log(res.currentTarget.dataset);


      let mess = res.currentTarget.dataset
      wx.navigateTo({
          url: '/pages/message/message?app_stu=' + mess.app_stu + '&user_stu=' + mess.user_stu
      })


    },
    nav:function(res){
        console.log(res.currentTarget.dataset.detail);
        let mess = res.currentTarget.dataset.detail
        wx.navigateTo({
            url: '/pages/detail/detail?time_TS=' + mess.time_TS + '&type_text=' + mess.user.type_text
        })
        
      },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad(options) {
        console.log('f',options.time_TS);
        this.setData({
            stu:options.time_TS
        })
        wx.request({
            url: app.globalData.djangourl+'api/user_US/',
            method:'POST',
            dataType: 'json',
            data:{"stu":options.time_TS,
            "student_number":app.globalData.userlogin.student_number
        },
            success:res=>{
                console.log(res);
                if(res.data.FABLE==0){
                    this.setData({
                        FABLE:"关注",
                        FABLEbtye:"primary",
                    })

                }else if(res.data.FABLE==1){
                    this.setData({
                        FABLE:"已关注",
                        FABLEbtye:"warn",
                    })

                }
                this.setData({
                    Blogger:res.data.Blogger,
                    Fans:res.data.Fans,
                    favor_count:res.data.favor_count,
                    head:res.data.head[0],
                    list:res.data.list
                })
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