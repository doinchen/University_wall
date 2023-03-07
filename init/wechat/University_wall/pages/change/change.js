var app = getApp();
// pages/change/change.js

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
    avatarurl: "../../images/logo.png"

  },
  choosefile: function () {
    let that = this
    wx.chooseImage({
      count: 1,
      sizeType: ['original'],
      success: function (e) {
        console.log(e.tempFiles[0].path);
        var avatarurl = e.tempFiles[0].path
        that.setData({
          avatarurl: avatarurl
        })
        // wx.cropImage({
        //   src:avatarurl,
        //   cropScale:"1:1",
        //   success:function(e){
        //     console.log(e.tempFilePath);
        //       that.setData({
        //    avatarurl:e.tempFilePath})
        //   }


        // })

      }

    })
  },
  upfile: function () {
    let time = formatDate();
    let stu_num = app.globalData.userlogin.student_number
    let filePath = this.data.avatarurl;
    let name = app.globalData.userlogin.username

    wx.uploadFile({
      filePath: filePath,
      name: stu_num,
      url: app.globalData.djangourl + 'api/UpLoad_avatar/',
      method: 'POST',
      formData: { // 传输一些需要的数据
        name: name,
        id: stu_num,
        time: time,
        per_name: app.globalData.userlogin.name,
        phone: app.globalData.userlogin.id

      },
      success: function (res) {
        console.log(res);

        if (res.data == "true") {
          // console.log("aaabbbaaaa");
          wx.showToast({
            title: '上传成功',
            icon: 'none'
          })
          wx.request({
            url: app.globalData.djangourl + 'api/logined/',
            method: 'POST',
            dataType: 'json',
            data: { // 传输一些需要的数据
              id:app.globalData.userlogin.id,
              stu_num: stu_num,


            },
            success:function(res){
              console.log(res.data.asd);
              app.globalData.userlogin.avatarurl=res.data.asd
              wx.setStorageSync('userlogin', app.globalData.userlogin)
              console.log(app.globalData.userlogin);
              console.log(wx.getStorageSync("userlogin"));
              wx.navigateBack({
              })
            }


          })




        } else {
          var str = res.data;
          var str = str.substring(2, str.length - 2);
          console.log(str);
          wx.showToast({
            title: str,
            icon: 'none'
          })

        }
        var str = dict(str.substring(1,str.length-1));
        console.log(str);
        var dict =str
        console.log(dict);


      },
      fail: function (e) {
        console.log(e.errMsg);
        if (e.errMsg == "uploadFile:fail createUploadTask:fail file not found") {
          wx.showToast({
            title: '请选择图片',
            icon: 'none'
          })

        }


      }


    })

  },
  inputuname:function(e){
    var str = e.detail.value;
    var len = 0;
    for (var i = 0; i < str.length; i++) {
        if (str.charCodeAt(i) > 127 || str.charCodeAt(i) == 94) {
            len += 2;
        } else {
            len++;
        }
    }
    let c = 20-len
    console.log(len);
    console.log(e.detail.value);
    this.setData({
      username:e.detail.value,
      c:c
    })

  },
  changeuname:function(){
     let u_name_len = this.data.c
    if(u_name_len<0){
      wx.showToast({
        title: '字数超出',
        icon:'none'
      })
    }else{
      let username = this.data.username
      console.log("id",app.globalData.userlogin.id);
      console.log("stu",app.globalData.userlogin.student_number);
      wx.request({
        url: app.globalData.djangourl+'api/Change_username/',
        method:'POST',
        dataType: 'json',
        data: { // 传输一些需要的数据
          id:app.globalData.userlogin.id,
          stu_num: app.globalData.userlogin.student_number,
          new_username:username


        },
        success:function(res){
          if(res.data.status==true){
            console.log(res.data.username);
            app.globalData.userlogin.username=res.data.username
            wx.setStorageSync('userlogin', app.globalData.userlogin)
            wx.navigateBack({})

          }
          
        }
        
      })

    }
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    console.log(options.type);
    this.setData({
        type: options.type
      }

    )

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