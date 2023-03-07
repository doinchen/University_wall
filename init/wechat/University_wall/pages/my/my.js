var app = getApp();
// pages/my/my.js
Page({

    /**
     * 页面的初始数据
     */
    data: {
        menu_list:[
            {
                id:"1",
                imgurl:"../../images/people.png",
                text:"个人信息"
            },
            {
                id:"2",
                imgurl:"../../images/label.png",
                text:"我的主页"
            },
            {
                id:"3",
                imgurl:"../../images/addressbook.png",
                text:"关注列表"
            },
            {
                id:"4",
                imgurl:"../../images/supply.png",
                text:"收藏列表"
            },
        ],
        login:false,
        userInfo:{
            avatarurl:"../../images/logo.png",
            username:"未登录"
    }

    },


    onTouchStart:function(e){
        // console.log("data_id",e.currentTarget.dataset.id);
        this.setData({
            check:e.currentTarget.dataset.id
        })

    },
    onTouchEnd:function(){
        this.setData({
            check:false
        })

    },


    
    gateTo:function(w){

        console.log('aaa',w.currentTarget.dataset.id);
        let t = w.currentTarget.dataset.id;
        if(t==1){
            console.log('个人');
            wx.navigateTo({
              url: '/pages/personal/personal'
            })
        }else if(t == 2){
            console.log('主页');
            wx.navigateTo({
                url: '/pages/us/us?time_TS=' + app.globalData.userlogin.student_number
              })
        }

    },
    gotologin:function(){
        let events=1
        wx.navigateTo({
          url: '/pages/login/login',
        })

    },
    gotoout:function(){
        wx.setStorageSync('userlogin',null)
        app.globalData.userlogin = {}
        this.setData({
            login:false,
            userInfo:{
                avatarurl:"../../images/logo.png",
                username:"未登录"
        }
        })

    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad(options) {
        // console.log("全局",app.globalData.userlogin);
        // console.log("本地",wx.getStorageSync('userlogin'));

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
        // console.log(app.globalData.userlogin.id==undefined);
        if(app.globalData.userlogin.id!=undefined){
             
            this.setData({
                login:true,
                userInfo:app.globalData.userlogin
            })

        }else{
            this.setData({
                login:false
            })
        }

        

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