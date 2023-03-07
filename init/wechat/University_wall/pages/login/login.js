// pages/login/login.js
var app = getApp();
Page({

    /**
     * 页面的初始数据
     */
    data: {

    },
    student_id:function(e){
        // console.log(e.detail.value);
        this.setData({student_id:e.detail.value})
    },
    password:function(e){
        // console.log(e.detail.value);
        this.setData({password:e.detail.value})
    },
    login:function(){
        let student_id = this.data.student_id
        let password = this.data.password
        if(student_id==""||password==""||student_id==undefined||password==undefined){
            wx.showToast({
                title: '学号或密码不能为空',
                icon: 'none'
              })
        }
        else{
            // console.log(student_id);
            // console.log(password);
            var pat = /\D/;
            let str=student_id;
            // console.log(pat.test(str));
            if(pat.test(str)==true){
    
                wx.showToast({
                  title: '学号必须为纯数字',
                  icon: 'none'
                })
            }else{
                // console.log(this.data.student_id,this.data.password);
                // that = this
                wx.request({

                    url: app.globalData.djangourl+'api/login/',
                    data: {
                        student_id:this.data.student_id,
                        password:this.data.password
                    },
                    method: 'POST',
                    dataType: 'json',
                    success:function(res) {
                        console.log(res.data);
                        // console.log(res.data.status);
                        // console.log(res.data.message);
                        if(res.data.status !=true){
                            wx.showToast({
                                title:res.data.message,
                                icon: 'none'
                              })

                        }else{
                        wx.showToast({
                            title:res.data.message,
                            icon: 'none'
                          })
                        //   console.log("获取",res.data.user_login);
                          app.globalData.userlogin=res.data.user_login
                        //   console.log("全局",app.globalData.userlogin);
                          wx.setStorageSync('userlogin', res.data.user_login)
                        //   console.log("本地",wx.getStorageSync('userlogin'));



                          wx.navigateBack({
                            delta: 0,
                            success: (res) => {},
                            fail: (res) => {},
                            complete: (res) => {},
                          })
                        }

                    }
                })


            }
    


        }




    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad(options) {
        console.log("ss",options);

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