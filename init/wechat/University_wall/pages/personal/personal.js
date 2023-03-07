var app = getApp();
// pages/personal/personal.js
Page({

    /**
     * 页面的初始数据
     */
    data: {

    },
    change:function(e){
        
        console.log("data_type",e.currentTarget.dataset.input);
        // if(e.currentTarget.dataset.input == "avatarurl"){
        //     var type = e.currentTarget.dataset.input
            

        // }else if(e.currentTarget.dataset.input == "username"){

        // }else if(e.currentTarget.dataset.input == "id"){

        // }else if(e.currentTarget.dataset.input == "password"){

        // }
        wx.navigateTo({
          url: '/pages/change/change?type='+e.currentTarget.dataset.input,
        })
        
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad(options) {
        // console.log(app.globalData.userlogin);
        this.setData({
            user_in:app.globalData.userlogin
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
      this.setData({
        user_in:app.globalData.userlogin
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