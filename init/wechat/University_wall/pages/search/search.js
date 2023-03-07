// pages/search/search.js
// 获取应用实例
var ass = require('../../Node/code.js')

const app = getApp()
Page({

    /**
     * 页面的初始数据
     */
    data: {
        hidden:false,
        a:"text",
        b:"image",
        c:"video",
        textmess:'xczvx'

    },
    clearInput:function(){
        this.setData({
            textmess:"",
            hidden:false,
            intext:""
        })
        

    },
    // inputclick:function(){
    //     this.setData({
    //         textmess:"",
    //         intext:""
    //     })

    // },
    inputTyping:function(res){
        console.log(res.detail.value);
        this.setData({
            intext:res.detail.value
        })


    },
    searchclick:function(){
        console.log(this.data.intext);
        console.log(this.data.textmess);
        let text
        if( (this.data.intext == undefined || this.data.intext =="")&&(this.data.textmess == undefined || this.data.textmess == ""))
        {
            var inputmess = 0
            console.log("dsafasfsafa00");
            wx.showToast({
              title: '搜索不能为空',
              icon:'none'
            })
        }
        else if(this.data.intext == undefined || this.data.intext ==""){
            text = this.data.textmess
            console.log("dsafasfsafa11");
        }else if(this.data.textmess == undefined || this.data.textmess == ""){
            text = this.data.intext
            console.log("dsafasfsafa22");
        }
        if(inputmess!=0){
            wx.request({
                url: app.globalData.djangourl+'api/searchclick/',
                method:'POST',
                dataType: 'json',
                data:{
                    text:text
                },
                success:res=>{
                    console.log(res.data.list);
                    this.setData({
                        list:res.data.list,
                        hidden:true
                    })

                }
      
              })


        }



    },
    heatclick:function(res){
        console.log(res.currentTarget.dataset.in);
        this.setData({
            textmess:res.currentTarget.dataset.in

        })

    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad(options) {
        wx.request({
          url: app.globalData.djangourl +'api/top_search/',
          method:'GET',
          dataType:'json',
          success:res=>{
              console.log('热搜',res.data.list);
              this.setData({
                  heatlist:res.data.list
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